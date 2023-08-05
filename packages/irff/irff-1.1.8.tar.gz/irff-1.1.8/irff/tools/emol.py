#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from os import system, getcwd, chdir,listdir
from os.path import isfile # exists
from irff.irff_np import IRFF_NP
from irff.AtomDance import AtomDance
import argh
import argparse
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.io.trajectory import Trajectory
from ase.io import read
import tensorflow as tf



def get_mole(traj='nm-0.traj'):
    images = Trajectory(traj)
    tframe = len(images)
    x_     = [i for i in range(tframe)]
    e,e_ = [],[]

    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 rcut=None,
                 nn=True)
    
    for i,atoms in enumerate(images):
        energy = atoms.get_potential_energy()
        ir.calculate(atoms)
        e_.append(ir.E)
        e.append(energy)

    emol = np.mean(e) - np.mean(e_)
    print(' * recommended molecular energy is :',emol)



if __name__ == '__main__':
   ''' use commond like ./bp.py <t> to run it
       pb:   plot bo uncorrected 
       t:   train the whole net
   '''
   get_mole()



