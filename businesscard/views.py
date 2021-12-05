from django.shortcuts import render
from .models import *
import numpy as np
import random
import networkx as nx
import pandas as pd
from pyvis.network import Network
from datetime import datetime, timedelta


def distance_square(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def draw_graph(G, name):
    net = Network(notebook=True, width='100%', height='auto', bgcolor='#222222', font_color='black')
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
    fvf = list()
    for i in Fvf.objects.all()[:10]:
        item = dict()
        item['coord'] = [float(i.lat), float(i.lon)]
        item['address'] = i.address
        item['tail'] = list()
        for j in Fvf.objects.all()[:5]:
            item['tail'].append({
                'id': int(j.recid),
                'camera': j.camera,
                'speed': float(j.speed) if j.speed else 0,
                'date': j.date.isoformat(),
                'lanes': int(j.lanes) if j.lanes else 0,
            })
        fvf.append(item)


    df = pd.read_excel('БД.xlsx')
    lines = list()
    k = 1
    for i in range(1, df.shape[0]):
        item = dict()
        if random.randint(0, 10) == 1:
            if df.loc[i]['Год'] < 2000:
                item['color'] = '#ff0020'
            elif df.loc[i]['Год'] < 2005:
                item['color'] = '#ffaa00'
            else:
                item['color'] = '#00ff44'
            item['coord'] = [[df.loc[i - k]["Широта"], df.loc[i - k]["Долгота"]],
                             [df.loc[i]["Широта"], df.loc[i]["Долгота"]]]
            k = 1
            lines.append(item)
        else:
            k += 1

    data = list()
    for i in DetCoords.objects.all()[:50]:
        item = dict()
        item['name'] = i.name
        item['address'] = i.address
        item['lanes'] = int(i.lanes)
        item['date'] = i.date
        item['coord'] = [float(i.lat), float(i.lon)]
        data.append(item)

    return render(request, "index.html", {'lines': lines, 'data': data, 'fvf': fvf})


def statistics(request):
    data = list()

    for i in Detectors.objects.all()[:100]:
        data.append(
            [DetCoords.objects.filter(devid=i.id).first().name, DetCoords.objects.filter(devid=i.id).first().address,
             i.completeness, i.speed, i.occ, i.utilisation, i.volume])

    return render(request, "statistics.html", {'data': data})


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
    N = dict()
    G = nx.Graph()
    print(len(Q))
    for i in range(len(Q) - 30):
        G.add_node(Q[i].name)
        N[Q[i].name] = T[i][:-30]
        for j in range(len(Q) - 30):
            if i != j:
                G.add_edge(Q[i].name, Q[j].name, value=T[i][j], label=str(round(T[i][j], 2)))

    draw_graph(G, 'корреспонденций')
    return render(request, "create_model.html", {'N': N, 'Q': Q[:-30], 'range': range(len(Q) - 30)})


def docs(request):
    return render(request, "docs.html")


def location(request):
    return render(request, 'location.html')
