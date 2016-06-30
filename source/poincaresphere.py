#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: poincaresphere.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from random import randint
from .views import articles

# 3d arrow
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

# View for "Poincaré sphere" article

def poincaresphere(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        Lambda = escape(request.POST['Lambda'])
        Lambda = float(Lambda)

        if -1 <= Lambda <= 1:

            # Sphere
            u = np.linspace(0, 2 * np.pi, 39)
            v = np.linspace(0, np.pi, 21)
            x1 = np.outer(np.cos(u), np.sin(v))
            y1 = np.outer(np.sin(u), np.sin(v))
            z1 = np.outer(np.ones(np.size(u)), np.cos(v))

            # Equator
            u = np.linspace(0, 2 * np.pi, 100)
            x2 = np.cos(u)
            y2 = np.sin(u)
            z2 = np.array([0 for k in range(len(u))])

            # Vertical Hopf bifurcation
            def system(X, t):
                x, y = X
                dx = Lambda*x - y
                dy = x + Lambda*y
                return [dx, dy]
            orbit = odeint(system, [1,1], np.arange(0, 50, 0.01))
            x, y = orbit.T

            # Projection on the Poincaré sphere
            X = x/np.sqrt(1+x**2+y**2)
            Y = y/np.sqrt(1+x**2+y**2)
            Z = 1/np.sqrt(1+x**2+y**2)

            # Figure
            fig = plt.figure(figsize=(10,10))
            ax = fig.gca(projection = '3d')
            ax.set_axis_off()
            ax.grid(False)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_zlim(-1, 1)
            ax.plot_surface(x1, y1, z1, rstride=2, cstride=2, color='b', alpha=0.05, shade=1)
            ax.plot(x2, y2, z2, color='gray')
            ax.plot(X, Y, Z, color='blue')
            ax.set_title(r'$ \lambda = '+str(Lambda)+r' $')
            ax.text(1, 0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            ax.view_init(elev=30, azim=-140)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/poincaresphere.png')
            plt.close(fig)
            result = "You can make many simulations."
        else:
            result = "You must enter a decimal number between $-1$ and $1$."
            Lambda = 0.1

    except:
        mycache = randint(1000, 10000)
        result = "You must enter a decimal number between $-1$ and $1$."
        Lambda = 0.1
        return render(request, 'simulation/poincaresphere.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/poincaresphere.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })