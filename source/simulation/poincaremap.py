#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: poincaremap.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from random import randint
from .views import articles

# View for "Poincaré map" article
def poincaremap(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        E = escape(request.POST['E'])
        E = float(E)
        if 0.05 <= E <= 0.15:

            # Hénon-Heiles model
            y0 = 0
            py0 = 0
            px0 = 0.3
            x0 = (2*E - px0*px0)**0.5
            CI = [x0, px0, y0, py0]

            def henon_heiles(X, t):
                x, px, y, py = X
                dx = px
                dpx = -x - 2*x*y
                dy = py
                dpy = -y - x*x + y*y
                return [dx, dpx, dy, dpy]

            def HH(X,x):
                px, y, py, t = X
                dpx_dx = (-x - 2*x*y)/(px)
                dy_dx = (py)/(px)
                dpy_dx = (-y - x*x + y*y)/(px)
                dt_dx = 1/(px)
                return [dpx_dx, dy_dx, dpy_dx, dt_dx]

            # Euler method
            def euler(X, x, step):
                px, y, py, t = X
                pxnew = px + step*HH(X,x)[0]
                ynew = y + step*HH(X,x)[1]
                pynew = py + step*HH(X,x)[2]
                tnew = t + step*HH(X,x)[3]
                return [pxnew, ynew, pynew, tnew]

            # Hénon trick
            time = np.arange(0, 4000, 0.01)
            result = odeint(henon_heiles, CI, time)
            S = x0 - 0
            Sold = S
            Y = []
            PY = []
            for t in time:
                Sold = S
                p = result[t*100]
                S = p[0]
                if S*Sold < 0:
                    point = euler([p[1], p[2], p[3], t], p[0], S)
                    Y = Y + [point[1]]
                    PY = PY + [point[2]]

            # Figure
            fig, ax = plt.subplots()
            ax.scatter(Y, PY, s=0.5, color='b')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.set_xlim(-0.8, 1.3)
            ax.set_ylim(-0.8, 0.8)
            ax.set_xlabel(r"$y$", fontsize=24)
            ax.set_ylabel(r"$p_y$", fontsize=24, rotation='horizontal')
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.grid()
            ax.set_title(r"$E ="+str(E)+r"$", size='20')
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/poincaremap.png')
            plt.close(fig)

            result = """You can make many simulations."""
        else:
            result = "You must enter a decimal number between $0.05$ and $0.15$."
            E = 0.125

    except:
        mycache = randint(1000, 10000)
        result = "You must enter a decimal number between $0.05$ and $0.15$."
        E = 0.125
        return render(request, 'simulation/poincaremap.html', {
            'result': result,
            'E': E,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/poincaremap.html', {
	    'result': result,
        'E': E,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })
