#import h5py
from google_drive_downloader import GoogleDriveDownloader as gdd
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon,LineString
import shapely
from shapely.ops import cascaded_union
import os
import functools


def periodic_kernel(x1, x2, p,l,variance):
    return variance*np.exp(-2/l/l * np.sin(np.pi*abs(x1-x2)/p) ** 2)

def gram_matrix(xs,p,l,variance):
    return [[periodic_kernel(x1,x2,p,l,variance) for x2 in xs] for x1 in xs]

def generate_random_interface(p,l,variance,scale):

 xs = np.arange(-p/2, p/2,p/200)
 mean = [0 for x in xs]
 gram = gram_matrix(xs,p,l,variance)
 ys = np.random.multivariate_normal(mean, gram)*scale
 f = interpolate.interp1d(xs, ys,fill_value='extrapolate')

 return f

def download_file(file_id,filename):

      gdd.download_file_from_google_drive(file_id=file_id,
                                           dest_path='./' + filename,showsize=True,overwrite=True)


def generate_frame(**argv):

    Lx = float(argv['lx'])
    Ly = float(argv['ly'])
    frame = []
    frame.append([-Lx/2,Ly/2])
    frame.append([Lx/2,Ly/2])
    frame.append([Lx/2,-Ly/2])
    frame.append([-Lx/2,-Ly/2])

    return frame


def translate_shape(shape,base):

  out = []
  for p in shape:
    tmp = [p[0] + base[0],p[1] + base[1]]
    out.append(tmp)

  return out

def repeat_merge_scale(argv):

  polygons = argv['polygons']


  pbc = []
  pbc.append([0,0])
  pbc.append([1,0])
  pbc.append([-1,0])
  pbc.append([0,1])
  pbc.append([0,-1])
  pbc.append([1,1])
  pbc.append([-1,-1])
  pbc.append([-1,1])
  pbc.append([1,-1])
  lx = argv['lx']   
  ly = argv['ly']   


  frame = Polygon([[-0.5,-0.5],[-0.5,0.5],[0.5,0.5],[0.5,-0.5]])

   #---------------------
  #Store only the intersecting polygons
  final = []
  for poly in polygons:
    for kp in range(len(pbc)):
     tmp = []
     for p in poly:
      cx = p[0] + pbc[kp][0]
      cy = p[1] + pbc[kp][1]
      tmp.append([cx,cy])
     p1 = Polygon(tmp)
     if p1.intersects(frame):
      thin = Polygon(p1).intersection(frame)
      if isinstance(thin, shapely.geometry.multipolygon.MultiPolygon):
       tmp = list(thin)
       for t in tmp:
        final.append(t)
      else:
        final.append(thin)

  #Create bulk surface---get only the exterior to avoid holes
  MP = MultiPolygon(final) 

  conso = cascaded_union(MP)

  polygons_final = []
  if isinstance(conso, shapely.geometry.multipolygon.MultiPolygon):
      for i in conso: 
       polygons_final.append(list(i.exterior.coords))
  else: 
       polygons_final.append(list(conso.exterior.coords))
  

  

  #cut redundant points (probably unnecessary)
  new_poly = []
  for poly in polygons_final:
   N = len(poly)
   tmp = []
   for n in range(N):
    p1 = poly[n]
    p2 = poly[(n+1)%N]
    if np.linalg.norm(np.array(p1)-np.array(p2)) >1e-4:
     tmp.append(p1)
   new_poly.append(tmp)


  dmin = check_distances(new_poly)


  #scale-----------------------
  polygons = []
  for poly in new_poly:
   tmp = []
   for p in poly:
    g = list(p)
    g[0] *=lx
    g[1] *=ly
    tmp.append(g)
   polygons.append(tmp) 

  argv['polygons'] = polygons
  argv['dmin'] = dmin


def check_distances(new_poly):


  #Merge pores is they are too close
  Pores = [ Polygon(p)  for p in new_poly]
  dmin = 1e4
  move = {}
  for p1 in range(len(Pores)):
   #check if intersect   
   for p2 in range(p1+1,len(Pores)):
       d = Pores[p1].distance(Pores[p2])
       if d > 0 and d < dmin : dmin = d
      
   #top
   d = Pores[p1].distance(LineString([(-0.5,0.5),(0.5,0.5)])) 
   if d < dmin and d > 0:
     dmin = d

   #left
   d = Pores[p1].distance(LineString([(0.5,0.5),(0.5,-0.5)])) 
   if d < dmin and d > 0:
     dmin = d

   #bottom
   d = Pores[p1].distance(LineString([(-0.5,-0.5),(0.5,-0.5)])) 
   if d < dmin and d > 0:
     dmin = d
  
   #left
   d = Pores[p1].distance(LineString([(-0.5,-0.5),(-0.5,0.5)])) 
   if d < dmin and d > 0:
     dmin = d

  return dmin


def get_linear_indexes(mfp,value,scale,extent):

   if value == 0:
     return -1,-1,-1,-1

   n = len(mfp)

   found = False
   beyond = False
   if extent:
    if value < mfp[0]:
      beyond = True
      found = True
      i=0;j=1;
    elif value > mfp[-1]:
      i=n-2;j=n-1;
      beyond = True
      found = True
   if beyond == False:
    for m in range(n-1):

      if (value <= mfp[m+1]) and (value >= mfp[m]) :
        i = m; j= m+1 
        found = True
        break
  
   if found == False:
      print('no interpolation found')
   else:  
    aj = (value-mfp[i])/(mfp[j]-mfp[i]) #OK.
    ai = 1-aj

    if scale=='inverse':
     ai *=mfp[i]/value
     aj *=mfp[j]/value
   return i,ai,j,aj  

