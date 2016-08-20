#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: bazykin.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from random import randint
from scipy.integrate import odeint
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

# 2d arrow
def myarrow(x, y, t):
    return plt.annotate("",(x[t], y[t]),(x[t-2], y[t-2]),arrowprops=dict(arrowstyle="->", color='blue'), fontsize=20)

# View for "Bazykin's model" article
def bazykin(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        alpha = escape(request.POST['alpha'])
        delta = escape(request.POST['delta'])
        alpha = float(alpha)
        delta = float(delta)

        if 0 <= alpha <= 1 and 0 <= delta <= 1:

            # Bazykin's model
            gamma = 1
            eps = 0.1

            def baz(X, t):
                x1, x2 = X
                dx1 = x1 - (x1*x2)/(1+alpha*x1) - eps*x1*x1
                dx2 = -gamma*x2 + (x1*x2)/(1+alpha*x1) - delta*x2*x2
                return [dx1, dx2]

            # Numerical integration

            time = np.arange(0, 100, 0.01)

            X1 = [1, 1]
            X2 = [0.5, 0.5]
            X3 = [0.1, 1]

            orbit1 = odeint(baz, X1, time)
            orbit2 = odeint(baz, X2, time)
            orbit3 = odeint(baz, X3, time)

            x11, x21 = orbit1.T
            x12, x22 = orbit2.T
            x13, x23 = orbit3.T

            # Figure in the (x1, x2) plane

            fig, ax = plt.subplots()
            ax.plot(x11, x21, 'b')
            myarrow(x11, x21, 500)
            ax.plot(x12, x22, 'b')
            myarrow(x12, x22, 500)
            ax.plot(x13, x23, 'b')
            myarrow(x13, x23, 500)
            ax.set_xlabel(r"$x_1$", fontsize=20)
            ax.set_ylabel(r"$x_2$", fontsize=20, rotation='horizontal')
            ax.set_title(r'$\alpha = '+str(alpha)+r', \delta = '+str(delta)+r' $')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/bazykin1.png')
            plt.close(fig)


            # Figure on the Poincare sphere

            def limites(u, e, a):
                ax.set_xlim(-u, u)
                ax.set_ylim(-u, u)
                ax.set_zlim(-u, u)
                ax.view_init(elev=e, azim=a)

            def trajectoire(x, y, t0):
                X = x/np.sqrt(1+x**2+y**2)
                Y = y/np.sqrt(1+x**2+y**2)
                Z = 1/np.sqrt(1+x**2+y**2)
                ax.plot3D(X, Y, Z, color = 'red', linewidth=1.5)
                a = Arrow3D([X[t0],X[t0+2]],[Y[t0],Y[t0+2]],[Z[t0],Z[t0+2]], mutation_scale=20, lw=1, arrowstyle="-|>", color='red')
                ax.add_artist(a)

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

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_axis_off()
            ax.grid(False)
            ax.plot(x2, y2, z2, lw=2.5, color='0.25', alpha=0.7)
            ax.plot_surface(x1, y1, z1, rstride=1, cstride=1, linewidth=0.1, color='#FAFAFA')
            trajectoire(x11, x21, 200)
            trajectoire(x12, x22, 200)
            trajectoire(x13, x23, 200)
            limites(0.7, 37, 32)
            ax.set_title(r'$\alpha = '+str(alpha)+r', \delta = '+str(delta)+r' $')
            ax.text(1, 0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/bazykin2.png')
            plt.close(fig)

            result = "You can make many simulations."
        else:
            result = "You must enter decimal numbers between $0$ and $1$."
            alpha = 0.5
            delta = 0.5

    except:
        mycache = randint(1000, 10000)
        result = "You must enter decimal numbers between $0$ and $1$."
        alpha = 0.5
        delta = 0.5
        return render(request, 'simulation/bazykin.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/bazykin.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })
