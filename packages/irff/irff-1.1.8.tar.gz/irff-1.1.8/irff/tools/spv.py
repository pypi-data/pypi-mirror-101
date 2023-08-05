#!/usr/bin/env python
from __future__ import print_function
import argh
import argparse
from os import environ,system,getcwd
from os.path import exists
from ase.io import read,write
from ase.io.trajectory import Trajectory,TrajectoryWriter
from ase.calculators.singlepoint import SinglePointCalculator
from ase import Atoms
import matplotlib.pyplot as plt
import numpy as np
from irff.irff import IRFF
from irff.irff_np import IRFF_NP
from irff.mpnn import MPNN
from irff.ColData import ColData
from irff.dft.CheckEmol import check_emol


def supervise(direcs={'md':'md.traj'},efunc=3,fm=1,batch_size=50,nn=True):
    ffield = 'ffield.json' if nn else 'ffield'

    rn = MPNN(libfile=ffield,
              direcs=direcs,
              dft='siesta',
              opt=[],optword='nocoul',
              batch_size=batch_size,
              clip_op=False,
              InitCheck=False,
              nn=nn,
              bo_layer=[4,1],
              bf_layer=[6,2],
              be_layer=[3,1],
              EnergyFunction=efunc,
              MessageFunction=fm) 
    molecules = rn.initialize()
    rn.session(learning_rate=1.0e-10,method='AdamOptimizer')

    db_  = rn.get_value(rn.diffb)  # r<rmax that bo shuld be ...
    da_  = rn.get_value(rn.diffa)  # r>rmax that bop shuld be zero ...
    de_  = rn.get_value(rn.diffe)  # at equlibrium r that bo shuld be ...

    for bd in db_:
        print(bd,db_[bd],da_[bd],de_[bd])




if __name__ == '__main__':
    ''' use commond like ./cp.py scale-md --T=2800 to run it'''
    direcs = {'c2h4-0':'data/c2h4-0.traj',
              'c2h6-0':'data/c2h6-0.traj',
              'c2h6-1':'data/c2h6-1.traj',
              # 'fox-00': 'data/fox-0.traj',
              'h2o4-0':'data/h2o4-0.traj',
              'ch42-0':'data/ch42-0.traj',
              'n22-0':'data/n22-0.traj',
              'noco-s1':'data/noco-s1.traj',
              }
    
    getdata = ColData()
    strucs = ['o22', 'h22', 'c22','co2',
              'ch32', # 'nh3ch3','ch3h2o',
              'nh22','nh32',
              'hco','h2o2',#'h2o3',
              # 'nm',# 'nml','nml-7','nml-3',
              'noco','noco3',
               ] # 
              # 'nml-14',# 'nml-10',
              # 'fox',
    
    batchs = {'others':60,
              'nm':80,'h2o2':200,
              # 'co2':90,'noco':90,
              }
    
    for mol in strucs:
        b = batchs[mol] if mol in batchs else batchs['others']
        trajs = getdata(label=mol,batch=b)
        direcs.update(trajs)

    supervise(direcs=direcs)

   
