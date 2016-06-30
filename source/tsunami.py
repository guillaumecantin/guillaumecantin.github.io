#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: tsunami.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import odeint
from random import randint
import networkx as nx
from .views import articles
import matplotlib.image as mpimg


# View for "Tsunami" article

# PCR system
B1 = 0.5
B2 = 0.5
C2 = 0.2
alpha1 = 0.1
alpha2 = 0.1
delta1 = 0.1
delta2 = 0.1
mu1 = 0.1
mu2 = 0.1

def h(s,smin,smax,hmin,hmax):
    if s<smin:
        return hmin
    elif s>smax:
        return  hmax
    else:
        return ((hmin-hmax)/2)*np.cos(((s-smin)*np.pi)/(smax-smin))+(hmin+hmax)/2

def phi(t):return h(t,1,50,0,1)

def gamma(t):return h(t,1,3,0,1)

def f(s):
    if s<0:return 1
    elif s>1:return 0
    else:return 0.5*np.cos(s*np.pi)+0.5

def F(r,c):
    return -alpha1*f(r/(c+0.01))+alpha2*f(c/(r+0.01))

def G(r,p):
    return -delta1*f(r/(p+0.01))+delta2*f(p/(r+0.01))

def H(c,p):
    return mu1*f(c/(p+0.01))-mu2*f(p/(c+0.01))

def PCR(X, t, C1):
    r, c, p, q = X
    dr = gamma(t)*q*(1-r) - (B1+B2)*r + F(r,c)*r*c + G(r,p)*r*p
    dc = B1*r + C1*p - C2*c - F(r,c)*r*c + H(c,p)*c*p - phi(t)*c*(r+c+p+q)
    dp = B2*r - C1*p + C2*c - G(r,p)*r*p - H(c,p)*c*p
    dq = -gamma(t)*q*(1-r)
    return [dr, dc, dp, dq]


from django.contrib.auth.decorators import login_required

@login_required(login_url='http://guillaumecantin.pythonanywhere.com/login/')
def tsunami(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0

    choicenodes = []
    choiceedges = []
    result = ""
    mycache = randint(1000, 10000)
    absX1, ordX1 = 100.0, 100.0
    absX2, ordX2 = 100.0, 200.0
    absX3, ordX3 = 100.0, 300.0
    absX4, ordX4 = 200.0, 100.0
    absX5, ordX5 = 200.0, 200.0
    absX6, ordX6 = 200.0, 300.0
    absX7, ordX7 = 300.0, 100.0
    absX8, ordX8 = 300.0, 200.0
    edges = [(1, 2), (2, 3), (3, 6), (6, 4)]
    try:
        result = ""
        mycache = randint(1000, 10000)
        img = mpimg.imread('/home/guillaumecantin/mysite/static/simulation/images/plagenice.png')
        result = "The coordinates should satisfy the constraints: $0 \leq x \leq 800$ and $0 \leq y \leq 400$."
        absX1 = float(escape(request.POST['absX1']))
        absX2 = float(escape(request.POST['absX2']))
        absX3 = float(escape(request.POST['absX3']))
        absX4 = float(escape(request.POST['absX4']))
        absX5 = float(escape(request.POST['absX5']))
        absX6 = float(escape(request.POST['absX6']))
        absX7 = float(escape(request.POST['absX7']))
        absX8 = float(escape(request.POST['absX8']))
        ordX1 = float(escape(request.POST['ordX1']))
        ordX2 = float(escape(request.POST['ordX2']))
        ordX3 = float(escape(request.POST['ordX3']))
        ordX4 = float(escape(request.POST['ordX4']))
        ordX5 = float(escape(request.POST['ordX5']))
        ordX6 = float(escape(request.POST['ordX6']))
        ordX7 = float(escape(request.POST['ordX7']))
        ordX8 = float(escape(request.POST['ordX8']))
        edges_str = escape(request.POST['edges'])
        vertices = [int(s) for s in edges_str if s.isdigit()]
        edges = []
        for k in range(len(vertices)//2):
            edges = edges + [(vertices[2*k], vertices[2*k+1])]
        choicenodes = [[absX1, ordX1], [absX2, ordX2], [absX3, ordX3], [absX4, ordX4], [absX5, ordX5], [absX6, ordX6], [absX7, ordX7], [absX8, ordX8]]
        choiceedges = edges

        if 0 <= absX1 <= 800 and 0 <= ordX1 <= 400 and 0 <= absX2 <= 800 and 0 <= ordX2 <= 400 and 0 <= absX3 <= 800 and 0 <= ordX3 <= 400 and 0 <= absX4 <= 800 and 0 <= ordX4 <= 400 and 0 <= absX5 <= 800 and 0 <= ordX5 <= 400 and 0 <= absX6 <= 800 and 0 <= ordX6 <= 400 and 0 <= absX7 <= 800 and 0 <= ordX7 <= 400 and 0 <= absX8 <= 800 and 0 <= ordX8 <= 400 and len(edges) < 500:
            # connectivity matrix
            N = 8
            A = np.array([[0 for i in range(N)] for j in range(N)])
            result = "The edges should involve nodes 1, 2, 3, 4, 5, 6, 7, 8 only."
            for edge in edges:
                j = edge[1]-1
                i = edge[0]-1
                A[j][i] = 1
            for i in range(N):
                A[i][i] = -sum(A[j][i] for j in range(N) if j!= i)

            # Creating graph
            Graph = nx.DiGraph()
            Graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
            Graph.add_edges_from(edges)
            pos = {1: (absX1, ordX1), 2: (absX2, ordX2), 3: (absX3, ordX3), 4: (absX4, ordX4), 5: (absX5, ordX5), 6: (absX6, ordX6), 7: (absX7, ordX7), 8: (absX8, ordX8)}

            # Figure 1
            fig, ax = plt.subplots()
            ax.imshow(img)
            ax.set_xlim(0, 800)
            ax.set_ylim(400, 0)
            ax.grid()
            nx.draw_networkx_nodes(Graph, pos, nodelist=[1, 2, 3, 4], node_color='r')
            nx.draw_networkx_nodes(Graph, pos, nodelist=[5, 6, 7, 8], node_color='g')
            nx.draw_networkx_edges(Graph, pos, edge_color='blue', width=1)
            nx.draw_networkx_labels(Graph, pos)
            ax.text(0.02, -0.1, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/tsunami1.png')
            plt.close(fig)

            # PCR network
            eps = 0.2
            def network(X, t):
                dX = [0 for k in range(4*N)]
                for i in range(4):
                    [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0) + np.array([eps*sum(A[i][j]*X[0+4*j] for j in range(N)), eps*sum(A[i][j]*X[1+4*j] for j in range(N)), eps*sum(A[i][j]*X[2+4*j] for j in range(N)), 0])
                for i in range(4, N):
                    [dX[0+4*i], dX[1+4*i], dX[2+4*i], dX[3+4*i]] = PCR([X[0+4*i], X[1+4*i], X[2+4*i], X[3+4*i]], t, 0.3) + np.array([eps*sum(A[i][j]*X[0+4*j] for j in range(N)), eps*sum(A[i][j]*X[1+4*j] for j in range(N)), eps*sum(A[i][j]*X[2+4*j] for j in range(N)), 0])
                return dX

            X0 = [0 for k in range(4*N)]
            for k in range(N):
                X0[3+4*k] = 1

            # Solve with scipy
            time = np.arange(0, 60, 0.1)
            orbit = odeint(network, X0, time)
            solution = orbit.T
            P = sum(solution[2+4*i] for i in range(N))
            R = sum(solution[0+4*i] for i in range(N))
            C = sum(solution[1+4*i] for i in range(N))

            # Figure 2
            fig, ax = plt.subplots()
            ax.grid()
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.plot(time, R)
            ax.plot(time, C)
            ax.plot(time, P)
            ax.text(0.02, -0.1, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                transform=ax.transAxes,
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            plt.legend((r"$R(t)$", r"$C(t)$", r"$P(t)$"),
                shadow = True,
                prop={'size':20},
                loc = (0.7, 0.5))
            fig.savefig('/home/guillaumecantin/mysite/static/simulation/images/tsunami2.png')
            plt.close(fig)
            result = "Computation ended correctly. You can make other simulations."
        else:
            result = "You must respect the constraints: $0 \leq x \leq 800$ and $0 \leq y \leq 400$."
            choicenodes = []
            choiceedges = []
            absX1, ordX1 = 100.0, 100.0
            absX2, ordX2 = 100.0, 200.0
            absX3, ordX3 = 100.0, 300.0
            absX4, ordX4 = 200.0, 100.0
            absX5, ordX5 = 200.0, 200.0
            absX6, ordX6 = 200.0, 300.0
            absX7, ordX7 = 300.0, 100.0
            absX8, ordX8 = 300.0, 200.0
            edges = [(1, 2), (2, 3), (3, 6), (6, 4)]

    except:
        mycache = randint(1000, 10000)
        choicenodes = []
        choiceedges = []
        #result = "You must respect the constraints: "
        absX1, ordX1 = 100.0, 100.0
        absX2, ordX2 = 100.0, 200.0
        absX3, ordX3 = 100.0, 300.0
        absX4, ordX4 = 200.0, 100.0
        absX5, ordX5 = 200.0, 200.0
        absX6, ordX6 = 200.0, 300.0
        absX7, ordX7 = 300.0, 100.0
        absX8, ordX8 = 300.0, 200.0
        edges = [(1, 2), (2, 3), (3, 6), (6, 4)]
        return render(request, 'simulation/tsunami.html', {
            'result': result,
            'mycache': mycache,
            'articles': articles,
            'islogged': islogged,
            'choicenodes': choicenodes,
            'choiceedges': choiceedges,
            'lenchoicenodes': len(choicenodes)
        })

    return render(request, 'simulation/tsunami.html', {
	    'result': result,
        'mycache': mycache,
        'articles': articles,
        'islogged': islogged,
        'choicenodes': choicenodes,
        'choiceedges': choiceedges,
        'lenchoicenodes': len(choicenodes)
    })
