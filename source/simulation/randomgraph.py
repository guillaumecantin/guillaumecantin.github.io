#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: randomgraph.py
"""

from django.shortcuts import render
from django.utils.html import escape

# Scientific libraries
from matplotlib import pyplot as plt
from random import randint
import networkx as nx
from .views import articles

# View for "Random graph" article

def randomgraph(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    mycache = randint(1000, 10000)
    number = 50
    density = 0.5
    liste = []
    single = 1
    try:
        mycache = randint(1000, 10000)
        number = escape(request.POST['number'])
        density = escape(request.POST['density'])
        number = int(number)
        density = float(density)
        if 2 <= number <= 100 and 0 < density < 1:

            G = nx.random_geometric_graph(number, density)
            pos = nx.get_node_attributes(G, 'pos')

            # Figure
            plt.figure()
            nx.draw_networkx_edges(G, pos, alpha=0.3)
            if number <= 20:
                nx.draw_networkx_labels(G, pos, font_size=8, alpha=0.8)
                nx.draw_networkx_nodes(G, pos)
            else:
                nx.draw_networkx_nodes(G, pos, node_size=20)
            plt.xlim(-0.05,1.05)
            plt.ylim(-0.05,1.05)
            plt.axis('off')
            plt.title(r'$ n = '+str(number)+r' , \delta ='+str(density)+r' $')
            plt.text(0.02, 0.02, 'Copyright - Guillaume Cantin - 2016',
                verticalalignment='bottom', horizontalalignment='left',
                style='italic',
                color='gray',
                fontsize=6,
                alpha=0.2)
            plt.savefig('/home/guillaumecantin/mysite/static/simulation/images/randomgraph.png')
            plt.close()

            # Path finding
            if number <= 20:
                liste = []
                counter = 0
                for k in range(1, number):
                    if nx.has_path(G, 0, k) == True:
                        counter = counter + 1
                        liste = liste + [[k, nx.shortest_path(G, 0, k)]]
                if counter > 0:
                    single = 0

            result = """You can draw many graphs."""
        else:
            result = "You must respect the constraints: $2 \leq n \leq 100$ and $0 < \delta < 1$."
            number = 50
            density = 0.5
            liste = []
            single = 1

    except:
        mycache = randint(1000, 10000)
        result = "You must respect the constraints: $2 \leq n \leq 100$ and $0 < \delta < 1$."
        number = 50
        density = 0.5
        liste = []
        single = 1
        return render(request, 'simulation/randomgraph.html', {
            'result': result,
            'number': number,
            'density': density,
            'mycache': mycache,
            'liste': liste,
            'single': single,
            'articles': articles,
            'islogged': islogged
        })
    return render(request, 'simulation/randomgraph.html', {
	    'result': result,
        'number': number,
        'density': density,
        'mycache': mycache,
        'liste': liste,
        'single': single,
        'articles': articles,
        'islogged': islogged
    })
