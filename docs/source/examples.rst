Examples
=========================================

Interactive examples can be run in Google Colab

.. raw:: html

     <a href="https://colab.research.google.com/drive/18u1ieij2Wn6WEZFN2TmMteYHAJADMdSk?usp=sharing"><img  src="https://colab.research.google.com/assets/colab-badge.svg" style="vertical-align:text-bottom"></a>



1) Different shapes and non-uniform areas
#########################################



.. code-block:: python

   from openbte import Geometry, Solver, Material, Plot

   #Create Material
   Material(source='database',filename='Si',temperature=300,model='rta2DSym')

   #Create Geometry - > remember that in area_ratio, what matters is only the relative numbers, i.e. [1,2] is equivalent to [2,4]
   Geometry(model='lattice',lx = 10,ly = 10, step = 0.5, base = [[0.2,0],[-0.2,0]],porosity=0.1,shape=['circle','square'],area_ratio=[1,2])

   #Run the BTE
   Solver(verbose=False)

   #Plot Maps
   Plot(model='maps',repeat=[3,3,1])

.. raw:: html

    <iframe src="_static/plotly_1.html" height="475px" width="65%"  display= inline-block  ></iframe>


2) Custom shapes
#########################################


.. code-block:: python

   from openbte import Geometry,Material,Solver,Plot
   import numpy as np

   def shape(**options):
    area = options['area']
    T = options['T']
    f = np.sqrt(2)

    poly_clip = []
    a = area/T/2

    poly_clip.append([0,0])
    poly_clip.append([a/f,a/f])
    poly_clip.append([a/f-T*f,a/f])
    poly_clip.append([-T*f,0])
    poly_clip.append([a/f-T*f,-a/f])
    poly_clip.append([a/f,-a/f])

    return poly_clip


   #Create Material
   Material(source='database',filename='Si',temperature=300,model='rta2DSym')

   Geometry(porosity=0.05,lx=100,ly=100,step=5,model='lattice',shape='custom',base=[[0,0],[0.5,0.5]],shape_function=shape,shape_options={'T':[0.025,0.1]})

   #Run the BTE
   Solver(verbose=True)

   #Plot Maps
   Plot(model='maps',repeat=[3,3,1])

.. raw:: html

    <iframe src="_static/plotly_2.html" height="475px" width="65%"  display= inline-block  ></iframe>
   


