import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

def create_graph(filepath):
    G = ox.graph_from_xml(filepath, simplify=True)

    for u, v, data in G.edges(data=True):
        if 'length' in data:
            data['weight'] = data['length']
            #print(f"Edge from {u} to {v}: length = {data['length']}, weight = {data['weight']}")
        else:
            data['weight'] = 10 

        

    gdf = ox.features_from_xml(filepath)
    police_stations = gdf[gdf['amenity'] == 'hospital'].dropna(subset=['geometry'])

    for idx, row in police_stations.iterrows():
        geom = row.geometry
        if isinstance(geom, Polygon):
            x, y = geom.centroid.x, geom.centroid.y
        elif isinstance(geom, Point):
            x, y = geom.x, geom.y
        else:
            x, y = geom.centroid.x, geom.centroid.y

        if pd.isna(x) or pd.isna(y):
            continue

        nearest_node = ox.distance.nearest_nodes(G, x, y)
        G.add_node(idx, x=x, y=y, osmid=idx, amenity='hospital', node_weight=10)  # Adiciona um peso ao nó
        distance = ox.distance.great_circle(G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x'], y, x)
        G.add_edge(idx, nearest_node, weight=distance)  # Usa a distância como peso

   # ox.plot_graph(G)
    return G
