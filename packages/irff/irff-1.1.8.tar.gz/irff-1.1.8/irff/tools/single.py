#!/usr/bin/env python
# -*- coding: utf-8 -*-
from irff.dft.SinglePointEnergy import SinglePointEnergies
from ase.io import read


if __name__ == '__main__':
   SinglePointEnergies('swing.traj',label='nm2-s',frame=50,cpu=4)




