#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: views.py
"""

from django.shortcuts import render, redirect
from django.utils.html import escape

# list of articles

from .models import Figure

figures_list = Figure.objects.order_by('id')

figures_list_for_articles = [['figure/'+str(figure.id), str(figure.title), str(figure.summary)[:60]+' ...'] for figure in figures_list]

simulations_list = [['bazykin', 'Bazykin\'s model', 'Make your own simulation of the Bazykin\'s prey-predator model.'],
            ['bluesky', 'Blue-sky bifurcation', 'Make your own simulation of the blue-sky bifurcation.'],
            ['fhn', 'FitzHugh-Nagumo model', 'Experiment the emergence of a periodic regime in a two cells network coupled with the FitzHugh-Nagumo model.'],
            ['hamiltonian', 'Hamiltonian system', 'Visualize the orbit of an hamiltonian system on a torus.'],
            ['pcrnetwork', 'PCR network', 'Make your own simulation of a PCR network. (Limited access)'],
            ['pcrsystem', 'PCR system', 'Make your own simulation of the PCR system. (Limited access)'],
            ['poincaremap', 'Poincaré map', 'Create your own Poincaré map of the Hénon-Heiles model.'],
            ['poincaresphere', 'Poincaré sphere', 'Visualize the projection of an orbit on the Poincaré sphere.'],
            ['randomgraph', 'Random graph', 'Draw a random graph with the Networkx library, and find some paths.'],
            ['tsunami', 'Tsunami in Nice', 'Make a simulation of a tsunami in Nice with the PCR system. (Limited access)'],
            ['vanderpol', 'Van der Pol equation', 'Visualize the Hopf bifurcation in the van der Pol equation.']
            ]

articles_url = ['/'+simulations_list[k][0]+'/' for k in range(len(simulations_list))]
articles = [['Simulations', simulations_list], ['Figures', figures_list_for_articles]]

# highlight code
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def pygmentize(file):
    code = open('/home/guillaumecantin/mysite/static/simulation/code/'+file, 'r')
    name = '/home/guillaumecantin/mysite/simulation/templates/simulation/includes/'+file[:-3]+'html'
    output = open(name, 'w')
    code_hl = highlight(code.read(), PythonLexer(), HtmlFormatter())
    output.write(code_hl)
    output.close()
    code.close()
    return 0


#pygmentize('bluesky_code.txt')
#pygmentize('randomgraph_code.txt')
#pygmentize('hamiltonian_code.txt')



# Login view

from django.contrib.auth import authenticate, login, logout

def login_user(request):
    logout(request)
    username = password = ''
    reponse = ''
    islogged = 0
    next = ''
    if request.GET:
        next = escape(request.GET['next'])
    if request.POST:
        username = escape(request.POST['username'])
        password = escape(request.POST['password'])
        try:
            next = escape(request.POST['next'])
        except:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                reponse = "You are logged in, and allowed to access any page of the website."
                islogged = 1
                if next in articles_url:
                    return redirect('http://guillaumecantin.pythonanywhere.com'+next)
                elif next not in articles_url and len(next)>0:
                    logout(request)
                    islogged = 0
                    return render(request, 'simulation/error.html', {'articles': articles, 'islogged': islogged})
                else:
                    return render(request, 'simulation/index.html', {'texte': reponse, 'articles': articles, 'simulations_list': simulations_list, 'figures_list': figures_list, 'islogged': islogged})
            else:
                reponse = "Disabled account."
                islogged = 0
                return render(request, 'simulation/login.html', {'reponse': reponse, 'articles': articles, 'islogged': islogged, 'next': next})
        else:
            reponse = "Invalid login."
            islogged = 0
            return render(request, 'simulation/login.html', {'reponse': reponse, 'articles': articles, 'islogged': islogged, 'next': next})
    else:
        reponse = ''
        islogged = 0
        return render(request, 'simulation/login.html', {'reponse': reponse, 'articles': articles, 'islogged': islogged, 'next': next})


def logout_user(request):
    logout(request)
    islogged = 0
    texte = """You are logged out."""
    return render(request, 'simulation/index.html', {'texte': texte, 'articles': articles, 'simulations_list': simulations_list, 'figures_list': figures_list, 'islogged': islogged})

# View for index
def index(request):
    texte = ""
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    return  render(request, 'simulation/index.html', {'texte': texte, 'articles': articles, 'simulations_list': simulations_list, 'figures_list': figures_list, 'islogged': islogged})

# View for 'about' page
def about(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    return  render(request, 'simulation/about.html', {'articles': articles, 'islogged': islogged})

# View for 'simulations' page
def simulations(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    context = {'articles': articles, 'simulations_list': simulations_list, 'islogged': islogged}
    return render(request, 'simulation/simulations.html', context)

# Views
from .bluesky import bluesky
from .vanderpol import vanderpol
from .hamiltonian import hamiltonian
from .pcrsystem import *
from .poincaresphere import poincaresphere
from .fhn import fhn
from .poincaremap import poincaremap
from .randomgraph import randomgraph
from .pcrnetwork import pcrnetwork
from .bazykin import bazykin
from .tsunami import tsunami


# View for Figure model

def error(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    return render(request, 'simulation/error.html', {'articles': articles, 'islogged': islogged})

from .models import Figure

def figures(request):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    figures_list = Figure.objects.order_by('id')
    context = {'figures_list': figures_list, 'articles': articles, 'islogged': islogged}
    return render(request, 'simulation/figures.html', context)

def figure(request, figure_id):
    if request.user.is_authenticated():
        islogged = 1
    else:
        islogged = 0
    try:
        figure = Figure.objects.get(pk=figure_id)
        code = figure.sourcecode
        figurecode = open('/home/guillaumecantin/mysite/static/simulation/code/figure'+str(figure_id)+'.txt', 'w')
        figurecode.write(code)
        figurecode.close()
        file = 'figure'+str(figure_id)+'.txt'
        pygmentize(file)
        codeurl = 'simulation/includes/figure'+figure_id+'.html'
    except Figure.DoesNotExist:
        return render(request, 'simulation/error.html', {'articles': articles, 'islogged': islogged})
    return render(request, 'simulation/figure.html', {'figure': figure, 'articles': articles, 'islogged': islogged, 'codeurl': codeurl})


