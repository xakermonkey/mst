from django.shortcuts import render
from .models import *
import numpy as np
import math
import networkx as nx
import pandas as pd
from pyvis.network import Network


def distance_square(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def draw_graph(G, name):
    net = Network(notebook=True, width='100%', height='auto', bgcolor='#222222', font_color='white')
    # net.show_buttons(filter_=['physics', 'interaction', 'edges'])
    net.set_options("""
        var options = {
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": false
          },
          "interaction": {
            "tooltipDelay": 500
          },
          "physics": {
            "repulsion": {
              "centralGravity": 0,
              "springLength": 500,
              "springConstant": 0.565,
              "nodeDistance": 135,
              "damping": 0.49
            },
            "minVelocity": 0.75,
            "solver": "repulsion"
          }
        }
    """)
    net.from_nx(G)
    net.show(f"{name}.html")


def map(request):
    df = pd.read_excel('БД.xlsx')
    lines = list()
    for i in range(df.shape[0]):
        lines.append([df.loc[i]["Широта"], df.loc[i]["Долгота"]])
    print(lines)

    return render(request, "index.html", {'lines': lines})


def statistics(request):
    return render(request, "statistics.html")


def predict(request):
    return render(request, "predict.html")


def create_model(request):
    coord = DetCoords.objects.all()[:100]
    Q = list()

    for i in coord:
        if not i.name.startswith('полоса') and len(DetCoords.objects.filter(address=i.address)) == 2:
            Q.append(DetCoords.objects.filter(address=i.address)[0])
    #         D.append(DetCoords.objects.filter(address=i.address)[1])
    # T = np.zeros((len(Q), len(D)))
    # print(len(Q), len(D))
    # for i in range(len(Q)):
    #     for j in range(len(D)):
    #         if i != j:
    #             T[i][j] = k * float(Detectors.objects.filter(id=Q[i].devid).first().occ) * float(Detectors.objects.filter(id=D[j].devid).first().occ) / float(distance_square(Q[i].lon, Q[i].lat, D[j].lon, D[j].lat))
    # np.save('matrix.npy', T)
    T = np.load('matrix.npy')
    G = nx.MultiDiGraph()
    for i in range(len(Q)):
        G.add_node(Q[i].name)
        for j in range(len(Q)):
            if i != j:
                G.add_edge(Q[i].name, Q[j].name, value=T[i][j], label=str(round(T[i][j], 2)))
    draw_graph(G, 'корреспонденций')
    return render(request, "create_model.html")


def docs(request):
    return render(request, "docs.html")


def location(request):
    return render(request, 'location.html')
