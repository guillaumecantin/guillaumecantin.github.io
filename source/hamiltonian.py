#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: hamiltonian.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
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


# View for "Hamiltonian system" article
def hamiltonian(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        omega1 = escape(request.POST['omega1'])
        omega2 = escape(request.POST['omega2'])
        omega1 = float(omega1)
        omega2 = float(omega2)

        if 0 <= omega1 <= 10 and 0 <= omega2 <= 10:

            # Torus
            angle = np.linspace(0, 2 * np.pi, 60)
            theta1, theta2 = np.meshgrid(angle, angle)
            r, R = 0.25, 1.5
            X = (R + r * np.cos(theta2)) * np.cos(theta1)
            Y = (R + r * np.cos(theta2)) * np.sin(theta1)
            Z = r * np.sin(theta2)

            # Hamiltonian system in action and angular variables
            t = np.arange(0, 150, 0.01)
            theta1 = omega1*t
            theta2 = omega2*t
            x = (R + r * np.cos(theta1)) * np.cos(theta2)
            y = (R + r * np.cos(theta1)) * np.sin(theta2)
            z = r * np.sin(theta1)

            # Figure
            fig = plt.figure()
            ax = fig.gca(projection = '3d')
            plt.setp(ax.get_xticklabels(), visible=False)
            plt.setp(ax.get_xticklines(), visible=False)
            plt.setp(ax.get_xgridlines(), visible=False)
            plt.setp(ax.get_yticklabels(), visible=False)
            plt.setp(ax.get_yticklines(),visible=False)
            plt.setp(ax.get_zticklabels(), visible=False)
            plt.setp(ax.get_zticklines(),visible=False)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_zticklabels([])
            ax.grid(False)
            ax.set_xlim3d(-1.5, 1.5)
            ax.set_ylim3d(-1.5, 1.5)
            ax.set_zlim3d(-1, 1)
            ax.plot_surface(X, Y, Z, color = 'g',alpha=0.05, rstride = 3, cstride = 3)
            ax.plot(x,y,z)
            ax.set_title(r'$ \omega_1 = '+str(omega1)+r', \omega_2 = '+str(omega2)+r' $')
            ax.text(1, 0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/hamiltonian.png')
            plt.close(fig)
            result = "You can make many simulations."
        else:
            result = "You must enter decimal numbers between $0$ and $10$."
            omega1 = 5
            omega2 = 2

    except:
        mycache = randint(1000, 10000)
        result = "You must enter decimal numbers between $0$ and $10$."
        omega1 = 5
        omega2 = 2
        return render(request, 'simulation/hamiltonian.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/hamiltonian.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })
