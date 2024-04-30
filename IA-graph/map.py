# Este arquivo pode ser main.py
import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt
import folium
from matplotlib.collections import LineCollection

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

class Item(BaseModel):
    lat: float
    long: float

app = FastAPI()

from graph import create_graph
from busca import a_star_search, bfs_search

def plot_path_on_map(lines):
    # Coordenadas de São Carlos para centrar o mapa
    sao_carlos_lat, sao_carlos_lon = -22.0087, -47.8909

    # Criar um mapa centrado em São Carlos
    m = folium.Map(location=[sao_carlos_lat, sao_carlos_lon], zoom_start=14)

    # Adicionar as linhas do caminho ao mapa
    for line in lines:
        folium.PolyLine(line, color='red', weight=5, opacity=0.8).add_to(m)

    return m



def get_lines(G, path):
    # Criar as linhas do caminho
    lines = []
    for i in range(len(path) - 1):
        node_start = path[i]
        node_end = path[i + 1]
            
        missing_nodes = [node for node in path if node not in G.nodes]
        if missing_nodes:
            print("Nós ausentes no grafo:", missing_nodes)
        else:
            print("Todos os nós estão presentes no grafo.")

            # Coleta as coordenadas dos nós
            start_coords = (G.nodes[node_start]['y'], G.nodes[node_start]['x'])  # (lat, lon)
            end_coords = (G.nodes[node_end]['y'], G.nodes[node_end]['x'])  # (lat, lon)

            # Adiciona a linha formada por essas coordenadas ao conjunto de linhas
            lines.append([start_coords, end_coords])

    print(lines)
    return lines

@app.post("/drawMap", response_class=HTMLResponse)
async def print_map(item: Item):

# def main():
    
    # print("Digite 1 para realizar a busca a* ou 2 para largura:")
    # choice = input()

    # print("Digite a latitude e longitude para o ponto de início (formato: lat, lon):")
    # lat, lon = map(float, input().split(','))
    
    lat = item.lat
    lon = item.long

    try:
    
        filepath = 'map.osm'
        G = create_graph(filepath)
        print("Grafo carregado com sucesso.")


        # Encontrar nós de interesse: hospitais, igrejas, abrigos e estações policiais
        types_of_interest = ['hospital', 'church', 'shelter', 'police']
        target_nodes = [node for node, data in G.nodes(data=True) if data.get('amenity') in types_of_interest]
        
        if not target_nodes:
            print("Nenhum local de interesse encontrado.")
            return


        # Encontrar o nó mais próximo das coordenadas fornecidas
        start_node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
        print(f"Nó de início escolhido: {start_node}")


        # Avaliar todos os caminhos para os locais de interesse e encontrar o mais curto
        min_path_cost = float('inf')
        best_path = []
        best_goal_node = None

        for goal_node in target_nodes: # Iterar sobre todos os nós de interesse
            if nx.has_path(G, start_node, goal_node): # Verificar se há um caminho entre os nós

                
                print(f"Calculando caminho para o local de interesse em {goal_node}...")    
                
                # if choice == '1': # A* search
                path, cost = a_star_search(G, start_node, goal_node) 
                # if choice == '2': # BFS search
                #     path, cost = bfs_search(G, start_node, goal_node)
                if cost < min_path_cost: # Atualizar o melhor caminho encontrado
                    min_path_cost = cost
                    best_path = path
                    best_goal_node = goal_node
                print(f"Caminho para {goal_node} com custo {cost}")

        if best_path:
            print("Caminho calculado com sucesso.")
            print("Melhor caminho encontrado:", best_path)
            print(f"De: {start_node} Para: {best_goal_node}")
            print(f"Menor custo do caminho: {min_path_cost}")
            

            lines = get_lines(G, best_path)
            m = plot_path_on_map(lines)
            html_string = m.get_root().render()
            return HTMLResponse(content = html_string, status_code=200)
            
           
        else:
            print("Não foi possível encontrar um caminho para qualquer local de interesse.")

    except Exception as e:
        print("Erro ao executar:", e)

if __name__ == "__main__":
    main()
