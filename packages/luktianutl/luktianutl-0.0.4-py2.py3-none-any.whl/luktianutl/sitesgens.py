#version 2

from collections import Iterable
import numpy as np
import itertools, psutil, os, pickle, time

def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m"%'   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
    print(bar, end='', flush=True)

def iter_drop_n(iterable, n=1, remnant=0):
    
    if isinstance(iterable, Iterable):
        
        for i in range(0, len(iterable), n):
            if len(iterable[i+n:]) < remnant:
                break
            yield iterable[i:i+n], iterable[i+n:]


def iter_split_n(iterable, n=1, remnant=0):
    
    if isinstance(iterable, Iterable):
        
        for i in range(0, len(iterable), n):
            if len(iterable[i+n:]) < remnant:
                break
            yield iterable[:i+n], iterable[i+n:]

def cross_list2dict(a, b):
    results = { a[i]: b[i] for i in range(len(a))}
    return results

class SiteObj:
    
    def __init__(self, **params):
        
        self.iterable = params.get("iterable", [])  #list
        self.ratio_sum = params.get("ratio_sum", 1)
        self.site_number = params.get("site_number", 2)
        self.step = params.get("step", 0.1)
        self.ratio_range = params.get("ratio_range", [0, self.ratio_sum])
        self.restraints = params.get("restraints", [])  #list or dict
        self.base_atoms = []
        self.base_ratios = []
        self.combined_atoms = []
        self.combined_atoms_length = 0
        self.combined_ratios = []
        self.combined_ratios_length = 0
        self.combined_sites = []
        self.combined_sites_length = 0
        self.writeIO = False #future
        self.prune_atom = True
        self._fill_base()
        if self.ratio_sum != self.ratio_range[1]:
            self.ratio_range[1] = self.ratio_sum
    
    @property
    def get_params(self):
        return dict(
            iterable=self.iterable,
            site_number=self.site_number,
            step=self.step,
            ratio_sum = self.ratio_sum,
            ratio_range=self.ratio_range,
            restraints=self.restraints,
            base_atoms=self.base_atoms,
            base_ratios=self.base_ratios,
            combined_atoms_length=self.combined_atoms_length,
            combined_ratios_length=self.combined_ratios_length,
            combined_sites_length=self.combined_sites_length
            )
    
    @property
    def get_combinations(self):
        return dict(
            combined_atoms=self.combined_atoms,
            combined_ratios=self.combined_ratios,
            combined_sites=self.combined_sites
            )
    
    def _fill_base(self):
        if not self.ratio_range:
            self.ratio_range = [0, 1]
        self.base_atoms = []
        self.base_ratios = []
        if isinstance(self.restraints, dict):
            self.base_atoms = list(self.restraints.keys())
            self.base_ratios = list(self.restraints.values())
        elif isinstance(self.restraints, list):
            self.base_atoms = self.restraints
            self.base_ratios = [ self.ratio_range for i in range(len(self.base_atoms))]
        if self.base_atoms:
            for base_atom in self.base_atoms:
                if base_atom in self.iterable:
                    self.iterable.pop(self.iterable.index(base_atom))
    
    def combine(self):
        combined_atoms = []
        times = 1000
        ratio_sum = times * self.ratio_sum
        _step = times * self.step
        if self.base_atoms:
            meshes = []
            #有base_atoms,肯定必有base_ratios
            for index, (prefix, ramnant) in enumerate(iter_drop_n(self.base_atoms)):
                combined_ratios = [ np.array(self.base_ratios[index]) * times ]
                combined_ratios += [np.array(self.ratio_range) * times \
                                    for ran in range(self.site_number-1) ]
                combined_atoms_iter, meshes_iter = self._combine_atoms_ratios(prefix, 
                                                                 ramnant+self.iterable, 
                                                                 combined_ratios, 
                                                                 self.site_number-1, 
                                                                 ratio_sum, _step)
                combined_atoms += combined_atoms_iter
                meshes.append(meshes_iter)
                self._combine_sites(combined_atoms_iter, meshes_iter, warm=True)
            meshes = np.concatenate(meshes, axis=0)
        else:
            #没有base_atoms, 正常生成
            prefix = None
            combined_ratios = [ np.array(self.ratio_range) * times \
                                for i in range(self.site_number)]
            combined_atoms, meshes = self._combine_atoms_ratios(prefix,
                                                   self.iterable,
                                                   combined_ratios,
                                                   self.site_number,
                                                   ratio_sum, _step)
            self._combine_sites(combined_atoms, meshes, warm=False)
        self.combined_atoms = combined_atoms
        self.combined_atoms_length = len(combined_atoms)
        self.combined_ratios = meshes
        self.combined_ratios_length = len(self.combined_ratios)
        return self
    
    def _combine_atoms_ratios(self, prefix, iterable, combined_ratios, site_number, ratio_sum, _step):
        if prefix:
            combined_atoms = [prefix+list(atom) for atom in itertools.combinations(iterable, site_number)]
        else:
            combined_atoms = [list(atom) for atom in itertools.combinations(iterable, site_number)]
        meshes = [ np.linspace(ran[0], ran[1], int((ran[1]-ran[0])/_step)+1) \
                  for ran in combined_ratios ]
        meshes = np.meshgrid(*meshes)
        meshes = np.array([ i.ravel() for i in meshes ]).T
        meshes = meshes[np.where(np.sum(meshes, axis=1) == ratio_sum)]
        return combined_atoms, meshes/1000
    
    def _combine_sites(self, combined_atoms, combined_ratios, warm):
        if not warm:
            self.combine_sites = []
            self.combined_sites_length = 0
        meshed_indexes = np.meshgrid(list(range(len(combined_atoms))), list(range(len(combined_ratios))))
        meshed_indexes = [i.ravel() for i in meshed_indexes]
        meshed_indexes = np.array(meshed_indexes).T
        self.combined_sites_length += len(meshed_indexes)
        for atom_i, ratio_i in meshed_indexes:
            if self.writeIO:
                pass
            else:
                site = cross_list2dict(combined_atoms[atom_i], combined_ratios[ratio_i])
                if self.prune_atom and isinstance(self.restraints, dict):
                    prune_flag = False
                    for site_atom, site_ratio in site.items():
                        if site_atom in self.restraints.keys():
                            r_range = self.restraints[site_atom]
                            if site_ratio < r_range[0] or site_ratio > r_range[1]:
                                prune_flag = True
                                break
                    if prune_flag:
                        pass
                    else:
                        self.combined_sites.append(site)
                else:
                    self.combined_sites.append(site)
        if self.prune_atom:
            self.combined_sites_length = len(self.combined_sites)
        return self
        

def combines(*siteobjs, silent=False, pause=True, save="memory", directory=None, mem_percent=0.75):
    for siteobj in siteobjs:
        if not siteobj.get_combinations["combined_sites"]:
            siteobj.combine()
    combinations = [ siteobj.get_combinations["combined_sites"] for siteobj in siteobjs]
    meshed_indexes = [ list(range(siteobj.get_params["combined_sites_length"])) for siteobj in siteobjs]
    if save == "memory":
        meshed_indexes = np.meshgrid(*meshed_indexes)
        meshed_indexes = [i.ravel() for i in meshed_indexes]
        meshes_length = len(meshed_indexes[0])
        if pause:
            print(meshes_length)
        else:
            round_ = 0
            formulars = []
            for index_tuple in zip(*meshed_indexes):
                round_ += 1
                if not silent:
                    if round_ % 1000:
                        print(f"{round_}/{meshes_length}")
                formular = []
                for i in range(len(siteobjs)):
                    formular.append(combinations[i][index_tuple[i]])
                formulars.append(formular)
            return formulars
    elif save == "disk":
        file_count = 0
        max_percent = 0
        formulars = []
        mem_total = psutil.virtual_memory().total / 1024**3
        round_ = 0
        meshes_length = len(meshed_indexes[0]) * len(meshed_indexes[1]) * len(meshed_indexes[2])
        for a_i in meshed_indexes[0]:
            for b_i in meshed_indexes[1]:
                for c_i in meshed_indexes[2]:
                    round_ += 1
                    mem_used = psutil.virtual_memory().used / 1024**3
                    process_percent = round((round_ / meshes_length) * 100, 3)
                    if not silent:
                        if process_percent > max_percent:
                            max_percent = process_percent
                            process_bar(process_percent/100, total_length=15)
                        #     print(f"{process_percent}", flush=True, end=" ")
                        # if round(mem_used) % 5 == 0:
                        #     print(f"mem used: {mem_used}/{mem_total}", flush=True, end=" ")
                    formular = [combinations[0][a_i], combinations[1][b_i], combinations[2][c_i]]
                    formulars.append(formular)
                    if mem_used > mem_total * mem_percent:
                        if directory is None:
                            directory = "./"
                        file_path = os.path.join(directory, f"formulars{file_count}.pkl")
                        with open(file_path, "wb") as f:
                            pickle.dump(formulars, f)
                        formulars.clear()
                        file_count += 1
        if len(formulars) > 0:
            if directory is None:
                directory = "./"
            file_path = os.path.join(directory, f"formulars{file_count}.pkl")
            with open(file_path, "wb") as f:
                pickle.dump(formulars, f)
            formulars.clear()
            file_count += 1
        
