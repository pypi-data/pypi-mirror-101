import torch
import torch.nn as nn
import torch.utils.data as Data
from sklearn.preprocessing import StandardScaler
import numpy as np
import copy
from itertools import zip_longest
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
gpu = True

class Net(nn.Module):
    def __init__(self, feature_len, *net_lens):
        super(Net, self).__init__()
        if net_lens:
            net_lens = list(net_lens)
            sequentials = []
            in_lens = [feature_len] + net_lens
            for in_len, out_len in zip_longest(in_lens, net_lens, fillvalue=1):
                sequentials.append(nn.Linear(in_len, out_len))
                if out_len != 1:
                    sequentials.append(nn.ReLU())
            self.dense = nn.Sequential(*sequentials)
        else:
            self.dense = nn.Sequential(
                nn.Linear(feature_len, 64),
                nn.ReLU(),
                nn.Linear(64, 256),
                nn.ReLU(),
                nn.Linear(256, 512),
                nn.ReLU(),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Linear(256, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
                )
    def forward(self, x):
        return self.dense(x)

def train_net(X_train, Y_train, X_test, Y_test, *net_lens):
    # , train_indexes, test_indexes = perm_rng(X, Y, indexes, 0.1)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    X_train_torch = torch.from_numpy(X_train.astype(np.float32))
    X_test_torch = torch.from_numpy(X_test.astype(np.float32))
    Y_train_torch = torch.from_numpy(Y_train.reshape(-1, 1).astype(np.float32))
    Y_test_torch = torch.from_numpy(Y_test.reshape(-1, 1).astype(np.float32))
    
    train_data = Data.TensorDataset(X_train_torch, Y_train_torch)
    test_data = Data.TensorDataset(X_test_torch, Y_test_torch)
    train_loader = Data.DataLoader(
        dataset=train_data,
        batch_size=64,
        shuffle=True,
        num_workers=0
        )
    test_loader = Data.DataLoader(
        dataset=test_data,
        batch_size=64,
        shuffle=False,
        num_workers=0
        )
    
    net = Net(X_train.shape[1], *net_lens)
    print(net)
    if gpu:
        net = net.to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    train_rate = 0.85 # 验证集比率为0.15
    batch_num = len(train_loader) # 计算总的batch数
    train_batch_num = round(batch_num * train_rate) # 用于训练集的batch数
    train_loss_all = [] # 每轮epoch的训练损失的list
    train_r2_all = [] # 每轮epoch的训练决定系数的list
    train_rmse_all = []
    train_mae_all = []
    val_loss_all = [] # 每轮epoch的验证损失的list
    val_r2_all = [] # 每轮epoch的验证决定系数的list
    val_rmse_all = []
    val_mae_all = []
    best_train_r2 = 0
    best_train_rmse = 0
    best_train_mae = 0
    best_val_r2 = 0 # 最佳r2，如果训练中遇到更好的r2的模型，那么保存这份模型的验证r2和参数
    best_val_rmse = 0
    best_val_mae = 0
    best_model_wts = copy.deepcopy(net.state_dict()) # 最佳模型参数
    best_epoch = 0
    
    ## 训练部分，分为两个阶段，第一阶段为训练阶段，第二阶段为验证阶段
    for epoch in range(2000):
        train_loss = 0 # 训练累计损失
        train_preds = [] # 存放训练集的预报值
        train_obs = [] # 存放训练集对应的观测值
        train_num = 0 # # 训练集累计样本数
        val_loss = 0 # 验证累计损失
        val_preds = [] # 存放验证集的预测值
        val_obs = [] # 存放验证集的观测值
        val_num = 0 # 验证集的累计样本数
        
        ## 开启训练
        for step, (batch_x, batch_y) in enumerate(train_loader):
            ## 如果开启了gpu为True，那么数据会发送到GPU上进行计算
            if gpu:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            ## 第一阶段，训练阶段
            if step < train_batch_num: # 训练
                ## 常规的网络计算、误差反馈
                output = net(batch_x) # 计算得到output 
                loss = criterion(output, batch_y) # 计算损失
                optimizer.zero_grad() # 梯度清零
                loss.backward() # 梯度反向传播
                optimizer.step() # 参数更新
                ## 累加损失、r2值
                train_loss += loss.item() * batch_x.size(0) # 累加batch的训练损失
                train_preds.append(output) # 累计存放batch的训练预测值
                train_obs.append(batch_y.data) # 累计存放batch的训练观测值
                train_num += batch_x.size(0) # 累加训练样本数
            
            ## 第二阶段，验证阶段
            else:
                ## 注意此处不应更新梯度，因此要加上torch.no_grad()
                with torch.no_grad():
                    output = net(batch_x) # 计算output
                    loss = criterion(output, batch_y) # 计算损失
                    val_loss += loss.item() * batch_x.size(0) # 累加验证损失
                    val_preds.append(output) # 累计存放batch的验证预测值
                    val_obs.append(batch_y.data) # 累计存放batch的验证观测值
                    val_num += batch_x.size(0) # 累加验证样本数
        ## 一个epoch完成后，将观测值与预测值进行cat合并
        train_obs = torch.cat(train_obs)
        train_preds = torch.cat(train_preds)
        val_obs = torch.cat(val_obs)
        val_preds = torch.cat(val_preds)
        ## 如果开启了gpu，那么此处需要将数据传回cpu类型
        if gpu:
            train_obs = train_obs.cpu()
            train_preds = train_preds.cpu()
            val_obs = val_obs.cpu()
            val_preds = val_preds.cpu()
        ## 可以直接计算batch的平均损失，因为loss不是tensor
        train_loss_all.append(train_loss / train_num)
        val_loss_all.append(val_loss / val_num)
        ## 对于训练预测值和训练观测值来说是tensor，且训练预测值开启了requires_grad，因此需要先detach再转为numpy
        train_r2_all.append(r2_score(train_obs.numpy(), train_preds.detach().numpy()))
        train_rmse_all.append(np.sqrt(mean_squared_error(train_obs.numpy(), train_preds.detach().numpy())))
        train_mae_all.append(mean_absolute_error(train_obs.numpy(), train_preds.detach().numpy()))
        ## 对于验证预测值来说，没有开启requires_grad，因此可以不用detach
        ## 实际上这里不写numpy方法也可以直接计算
        val_r2_all.append(r2_score(val_obs.numpy(), val_preds.numpy()))
        val_rmse_all.append(np.sqrt(mean_squared_error(val_obs.numpy(), val_preds.numpy())))
        val_mae_all.append(mean_absolute_error(val_obs.numpy(), val_preds.numpy()))
        ## 保存训练中的最佳模型
        if val_r2_all[-1] > best_val_r2:
            best_epoch = epoch
            best_model_wts = copy.deepcopy(net.state_dict())
            best_train_r2 = train_r2_all[-1]
            best_train_rmse = train_rmse_all[-1]
            best_train_mae = train_mae_all[-1]
            best_val_r2 = val_r2_all[-1]
            best_val_rmse = val_rmse_all[-1]
            best_val_mae = val_mae_all[-1]
    ## 完成训练后，让net读取最佳模型参数
    net.load_state_dict(best_model_wts)
    
    test_preds = [] # 累计存放测试集的预测值
    test_obs = [] # 累计存放测试集的观测值
    test_loss = 0 # 累加测试集的损失
    test_num = 0 # 累加测试集的样本数
    ## 开始测试
    for step, (batch_x, batch_y) in enumerate(test_loader):
        ## 如果开启了GPU，那么此处要先把数据发送到GPU上
        if gpu:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        ## 注意测试时不需要计算梯度和反向传播梯度，因此需要使用torch.no_grad()
        with torch.no_grad():
            output = net(batch_x) # 计算output
            loss = criterion(output, batch_y) # 计算loss
            test_preds.append(output) # 累计存放测试集的预测值
            test_obs.append(batch_y.data) # 累计存放测试集的预测值
            test_loss += loss.item() * batch_x.size(0) # 累加测试集损失
            test_num += batch_x.size(0) # 累加测试集的样本数
    test_loss_all = test_loss / test_num # 计算总的测试集平均损失
    test_preds = torch.cat(test_preds) # 将测试集的预测值进行合并
    test_obs = torch.cat(test_obs) # 将测试集的观测值进行合并
    ## 如果开启了GPU，那么此处需要先把观测值和预测值变回cpu类型数据
    if gpu:
        test_preds = test_preds.cpu()
        test_obs = test_obs.cpu()
    ## 观测值和预测值是tensor类型数据，可以直接计算。这里不用numpy方法也可直接计算
    test_r2 = r2_score(test_obs.numpy(), test_preds.numpy())
    test_rmse = np.sqrt(mean_squared_error(test_obs.numpy(), test_preds.numpy()))
    test_mae = mean_absolute_error(test_obs.numpy(), test_preds.numpy())
    
    return dict(
        # train_r2 = best_train_r2,
        # train_rmse = best_train_rmse,
        # train_mae = best_train_mae,
        val_r2 = best_val_r2,
        val_rmse = best_val_rmse,
        val_mae = best_val_mae,
        test_r2 = test_r2,
        test_rmse = test_rmse,
        test_mae = test_mae,
        test_preds = test_preds,
        test_obs = test_obs,
        net=net,
        scaler=scaler
        )