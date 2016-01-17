#!/usr/bin/env python3

"""
PCR system
Succession of catastophic events
"""

#scientific libraries
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.integrate import odeint
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

#matplotlib arrow to follow the orbit
def myarrow2d(plt,begin,end,dim,col):
    return plt.arrow(begin[0],begin[1],end[0],end[1],head_width=dim[0],head_length=dim[1],color=col)

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

#functions of the PCR system
def h(s,smin,smax,hmin,hmax):
    if s<smin:
        return hmin
    elif s>smax:
        return  hmax
    else:
        return ((hmin-hmax)/2)*np.cos(((s-smin)*np.pi)/(smax-smin))+(hmin+hmax)

def phi(t):return h(t,50,90,0,1)
def gamma(t):return h(t,1,3,0,1)

def f11(s):
    if s<0:return 1
    elif s>1:return 0
    else:return 0.5*np.cos(s*np.pi)+0.5

def s1(t):return (np.cos(t)*A+1)/2
def s2(t):return 0

def Frc(x,y):return -alpha1*f11(x/(y+0.01))+alpha2*f11(y/(x+0.01))
def Frp(x,z):return -delta1*f11(x/(z+0.01))+delta2*f11(z/(x+0.01))
def G(y,z):return mu1*f11(y/(z+0.01))-mu2*f11(z/(y+0.01))
def a(t,A):return 1/(2+4/(1+A*np.cos(t)))

#PCR system
def PCR(X,t):
    q,r,c,p = X
    dq = -gamma(t)*q*(1-r/rm)
    dr = gamma(t)*q*(1-r/rm)-(B1+B2)*r+Frc(r,c)*r*c+Frp(r,p)*r*p+s1(t)*c+s2(t)*p
    dc = B1*r-Frc(r,c)*r*c+C1*p-s1(t)*c-C2*c-phi(t)*c*(p+c+r+q)+G(c,p)*c*p
    dp = B2*r-s2(t)*p-Frp(r,p)*r*p-C1*p+C2*c-G(c,p)*c*p
    return [dq,dr,dc,dp]

#parameters of the PCR system
B1 = 1 
B2 = 1
alpha1 = 0
alpha2 = 0
delta1 = 0
delta2 = 0 
mu1 = 0
mu2 = 0
C1 = 1 
C2 = 0 
N = 1
rm = 1
A = 0.9

t_output = np.arange(0, 100, 0.1)
CondInit = [1, 0, 0, 0]

#create a matplotlib figure
fig = plt.figure()
ax = fig.gca(projection='3d')
for T in range(2,79):
    time = np.arange(0,T,0.1)
    y_result = odeint(PCR,CondInit,time) #solve with scipy
    qq, rr, cc, pp = y_result.T
    ax.set_ylim(0,0.6)
    ax.set_xlim(0,0.4)
    ax.set_zlim(0,0.3)
    ax.view_init(10, 110)
    ax.set_xlabel(r"$r$",fontsize=24)
    ax.set_ylabel(r"$c$",fontsize=24)
    ax.set_zlabel(r"$p$",fontsize=24)
    a = Arrow3D([rr[-3],rr[-1]],[cc[-3],cc[-1]],[pp[-3],pp[-1]], mutation_scale=20, lw=1, arrowstyle="-|>", color="b") #draw an arrow
    ax.add_artist(a)
    #set ticks unvisible
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_xticklines(), visible=False)
    plt.setp(ax.get_xgridlines(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_yticklines(),visible=False)
    plt.setp(ax.get_zticklabels(), visible=False)
    plt.setp(ax.get_zticklines(),visible=False)
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.plot(rr,cc,pp,'b')
    plt.pause(0.001)
    #save the figures
    if T<10:fig.savefig('~/domino/domino0'+str(T)+'.png')
    else:fig.savefig('~/domino/domino'+str(T)+'.png')
    ax.clear()


