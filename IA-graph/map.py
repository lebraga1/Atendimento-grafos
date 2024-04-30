import networkx as nx # Biblioteca para trabalhar com grafos
import folium # Biblioteca para visualização de mapas
import time # Biblioteca para medir o tempo de execução
from fastapi import FastAPI # Biblioteca para criar APIs
from pydantic import BaseModel # Biblioteca para validação de dados
from fastapi.responses import HTMLResponse # Biblioteca para retornar respostas HTML
import osmnx as ox # Biblioteca para trabalhar com mapas

class Item(BaseModel): # Classe para validar os dados de entrada
    lat: float
    long: float

app = FastAPI() # Criar uma instância da API

from graph import create_graph # Importar a função para criar o grafo
from busca import a_star_search, bfs_search # Importar as funções de busca







# Função para medir o desempenho de um algoritmo de busca a partir de um menor caminho conhecido
def measure_performance(G, start_node, goal_node, search_function):
    start_time = time.time()
    path, cost, nodes_expanded = search_function(G, start_node, goal_node)
    end_time = time.time()
    duration = end_time - start_time
    return duration, cost, nodes_expanded, path



# Função para plotar o caminho encontrado no mapa
def plot_path_on_map(lines):


    # Coordenadas de São Carlos para centrar o mapa
    sao_carlos_lat, sao_carlos_lon = -22.0087, -47.8909

    # Criar um mapa centrado em São Carlos
    m = folium.Map(location=[sao_carlos_lat, sao_carlos_lon], zoom_start=14)

    # Adicionar as linhas do caminho ao mapa
    for line in lines:
        folium.PolyLine(line, color='red', weight=5, opacity=0.8).add_to(m)

    return m


# Função para obter as coordenadas dos nós do caminho
def get_coord(G, path):
    lines = []
    for i in range(len(path) - 1): # Iterar sobre os nós do caminho
        node_start = path[i]
        node_end = path[i + 1]
            
        missing_nodes = [node for node in path if node not in G.nodes]

        if missing_nodes:
            print("Nós ausentes no grafo:", missing_nodes)
        else:
            #print("Todos os nós estão presentes no grafo.") #print de debug no terminal

            # Coleta as coordenadas dos nós
            start_coords = (G.nodes[node_start]['y'], G.nodes[node_start]['x'])  # (lat, lon)
            end_coords = (G.nodes[node_end]['y'], G.nodes[node_end]['x'])  # (lat, lon)

           # Adiciona as coordenadas ao caminho
            lines.append([start_coords, end_coords])

    #print(lines) #print de debug no terminal

    return lines


@app.post("/drawMap", response_class=HTMLResponse) # Rota para desenhar o mapa
async def print_map(item: Item): # Função para desenhar o mapa

#def main():
    
    #print("Digite 1 para realizar a busca a* ou 2 para largura:")
    #choice = input()

    #print("Digite a latitude e longitude para o ponto de início (formato: lat, lon):")
    #lat, lon = map(float, input().split(','))
    
    lat = item.lat 
    lon = item.long

    try:
    
        filepath = 'map.osm' # Caminho para o arquivo OSM do mapa
        G = create_graph(filepath) # Criar o grafo a partir do arquivo OSM
        
        #print("Grafo carregado com sucesso.") 

        # Encontrar nós de interesse: hospitais, igrejas, abrigos e estações policiais
        types_of_interest = ['hospital', 'church', 'shelter', 'police']
        target_nodes = [node for node, data in G.nodes(data=True) if data.get('amenity') in types_of_interest] 
        
        if not target_nodes:
            print("Nenhum local de interesse encontrado.")
            return


        # Encontrar o nó mais próximo das coordenadas fornecidas
        start_node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
        #print(f"Nó de início escolhido: {start_node}")


        # Avaliar todos os caminhos para os locais de interesse e encontrar o mais curto
        min_path_cost = float('inf')
        best_path = []
        best_goal_node = None
        
        #start_time = time.time()
        #nodes_expanded = 0

        for goal_node in target_nodes: # Iterar sobre todos os nós de interesse

            #if nx.has_path(G, start_node, goal_node): # Verificar se há um caminho entre os nós, importante para debug no terminal
                
            #print(f"Calculando caminho para o local de interesse em {goal_node}...")    
                
            #if choice == '1': # A* search
            path, cost, nodes_exp = a_star_search(G, start_node, goal_node)
            #nodes_expanded+=nodes_exp # Contar o número de nós expandidos

            #if choice == '2': # BFS search
            #path, cost, nodes_exp = bfs_search(G, start_node, goal_node)
            #nodes_expanded+=nodes_exp 

            if cost < min_path_cost: # Atualizar o melhor caminho encontrado
                min_path_cost = cost
                best_path = path
                best_goal_node = goal_node
            #print(f"Caminho para {goal_node} com custo {cost}")

        #end_time = time.time()
        #tot_time = end_time - start_time


        #print(f"Tempo total de execução: {tot_time}s")
        #print("Costs: ", min_path_cost)
        #print("Nodes expanded: ", nodes_expanded)

        if best_path:
            #print("Caminho calculado com sucesso.")
            #print("Melhor caminho encontrado:", best_path)
            #print(f"De: {start_node} Para: {best_goal_node}")
            #print(f"Menor custo do caminho: {min_path_cost}")

            #duration_a_star, cost_a_star, nodes_expanded_a_star, path_a_star = measure_performance(G, start_node, best_goal_node, a_star_search)
            #duration_bfs, cost_bfs, nodes_expanded_bfs, path_bfs = measure_performance(G, start_node, best_goal_node, bfs_search)

            #print(f"A* Duration: {duration_a_star}s, Cost: {cost_a_star}, Nodes Expanded: {nodes_expanded_a_star}")
            #print(f"BFS Duration: {duration_bfs}s, Cost: {cost_bfs}, Nodes Expanded: {nodes_expanded_bfs}")
            
            lines = get_coord(G, best_path)
            m = plot_path_on_map(lines)
        
            #m.save('path.html')  # Salva o mapa em um arquivo HTML]

            html_string = m.get_root().render() # Renderiza o mapa em HTML
            return HTMLResponse(content = html_string, status_code=200) # Retorna o mapa em HTML
            
           
        else:
            print("Não foi possível encontrar um caminho para qualquer local de interesse.")

    except Exception as e:
        print("Erro ao executar:", e)

#if __name__ == "__main__":
#    main()
