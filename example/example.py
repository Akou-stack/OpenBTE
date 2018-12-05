from openbte.material import *
from openbte.geometry import *
from openbte.solver import *
from openbte.plot import *


#mat = Material(model='gray',n_theta=6,n_phi=48,kappa=100.0,mfps=[1e-10])

#geo = Geometry(type='bulk',lx=1,ly=1,
#                    porosity=0.25,step=0.1,shape='square')

sol = Solver(max_bte_iter = 1,multiscale=False)
