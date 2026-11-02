"""Reproducible solid-mesh primitives; metres before final print scaling.
No historical geometry is implied by these generic construction helpers.
"""
import numpy as np
from manifold3d import Manifold,CrossSection

def box(x0,x1,y0,y1,z0,z1):
 assert x1>x0 and y1>y0 and z1>z0
 return Manifold.cube((x1-x0,y1-y0,z1-z0)).translate((x0,y0,z0))

def prism(points,z0,z1):
 p=np.asarray(points,dtype=float)
 if np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])<0:p=p[::-1]
 return CrossSection([p]).extrude(z1-z0).translate((0,0,z0))

def perimeter_band(points,width,z0,z1):
 p=np.asarray(points,dtype=float)
 if np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])<0:p=p[::-1]
 c=CrossSection([p]);return (c-c.offset(-width)).extrude(z1-z0).translate((0,0,z0))

def y_intersections(points,x):
 """Locate real outside wall segments, not the axis-domain bounding box."""
 ys=[]
 for (a,b),(c,d) in zip(points,points[1:]+points[:1]):
  if min(a,c)<=x<max(a,c):ys.append(b+(d-b)*(x-a)/(c-a))
 return sorted(ys)

def square_vault_cap(cx,cy,z0,span=1.2,rise=.5,n=12):
 """Square-plan clipped orthogonal barrel intersection, not circular hemisphere.
 Printed source controls span/rise; curved interpolation is explicitly approximate.
 """
 h=span/2;r=(h*h+rise*rise)/(2*rise);zc=z0+rise-r
 xs=np.linspace(-h,h,n+1);prof=[(-h,z0-.04),(h,z0-.04)]+[(float(x),float(zc+(r*r-x*x)**.5))for x in xs[::-1]]
 # x,z plane extruded through y; reflection is corrected by Manifold.
 a=CrossSection([prof]).extrude(span).transform(((1,0,0,cx),(0,0,1,cy-h),(0,1,0,0)))
 b=CrossSection([prof]).extrude(span).transform(((0,0,1,cx-h),(1,0,0,cy),(0,1,0,0)))
 return a^b
