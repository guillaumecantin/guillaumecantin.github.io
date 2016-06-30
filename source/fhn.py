#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: fhn.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from random import randint
from .views import articles


# View for "FitzHugh-Nagumo model" article
def fhn(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        c = escape(request.POST['c'])
        c = float(c)
        if 0 <= c <= 1:

            # FitzHugh-Nagumo model for two identical cells
            a = 0.5
            b = 0.5
            gamma = 0.5
            def f(X,t):
                v1, w1, v2, w2 = X
                dv1 = v1*(a-v1)*(v1-1)-w1-c*v2
                dw1 = b*v1-gamma*w1
                dv2 = v2*(a-v2)*(v2-1)-w2-c*v1
                dw2 = b*v2-gamma*w2
                return [dv1, dw1, dv2, dw2]

            # Numerical integration with scipy.odeint
            time = np.arange(0, 40, 0.05)
            X0 = [0.3, 0.3, -0.3, -0.3]
            orbit = odeint(f, X0, time)
            v1, w1, v2, w2 = orbit.T

            # Figure 1
            fig, ax = plt.subplots()
            ax.set_ylim(-0.6, 1)
            ax.plot(time, v1)
            ax.plot(time, v2)
            ax.set_title(r"$c ="+str(c)+r"$", size='20')
            ax.legend((r"$v_1(t)$",r"$v_2(t)$"), ncol=1, shadow = True, prop={'size':20}, loc = (0.71, 0.73))
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.grid()
            ax.set_xlabel(r'$t$')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/fhn1.png')
            plt.close(fig)

            # Figure 2
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(v1, v2, 'b')
            ax.set_xlabel(r'$v_1$')
            ax.set_ylabel(r'$v_2$', rotation='horizontal')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/fhn2.png')
            plt.close(fig)

            result = """You can make many simulations."""
        else:
            result = "You must enter a decimal number between $0$ and $1$."
            c = 0.3

    except:
        mycache = randint(1000, 10000)
        result = "You must enter a decimal number between $0$ and $1$."
        c = 0.3
        return render(request, 'simulation/fhn.html', {
            'result': result,
            'c': c,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/fhn.html', {
	    'result': result,
        'c': c,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })
