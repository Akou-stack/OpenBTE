Material
===================================


Fourier model
-----------------------------------

OpenBTE features a 3D solver of diffusive heat conduction solved on unstructured grids. This model is used as a first-guess to OpenBTE and can be used as a stand-alone model. To create the relative material model, simply use

.. code-block:: python

   Material(model='fourier',kappa=130)

where ``kappa`` is the bulk thermal conductivity.

It is also possible to define an anisotropic thermal conductivity 

.. code-block:: python

   Material(model='fourier',kappa_xx=100,kappa_yy=150)

Gray model approximation
-----------------------------------

Within the gray model, we assume single MFP-materials. In light of new first-principles developments, this model might not be needed. However, it can be useful to understand heat transport regimes and trends. To create ``material.npz`` no prior file is needed in this case, but only two options, e.g the mean-free-path (in m) and the bulk thermal conductivity. Here is an example:

.. code-block:: python

   Material(model='gray2DSym',mfp=1e-8,kappa=130)


There are three material models associated with this method

* ``model='gray3D'``: three-dimensional domain 

* ``model='gray2DSym'``: three-dimensional domain with infinite thickness

* ``model='gray2D'``: two-dimensional domain


Mean-free-path approximation
-----------------------------------

This method estimates kappa given only the cumulative thermal conductivity. It assumes isotropic distribution, therefore use it cautiously. The BTE to solve is

* ``model='mfp3D'``: three-dimensional domain

* ``model='mfp2DSym'``: three-dimensional domain with infinite thickness

* ``model='mfp2D'``: two-dimensional domain


The material file can be created by running

.. code-block:: python

   Material(model=<('mfp3D'),'mfp2DSym','mfp2D'>)

provided the file ``mfp.npz`` is in your current directory. This file must contain the following information

.. table:: 
   :widths: auto
   :align: center

   +--------------------------+-------------+--------------------------------------------------------------------------+-------------------------------------------+
   | **Item**                 | **Shape**   |       **Symbol [Units]**                                                 |    **Name**                               |
   +--------------------------+-------------+--------------------------------------------------------------------------+-------------------------------------------+
   | ``mfp``                  |  N          |   :math:`\Lambda` [:math:`m`]                                            | Mean Free Path                            |
   +--------------------------+-------------+--------------------------------------------------------------------------+-------------------------------------------+
   | ``Kacc``                 |  N          |   :math:`\alpha` [:math:`\mathrm{W}\mathrm{m}^{-1}\textrm{K}^{-1}`]      | Cumulative thermal conductivity           |
   +--------------------------+-------------+--------------------------------------------------------------------------+-------------------------------------------+
   
Once you have your dictionary with proper information, you can simplt save the ``mfp.npz`` file by typing

.. code-block:: python

   from openbte.utils import *

   save_data('mfp',{'mfp':mfp,'Kacc':Kacc})



Relaxation time approximation
-----------------------------------

Within the temperature formulation, the BTE under th relaxation time approximation reads as

.. math::

   \mathbf{v}_\mu\cdot\nabla T_\mu^{(n)} + T_\mu^{(n)} = T_L

where

.. math::
    
   T_L = \left[ \sum_l \frac{C_l}{\tau_l} \right]^{-1} \sum_\nu \frac{C_\nu}{\tau_\nu} T_\nu.

The scattering times are defined as  :math:`\tau_\nu^{-1} = W_{\nu\nu}`, where :math:`\mathbf{W}` is the scattering matrix. Terms :math:`T_\mu`  are the phonon pseudo temperatures. Upon convergence, the heat flux is computed with :math:`\mathbf{J} = \mathcal{V}^{-1} N^{-1} \sum_\mu C_\mu \mathbf{v}_\mu T_\mu`, where :math:`\mathbf{v}_\mu` is the group velocity and :math:`C_\mu` is the heat capacity; the latter is defined as :math:`C_\mu = k_B \eta_\mu \left(\sinh \eta_\mu \right)^{-2}`, where :math:`\eta_\mu = \hbar \omega_\mu/k_B/T_0/2`. Adiabatic boundary conditions are generally applied with :math:`T_{\mu^-} = \sum_{\nu^+} R_{\mu^-\nu^+} T_{\nu^+}`, where :math:`R_{\mu^-\nu^+}` is a reflection matrix, :math:`T_{\mu^-}` (:math:`T_{\mu^+}`) is related to incoming (outgoing) phonons. Currently, OpenBTE employes a crude approximation, i.e. all phonons thermalize to a boundary temperature, whose values is obtained by ensuring zero total incident flux [`Landon (2014)`_]. Within this approach, the reflection matrix reads as :math:`R_{\mu^-\nu^+}=-C_\nu\mathbf{v}_\nu \cdot \hat{\mathbf{n}} \left[\sum_{k^-} C_{k^-} \mathbf{v}_{k^-}\cdot \hat{\mathbf{n}} \right]^{-1}`.

Creating ``rta.npz``
###############################################

The first step for solving the RTA-BTE is to create the file ``rta.npz``. This file is an ``gzip`` file that must have the following items:

.. table:: 
   :widths: auto
   :align: center

   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+
   | **Item**       | **Shape**   |       **Symbol [Units]**                                                 |    **Name**              |
   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+
   | ``tau``        |  N          |   :math:`\tau` [:math:`s`]                                               | Scattering time          |
   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+
   | ``C``          |  N          |   :math:`C` [:math:`\mathrm{W}\mathrm{s}\textrm{K}^{-1}\textrm{m}^{-3}`] | Specific Heat capacity   |
   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+
   | ``v``          |  N x 3      |   :math:`\mathbf{v}` [:math:`\mathrm{m}\textrm{s}^{-1}`]                 | Group velocity           |
   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+
   | ``kappa``      |  3 x 3      |   :math:`\kappa` [:math:`\mathrm{W}\textrm{K}^{-1}\textrm{m}^{-1}`]      | Thermal conductivity     |
   +----------------+-------------+--------------------------------------------------------------------------+--------------------------+


Each item must be a ``numpy`` array with the prescribed ``shape``. The thermal conductivity tensor is given by :math:`\kappa^{\alpha\beta} = \mathcal{V}^{-1}N_0^{-1}\sum_{\mu} C_\mu  v_\mu^{\alpha} v_\mu^{\beta} \tau_\mu`, where :math:`\mathcal{V}` is the volume of the unit cell and :math:`N_0` is the numbre of wave vectors. 

With ``rta.npz`` in your current directory, ``material.npz`` can be generated simply with

.. code-block:: python

   Material(model=<('rta3D'),'rta2DSym','rta2D'>)


The RTA-BTE has three material models:

* ``model='rta3D'``: three-dimensional domain

* ``model='rta2DSym'``: three-dimensional domain with infinite thickness

* ``model='rta2D'``: two-dimensional domain


Interface with AlmaBTE
###############################################

AlmaBTE_ is a popular package that compute the thermal conductivity of bulk materials, thin films and superlattices. OpenBTE is interfaced with AlmaBTE for RTA calculations via the script ``almabte2openbte.py``. 

Assuming you have ``AlmaBTE`` in your current ``PATH``, this an example for ``Si``.

- Download Silicon force constants from AlmaBTE's database_.

  .. code-block:: bash

   wget https://almabte.bitbucket.io/database/Si.tar.xz   
   tar -xf Si.tar.xz && rm -rf Si.tar.xz  

- Compute bulk scattering time with AlmaBTE.

  .. code-block:: bash

   echo "<singlecrystal> 
   <compound name='Si'/>
   <gridDensity A='8' B='8' C='8'/>
   </singlecrystal>" > inputfile.xml
   
   VCAbuilder inputfile.xml
   phononinfo Si/Si_8_8_8.h5
    
- A file named ``Si_8_8_8_300K.phononinfo`` is in your current directory. The file ``rta.npz`` can then be created with 

  .. code-block:: bash

     AlmaBTE2OpenBTE Si_8_8_8_300K.phononinfo

- Using OpenBTE command line interface, the ``material`` may be created with

  .. code-block:: bash

     OpenBTE $'Material:\n model: rta2DSym'


.. _Deepdish: https://deepdish.readthedocs.io/
.. _`Wu et al.`: https://www.sciencedirect.com/science/article/pii/S0009261416310193?via%3Dihub
.. _`Fugallo et al. (2013)`: https://arxiv.org/pdf/1212.0470.pdf
.. _`Romano (2020)`: https://arxiv.org/abs/2002.08940
.. _Phono3py: https://phonopy.github.io/phono3py/
.. _`Chaput (2013)`: https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.110.265506?casa_token=BTUhHjniziYAAAAA%3AGw4C_2ql3cGvy6zwNe_38m7vz130fV7LYZMxrnIt_FSbmQauL3fczg5QT1b0EXTU39nYWEHYUHbv
.. _`Landon (2014)`: https://dspace.mit.edu/handle/1721.1/92161
.. _`Vazrik et al. (2017)` : https://arxiv.org/pdf/1711.07151.pdf
.. _`Cepellotti et al. (2016)` : https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.041013
.. _AlmaBTE: https://almabte.bitbucket.io/
.. _database: https://almabte.bitbucket.io/database/










Full Scattering Operator
----------------------------------------------


In many cases the relaxation time approximation (RTA) is not enough and the full scattering operator must be used. OpenBTE employes the following iterative scheme

.. math::

   \mathbf{F}_\mu\cdot\nabla T_\mu^{(n)} + T_\mu^{(n)} = \sum_\nu B_{\mu\nu}T_\nu^{(n-1)}

where

.. math::
    
   B_{\mu\nu} = \delta_{\mu\nu} - W_{\mu\nu}W_{\mu\mu}^{-1}.

The term :math:`\mathbf{W}` is the scattering matrix and :math:`T_\mu` the phonon pseudo temperatures. Upon convergence, the heat flux is computed with :math:`\mathbf{J} = \mathcal{V}^{-1} N^{-1} \sum_\mu C_\mu \mathbf{v}_\mu T_\mu`, where :math:`\mathbf{v}_\mu` is the group velocity and :math:`C_\mu` is the heat capacity; the latter is defined as :math:`C_\mu = k_B \eta_\mu \left(\sinh \eta_\mu \right)^{-2}`, where :math:`\eta_\mu = \hbar \omega_\mu/k_B/T_0/2`. Adiabatic boundary conditions are generally applied with :math:`T_{\mu^-} = \sum_{\nu^+} R_{\mu^-\nu^+} T_{\nu^+}`, where :math:`R_{\mu^-\nu^+}` is a reflection matrix, :math:`T_{\mu^-}` (:math:`T_{\mu^+}`) is related to incomng (outgoing) phonons. Currently, OpenBTE employes a crude approximation, i.e. all phonons thermalize to a boundary temperature, whose values is obtained by ensuring zero total incident flux [`Landon (2014)`_]. Within this approach, the reflection matrix reads as :math:`R_{\mu^-\nu^+}=-C_\nu\mathbf{v}_{\nu^-} \cdot \hat{\mathbf{n}} \left[\sum_{k^-} C_{k^-} \mathbf{v}_{k^-}\cdot \hat{\mathbf{n}} \right]^{-1}`.

Creating ``full.npz``
###############################################

The first step for solving the BTE with the full collision operator is to create the file ``full.npz``. This file is an ``gzip`` file that must have the following items:

.. table:: 
   :widths: auto
   :align: center

   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | **Item**      | **Shape**   |       **Symbol [Units]**                                          |    **Name**         |
   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | ``W``         |  N x N      |  :math:`W` [:math:`\textrm{W}\textrm{K}^{-1}`]                    | Scattering operator |
   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | ``C``         |  N          | :math:`C` [:math:`\mathrm{W}\textrm{K}^{-1}\textrm{s}`]           | Heat capacity       |
   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | ``v``         |  N x 3      | :math:`\mathbf{v}` [:math:`\mathrm{m}\textrm{s}^{-1}`]            | Group velocity      |
   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | ``alpha``     |  1 x 1      | :math:`\mathcal{V} N` [:math:`\mathrm{m}^{3}`]                    | Normalization factor|
   +---------------+-------------+-------------------------------------------------------------------+---------------------+
   | ``kappa``     |  3 x 3      | :math:`\kappa` [:math:`\mathrm{W}\textrm{K}^{-1}\textrm{m}^{-1}`] | Thermal conductivity|
   +---------------+-------------+-------------------------------------------------------------------+---------------------+



Each item must be a ``numpy`` array with prescribed ``shape``. We recommend using the package Deepdish_ for IO ``hdf5`` operations. Within this formalism the thermal conductivity tensor is given by :math:`\langle S^{\alpha}|W^{\sim1}|S^{\beta}\rangle`, where :math:`S^\alpha_\mu = C_\mu v^\alpha_\mu` and :math:`\sim1` is the Moore-Penrose inverse. Note that we use the notation :math:`< f | g | f > = N^{-1} \mathcal{V}^{-1} \sum_{\mu\nu} f_\mu g_{\mu\nu} f_\nu` .To check the consistencty of the data populating ``full.npz``, you may want to run this script:

.. code-block:: python

   import numpy as np
   from openbte.utils import *

   data = load_data('full')
   S = np.einsum('i,ij->ij',data['C'],data['v'])
   kappa = np.einsum('i,ij,j->ij',S,np.linalg.pinv(data['W']),S)/data['alpha']

   assert(np.allclose(kappa,data['kappa']))

Of course, the best practice is to have the ``kappa`` populating ``full.npz`` generated by the other items and compare it with the intended value.

With ``full.npz`` in your current directory, ``material.npz`` can be generated simply with

.. code-block:: python

   Material(model='full')

The ``Material`` will ensure that the scattering operator :math:`W` is energy conserving, i.e. :math:`\sum_\mu W_{\mu\nu} = \sum_\mu W_{\mu\nu} = 0`. This condition is applied by using the method of Lagrange multipliers [`Romano (2020)`_]


Interface with Phono3py (Experimental)
###############################################

Phono3py_ calculates the bulk thermal conductivity using the full scattering matrix defined here [`Chaput (2013)`_]. In order to be used in tandem with OpenBTE, Phono3py must be run with the following options ``--reducible-colmat --write-lbte-solution --lbte``. Once Phono3py is solved, the ``full.npz`` is created by


.. code-block:: bash

   phono3pytoOpenBTE unitcell_name nx ny nz 

where ``unitcell_name`` is the file of your unit cell and ``nx ny nz`` is the reciprical space discretization.

Here is an example assuming you have a working installation of Phono3py:

.. code-block:: bash

   git clone https://github.com/phonopy/phono3py.git

   cd phono3py/examples/Si-PBEsol

   phono3py --dim="2 2 2" --sym-fc -c POSCAR-unitcell

   phono3py --dim="2 2 2" --pa="0 1/2 1/2 1/2 0 1/2 1/2 1/2 0" -c POSCAR-unitcell --mesh="8 8 8"  --reducible-colmat --write-lbte-solution  --fc3 --fc2 --lbte --ts=100

   Phono3py2OpenBTE POSCAR-unitcell 8 8 8 

Note that ``rta.npz`` is also created in the case you want to use a RTA model.   

Conversion from other collision matrix definitions
##################################################

If you are familiar with the form of the scattering operator, :math:`A` (in :math:`\textrm{s}^{-1}`), given by Eq. 13 in [`Fugallo et al. (2013)`_] , you may use the following conversion :math:`W_{\mu\nu} = A_{\mu\nu}\hbar\omega_\mu \hbar\omega_\nu  k_B^{-1}T_0^{-2}` [`Romano (2020)`_], where :math:`\hbar\omega_\mu` is the energy of the :math:`\mu`-labelled phonons (:math:`\mu` colectively represents wave vector and polatization), :math:`k_B` is the Boltzmann constant, :math:`T_0` is the reference temperature. Another definition of the scattering matrix, which we refer to as :math:`\mathbf{W}^v`, can be found in [`Vazrik et al. (2017)`_]. In this case the conversion is :math:`W_{\mu\nu} = W^v_{\mu\nu}C_\nu`. Lastly, from the symmetrized matrix :math:`\tilde{\Omega}` defined in [`Cepellotti et al. (2016)`_], we have :math:`W_{\mu\nu}=\tilde{\Omega}_{\mu\nu}\sqrt{C_\nu}\sqrt{C_\mu}`. This symmetrized matrix concides with the one defined here [`Chaput (2013)`_].

Two-dimensional materials
###############################################

For two-dimensional materials, a thickness :math:`L_c` is used for first-principles calculations. When reporting the thermal conductivity, however, and effective thickness, :math:`h`, is used. In practice, the volume of the unit cell must be computed as :math:`\mathcal{V} = \mathcal{V}_{\mathrm{DFT}} L_c/h`, where :math:`\mathcal{V}_{\mathrm{DFT}}` is the volume of the unit-cell used in DFT calculations [`Wu et al.`_]. This band-aid solution is often used to compare thermal conductivities of 2D and 3D materials. 



.. _Deepdish: https://deepdish.readthedocs.io/
.. _`Wu et al.`: https://www.sciencedirect.com/science/article/pii/S0009261416310193?via%3Dihub
.. _`Fugallo et al. (2013)`: https://arxiv.org/pdf/1212.0470.pdf
.. _`Romano (2020)`: https://arxiv.org/abs/2002.08940
.. _Phono3py: https://phonopy.github.io/phono3py/
.. _`Chaput (2013)`: https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.110.265506?casa_token=BTUhHjniziYAAAAA%3AGw4C_2ql3cGvy6zwNe_38m7vz130fV7LYZMxrnIt_FSbmQauL3fczg5QT1b0EXTU39nYWEHYUHbv
.. _`Landon (2014)`: https://dspace.mit.edu/handle/1721.1/92161
.. _`Vazrik et al. (2017)` : https://arxiv.org/pdf/1711.07151.pdf
.. _`Cepellotti et al. (2016)` : https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.041013





