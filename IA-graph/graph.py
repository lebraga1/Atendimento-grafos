import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

def create_graph(filepath):
    # Carrega o grafo como direcional e converte para não-direcional
    G = ox.graph_from_xml(filepath, simplify=True)
    G = G.to_undirected()
    

    # Atribuir pesos às arestas
    for u, v, data in G.edges(data=True):
        if 'length' in data:
            data['weight'] = data['length']
        else:
            data['weight'] = 10  # Valor padrão se não houver 'length'

    # Carregar e processar hospitais para adicionar ao grafo
    gdf = ox.features_from_xml(filepath)
    hospitals = gdf[gdf['amenity'] == 'hospital'].dropna(subset=['geometry'])

    for idx, row in hospitals.iterrows(): # Itera sobre os hospitais

        geom = row.geometry # Obtém a geometria do hospital
        x, y = (geom.centroid.x, geom.centroid.y) if isinstance(geom, Polygon) else (geom.x, geom.y) # Obtém as coordenadas do hospital

        if pd.isna(x) or pd.isna(y): # Se as coordenadas não estiverem definidas,
            continue

        nearest_node = ox.distance.nearest_nodes(G, x, y) # Encontra o nó mais próximo ao hospital
        G.add_node(idx, x=x, y=y, osmid=idx, amenity='hospital', node_weight=10) # Adiciona o hospital como nó ao grafo
        distance = ox.distance.great_circle(G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x'], y, x) # Calcula a distância entre o hospital e o nó mais próximo
        G.add_edge(idx, nearest_node, weight=distance) # Adiciona uma aresta entre o hospital e o nó mais próximo

    return G


