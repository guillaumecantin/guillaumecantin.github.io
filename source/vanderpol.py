#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: vanderpol.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from random import randint
from .views import articles


# View for "Van der Pol equation" article
def vanderpol(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        mu = escape(request.POST['mu'])
        mu = float(mu)
        if -1 <= mu <= 2:

            # Van der Pol equation
            def f(X,t):
                x, y = X
                dx = y
                dy = -x + mu*(1-x*x)*y
                return np.array([dx, dy])

            # Numerical integration with scipy.odeint
            h = 0.01
            time = np.arange(0, 100, h)
            X0 = [1, 0]
            orbit = odeint(f, X0, time)
            x, y = orbit.T

            # Figure 1
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(x, y, 'r')
            ax.set_title(r'$ \mu = '+str(mu)+r' $')
            ax.set_xlabel(r'$x_1$')
            ax.set_ylabel(r'$x_2$', rotation='horizontal')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/vanderpol.png')
            plt.close(fig)

            # Figure 2
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(time[:5000], x[:5000], 'b')
            ax.set_xlabel(r'$t$')
            ax.set_ylabel(r'$x_1$', rotation='horizontal')
            ax.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/vanderpol2.svg')
            plt.close(fig)

            result = """You can make many simulations."""
        else:
            result = "You must enter a decimal number between $-1$ and $2$."
            mu = 0.4

    except:
        mycache = randint(1000, 10000)
        result = "You must enter a decimal number between $-1$ and $2$."
        mu = 0.4
        return render(request, 'simulation/vanderpol.html', {
            'result': result,
            'mu': mu,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/vanderpol.html', {
	    'result': result,
        'mu': mu,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })