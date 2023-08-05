#!/usr/bin/env python
# coding: utf-8
import numpy as np
from ase.optimize import BFGS
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.io.trajectory import Trajectory,TrajectoryWriter
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff_np import IRFF_NP
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from irff.AtomDance import AtomDance


def deb_energies(ffield='ffield.json',nn='T',traj='md.traj'):
    # atoms = read(traj)
    # ao = AtomDance(atoms)
    # images = ao.stretch([[i,j]],nbin=50,traj=False)
    images =  Trajectory(traj)
    atoms = images[0]
    natom = len(atoms) 
    
    nn_=True if nn=='T'  else False
    ir = IRFF_NP(atoms=atoms,
                 libfile=ffield,
                 rcut=None,
                 nn=nn_)

    ir.calculate_Delta(atoms)
    natom = ir.natom
    energies = []
   
    for i_,atoms in enumerate(images):
        positions = atoms.positions
        ir.calculate(atoms)
        energies.append(ir.E)
        ebond = ir.ebond

        if i_>0:              ###########
           dE = energies[-2] - energies[-1]
           dE_ = abs(dE)
           if dE_>=0.2:
              print('%d Energies: ' %i_,'%9.4f ' %ir.E,'dE: %6.4f' %dE_)
              ir.calculate(images[i_-1])
              ebond_ = ir.ebond
              for i in range(natom-1):
                  for j in range(i+1,natom):
                      de = abs(ebond[i][j]-ebond_[i][j])
                      if de>=0.2:
                         # print(i,j,ebond[i][j],ebond_[i][j])
                         print('%d %d: ' %(i,j),
                               '%12.4f ' %ir.E,
                               'Ebd: %8.4f' %ir.Ebond,
                               'Eov: %8.4f' %ir.Eover,
                               # 'eov: %8.4f' %ir.eover[1],
                               'soi: %6.4f' %ir.so[i],
                               'soj: %6.4f' %ir.so[j],
                               'Dlpci: %6.4f' %ir.Delta_lpcorr[i],
                               'Dlpcj: %6.4f' %ir.Delta_lpcorr[j],
                               'otrm1: %6.4f' %ir.otrm1[i],
                               'otrm2: %6.4f' %ir.otrm2[i],
                               #'Eang: %8.4f' %ir.Eang,
                               'Eun: %8.4f' %ir.Eunder,
                               #'Etor: %8.4f' %ir.Etor,
                               #'Ele: %8.4f' %ir.Elone,
                               #'Evdw: %8.4f' %ir.Evdw,
                               #'Ehb: %8.4f' %ir.Ehb
                               )


if __name__ == '__main__':
   deb_energies()


