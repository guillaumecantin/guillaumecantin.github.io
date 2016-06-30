#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: pcrsystem.py
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


# View for "PCR system" article

# Parameters
xm = 0.75
X0 = [0, 0, 0, 1, 0]
def h(s,smin,smax,hmin,hmax):
    if s<smin:return hmin
    elif s>smax:return  hmax
    else:return ((hmin-hmax)/2)*np.cos(((s-smin)*np.pi)/(smax-smin))+(hmin+hmax)/2

def phi(t):return h(t,1,50,0,1)
def gamma(t):return h(t,1,3,0,1)
def f1(t):return h(t,0.45,0.6,-1,0.4)
def f2(t):return h(t,0.45,0.6,-1,0.4)
def g(t):return h(t,0,0.1,-1,1)
def f11(s):
    if s<0:return 1
    elif s>1:return 0
    else:return 0.5*np.cos(s*np.pi)+0.5

from django.contrib.auth.decorators import login_required

@login_required(login_url='http://guillaumecantin.pythonanywhere.com/login/')
def pcrsystem(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    try:
        mycache = randint(1000, 10000)
        B1 = escape(request.POST['B1'])
        B2 = escape(request.POST['B2'])
        C1 = escape(request.POST['C1'])
        C2 = escape(request.POST['C2'])
        s1 = escape(request.POST['s1'])
        s2 = escape(request.POST['s2'])
        alpha1 = escape(request.POST['alpha1'])
        alpha2 = escape(request.POST['alpha2'])
        delta1 = escape(request.POST['delta1'])
        delta2 = escape(request.POST['delta2'])
        mu1 = escape(request.POST['mu1'])
        mu2 = escape(request.POST['mu2'])
        B1 = float(B1)
        B2 = float(B2)
        C1 = float(C1)
        C2 = float(C2)
        s1 = float(s1)
        s2 = float(s2)
        alpha1 = float(alpha1)
        alpha2 = float(alpha2)
        delta1 = float(delta1)
        delta2 = float(delta2)
        mu1 = float(mu1)
        mu2 = float(mu2)

        if 0 <= B1 <= 1 and 0 <= B2 <= 1 and 0 <= C1 <= 1 and 0 <= C2 <= 1 and 0 <= s1 <= 1 and 0 <= s2 <= 1 and 0 <= alpha1 <= 1 and 0 <= alpha2 <= 1 and 0 <= delta1 <= 1 and 0 <= delta2 <= 1 and 0 <= mu1 <= 1 and 0 <= mu2 <= 1:

            # PCR system
            def Fxy(x,y):return -alpha1*f11(x/(y+0.01)) + alpha2*f11(y/(x+0.01))
            def Fxz(x,z):return -delta1*f11(x/(z+0.01)) + delta2*f11(z/(x+0.01))
            def G(y,z):return mu1*f11(y/(z+0.01)) - mu2*f11(z/(y+0.01))

            def PCR(X, t):
                x, y, z, Q1, Q2 = X
                dx = gamma(t)*Q1*(1-x/xm) - (B1+B2)*x + Fxy(x,y)*x*y + Fxz(x,z)*x*z + s1*y + s2*z
                dy = B1*x - Fxy(x,y)*x*y + C1*z - s1*y - C2*y - phi(t)*y*(1-Q2) + G(y,z)*y*z
                dz = B2*x - s2*z - Fxz(x,z)*x*z - C1*z + C2*y - G(y,z)*y*z
                dQ1 = -gamma(t)*Q1*(1-x/xm)
                dQ2 = phi(t)*y*(1-Q2)
                return [dx, dy, dz, dQ1, dQ2]

            # Solve with scipy
            time = np.arange(0, 60, 0.01)
            orbit = odeint(PCR, X0, time)
            r, c, p, q, b = orbit.T

            # Figure
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(time, r)
            ax.plot(time, c)
            ax.plot(time, p)
            title = r'$ B_1 = '+str(B1)+r', B_2 = '+str(B2)+r', C_1 = '+str(C1)+r', C_2 = '+str(C2)
            title = title + r', s_1 = '+str(s1)+r', s_2 = '+str(s2)+'$ \n $'+r' \alpha_1 = '+str(alpha1)
            title = title + r', \alpha_2 = '+str(alpha2)+r', \delta_1 = '+str(delta1)+r', \delta_2 = '
            title = title + str(delta2)+r', \mu_1 = '+str(mu1)+r', \mu_2 = '+str(mu2)+r' $'
            ax.set_title(title)
            ax.set_ylim(0, 1)
            ax.text(0.02, -0.1, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            plt.legend((r"$r(t)$", r"$c(t)$", r"$p(t)$"),
                shadow = True,
                prop={'size':20},
                loc = (0.7, 0.5))
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/pcrsystem.png')
            plt.close(fig)

            # Figure 3d
            fig = plt.figure()
            ax = fig.gca(projection = '3d')
            ax.grid()
            ax.plot(r, c, p, 'b', linewidth=0.8)
            arrow = Arrow3D([r[200],r[202]],[c[200],c[202]],[p[200],p[202]], mutation_scale=20, lw=0.8, arrowstyle="->", color="b")
            ax.add_artist(arrow)
            ax.set_xlabel(r'$r$')
            ax.set_ylabel(r'$c$')
            ax.set_zlabel(r'$p$')
            ax.text(0.5, 0.5, 0.0, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/pcrsystem3d.png')
            plt.close(fig)
            result = """You can make many simulations."""
        else:
            result = "You must enter decimal numbers between $0$ and $1$."
            B1 = 0.5
            B2 = 0.5
            C1 = 0.5
            C2 = 0.5
            s1 = 0.5
            s2 = 0.5
            alpha1 = 0.5
            alpha2 = 0.5
            delta1 = 0.5
            delta2 = 0.5
            mu1 = 0.5
            mu2 = 0.5

    except:
        mycache = randint(1000, 10000)
        result = "You must enter decimal numbers between $0$ and $10$."
        B1 = 0.5
        B2 = 0.5
        C1 = 0.5
        C2 = 0.5
        s1 = 0.5
        s2 = 0.5
        alpha1 = 0.5
        alpha2 = 0.5
        delta1 = 0.5
        delta2 = 0.5
        mu1 = 0.5
        mu2 = 0.5
        return render(request, 'simulation/pcrsystem.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/pcrsystem.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged
    })