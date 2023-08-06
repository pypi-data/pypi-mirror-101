

import re
import string


def _translate(_string, addition=[]):
    
    string_punctuation = string.punctuation
    string_punctuation = string_punctuation.translate(str.maketrans("", "", "."))
    
    if len(addition) == 0:
        translation_str = string_punctuation
    else:
        translation_str = string_punctuation + "".join(addition)
    
    translate_table = str.maketrans("", "", translation_str)
    
    return _string.translate(translate_table)

def _split_formular(formular):
    print(formular)
    formular = _translate(formular)
    ratios = re.compile("[\d+\.]+").findall(formular)
    splited_parts_by_ratios = re.split("|".join(ratios), formular)
    
    parts_with_ratios_list = []
    for ratio, part in zip(ratios+["1"], splited_parts_by_ratios):
        
        if len(part) == 0 or part == " ":
            continue
        
        subparts = re.compile("[A-Z]{1,2}(?![a-z])|[A-Z]{1}[a-z]{1,2}|[A-Z]{3}(?![a-z])|(?<=[N])[WVYP]").findall(part)
        
        if len(subparts) > 1:
            for i,j in enumerate(subparts[:-1]):
                subparts[i] = subparts[i] + "1"
        # print(part)
        subparts[-1] = subparts[-1] + ratio
        
        parts_with_ratios_list += subparts
    
    organic_part = ["".join([ i for i in parts_with_ratios_list if re.compile("[CHNOP](?![a-z])").findall(i)])]
    inorganic_part = [ i for i in parts_with_ratios_list if not re.compile("[CHNOP](?![a-z])").findall(i)]
    if len(organic_part) == 0 or organic_part[0] == "" or organic_part[0] == " ":
        splited_formular_list = inorganic_part
    else:
        splited_formular_list = organic_part + inorganic_part
    
    return splited_formular_list

def _split_formular_to_dict(formular, ratio_sums=[1, 1, 3]):
    formular_list = _split_formular(formular)
    
    site_list = [ {} for i in range(len(ratio_sums)) ]
    
    form_i = 0
    site_i = 0
    ratios = 0
    while form_i < len(formular_list):
        import re
        form = formular_list[form_i]
        ratio_sum = ratio_sums[site_i]
        ratio = re.compile("[\d+\.]+").findall(form)[0]
        ele = form.split(str(ratio))[0]
        ratios += float(ratio)
        site_list[site_i].update({ele:ratio})
        
        if round(ratios, 10) == round(ratio_sum, 10):
            site_i += 1
            ratios = 0
        form_i += 1
    if len(site_list[1]) == 0 or len(site_list[2]) == 0:
        return formular
    return [_sortdict(i) for i in site_list]

def _sortdict(adict,reverse=False):
    keys = list(adict.keys())
    keys.sort(reverse=reverse)
    return {key:adict[key] for key in keys}

def split_formulars_to_dicts(formular_data, *ratio_sums_cands):
    splited_formulars = []
    unsplited_formulars = []
    for i in range(len(formular_data)):
        form = formular_data[i]
        splited_for = _split_formular_to_dict(form)
        
        ratio_sums_cand_i = 0
        
        while isinstance(splited_for, str) and ratio_sums_cand_i < len(ratio_sums_cands):
            splited_for = _split_formular_to_dict(form, ratio_sums_cands[ratio_sums_cand_i])
            ratio_sums_cand_i += 1
        if isinstance(splited_for, list):
            splited_formulars.append(splited_for)
        else:
            unsplited_formulars.append(splited_for)
    return splited_formulars, unsplited_formulars

if __name__ == "__main__":
    
    
    formular_list = _split_formular("MA0.5FA0.6Sn1I3")
    form_i = 0
    site_i = 0
    ratios = 0
    ratio_sums = [1, 1, 3]
    site_list = [ {} for i in range(len(ratio_sums)) ]
    
    while form_i < len(formular_list):
        import re
        form = formular_list[form_i]
        ratio_sum = ratio_sums[site_i]
        ratio = re.compile("[\d+\.]+").findall(form)[0]
        ele = form.split(str(ratio))[0]
        ratios += float(ratio)
        site_list[site_i].update({ele:ratio})
        
        if round(ratios, 10) == round(ratio_sum, 10):
            site_i += 1
            ratios = 0
        form_i += 1

    # import pandas as pd
    # from glob import glob
    
    # target = pd.read_csv(glob("1.csv")[0], encoding="gbk").to_numpy()
    # formulars = target[:, 0].tolist()
    
    # new_formulars = [ _split_formular(formular) for formular in formulars]
    
    # _split_formular("CH6N)Y)I3")
    
    # for formular in formulars:
    #     _split_formular(formular)
    
    # pd.DataFrame(new_formulars).to_csv("1_2.csv")
    
# =============================================================================
#     # a = "CH3CHGuaBA0.05FA0.7885Cs0.1615PbI2.4Br0.6K"
#     # a = "GuaSnI3"
#     # a = "KPbI3"
#     a = "MAPb12Cl12"
#     # a = "C2H6PPbI3"
#     
#     
#     a = _translate(a)
#     
#     b = re.compile("[\d+\.]+").findall(a)
#     
#     d = "|".join(b)
#     
#     c = re.split(d, a)
#     
#     f = []
#     
#     for number, form in zip(b+["1"], c):
#         
#         if len(form) == 0:
#             continue
#         
#         e = re.compile("[A-Z]{1,2}(?![a-z])|[A-Z]{1}[a-z]{1,2}|[A-Z]{3}(?![a-z])").findall(form)
#         
#         if len(e) > 1:
#             for i,j in enumerate(e[:-1]):
#                 e[i] = e[i] + "1"
#         e[-1] = e[-1] + number
#         f += e
#     
#     g = "".join([ i for i in f if re.compile("[CHNOPS](?![a-z])").findall(i)])
#     
#     h = [ i for i in f if not re.compile("[CHNOPS](?![a-z])").findall(i)]
#     
#     i = [g]+h
# =============================================================================
    
    # a = _translate(a)
    
    # b = re.compile("[\d+\.]+").findall(a)
    
    # sub_a = a
    
    # subes = []
    
    # for n in b[::-1]:
        
        # sub_a = sub_a.split(n)[0]
        
        # print(f"sub_a: {sub_a}")
        
        # sub_a_splits = re.compile("(?<=\d)[A-Z]{1,2}[a-z]*|(?<=[a-z])[A-Za-z]{1,2}|[A-Za-z]{1,2}").findall(sub_a)
        # sub_a_splits = re.compile("(?<=\d)[A-Z]{1,2}[a-z]*|(?<=[a-z])[A-Z]{1}[a-z]{0,2}|[K]{1}|[A-Z]{1}[a-z]{1,2}|[A-Z]{1,2}").findall(sub_a)
        
        # tmp = sub_a_splits[-1]
        
        # tmp = str(tmp) + str(n)
        
        # print(sub_a_splits)
        
        # print(tmp)
        
        # subes.append(tmp)
    
    # remained_str = str.maketrans("", "", "".join(subes))
    # c = a.translate(remained_str)
    
    # d = re.compile("")
        
        # if len(sub_a_splits) == 0:
            # sub_a_splits = re.compile("[A-Za-z]+").findall(sub_a)
        
        # tmp = re.compile("(?<=\d)[A-Za-z]+").findall(sub_a)
        
        # if len(tmp) > 0: tmp = tmp[-1]
        
        # tmp = str(tmp) + str(n)
        
        # print(tmp)
        
    
    
    # pattern = re.compile("([A-Z][a-z][a-z]|[A-Z][a-z]|[B,N,C,O,F,I,V,K]|[A-Z][A-Z])")
    # pattern = re.compile("(\d*\.\d*)")
    # pattern = re.compile("[\d+\.]+")
    
    # data = []
    
    # for formular in formulars:
        
    #     formular = _translate(formular)
        
    #     numbers = pattern.findall(formular)
        
    #     for number in numbers:
            
    #         isoformular = number.split(formular)[0]
        
        # data.append(alphbet)
    
    
    # print(data[3])
    
    
    # formular3 = formulars[18]
    
    # formular3 = _translate(formular3)
    
    # numbers = pattern.findall(formular3)
    
    # numbers_split = "|".join(numbers)
    
    # print(re.split(numbers_split, formular3))
    
    # for number in numbers:
            
        # isoformular = formular3.split(number)[0]
    
    # a = formulars[3]
    
    # a = _translate(a)
    
    # table = str.maketrans("", "", string.punctuation)
    # b = a.translate(table) + "Gua"
    
    # pattern = re.compile("([A-Z][a-z][a-z]|[A-Z][a-z]|[A-Z][A-Z]|[A-Z])")
    # c = pattern.findall(b)
