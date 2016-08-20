#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: bluesky.py
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

# View for "Blue-sky bifurcation" article
def bluesky(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        mu = escape(request.POST['mu'])
        mu = float(mu)
        if 0.1 <= mu <= 0.5:

            # Blue-sky system
            eps = 0.02
            b = 10

            def f(X, t):
                x, y, z = X
                dx = x*(2 + mu - b*(x**2+y**2)) + z**2 + y**2 + 2*y
                dy = -z**3 - (y+1)*(z**2 + y**2 + 2*y) - 4*x + mu*y
                dz = z**2*(y+1) + x**2 - eps
                return np.array([dx, dy, dz])

            # Numerical integration with scipy.odeint
            h = 0.01
            time = np.arange(0, 150, h)
            X0 = [1, -1, 2]
            orbit = odeint(f, X0, time)
            x, y, z = orbit.T

            # Figure
            fig = plt.figure()
            ax = fig.gca(projection = '3d')
            plt.setp(ax.get_xticklabels(), visible=False)
            plt.setp(ax.get_xticklines(), visible=False)
            plt.setp(ax.get_xgridlines(), visible=False)
            plt.setp(ax.get_yticklabels(), visible=False)
            plt.setp(ax.get_yticklines(), visible=False)
            plt.setp(ax.get_zticklabels(), visible=False)
            plt.setp(ax.get_zticklines(), visible=False)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_zticklabels([])
            ax.grid(False)
            ax.plot(x, y, z, 'b', linewidth=0.5)
            arrow = Arrow3D([x[1200],x[1202]],[y[1200],y[1202]],[z[1200],z[1202]], mutation_scale=20, lw=1, arrowstyle="->", color="b")
            ax.add_artist(arrow)
            ax.view_init(elev=9, azim=-5)
            ax.set_title(r'$ \mu = '+str(mu)+r' $')
            ax.set_xlabel(r'$x$')
            ax.set_ylabel(r'$y$', rotation='horizontal')
            ax.set_zlabel(r'$z$', rotation='horizontal')
            ax.text(1, 0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/bluesky.png')
            plt.close(fig)
            result = """You can make many simulations."""
        else:
            result = "You must enter a decimal number between $0.1$ and $0.5$."
            mu = 0.4

    except:
        mycache = randint(1000, 10000)
        result = "You must enter a decimal number between $0.1$ and $0.5$."
        mu = 0.4
        return render(request, 'simulation/bluesky.html', {
            'result': result,
            'mu': mu,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/bluesky.html', {
	    'result': result,
        'mu': mu,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })