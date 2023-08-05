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


def deb_energies(i=0,j=1,ffield='ffield.json',nn='T',traj='md.traj'):
    # atoms = read(traj)
    # ao = AtomDance(atoms)
    # images = ao.stretch([[i,j]],nbin=50,traj=False)
    images =  Trajectory(traj)
    atoms=images[0]
    
    nn_=True if nn=='T'  else False
    ir = IRFF_NP(atoms=atoms,
                 libfile=ffield,
                 rcut=None,
                 nn=nn_)

    ir.calculate_Delta(atoms)
    natom = ir.natom
   
    for i_,atoms in enumerate(images):
        positions = atoms.positions        
        ir.calculate(atoms)
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        print('%d Energies: ' %i_,
              '%12.4f ' %ir.E,
              'Ebd: %6.4f' %ir.Ebond,
              'Eov: %6.4f' %ir.Eover,
              'Eang: %6.4f' %ir.Eang,
              'Eun: %6.4f' %ir.Eunder,
              'Etor: %6.4f' %ir.Etor,
              'Ele: %6.4f' %ir.Elone,
              'Evdw: %6.4f' %ir.Evdw,
              'Ehb: %6.4f' %ir.Ehb)



if __name__ == '__main__':
   deb_energies()


