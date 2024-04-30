import osmnx as ox
import networkx as nx
import random
from graph import create_graph
from busca import a_star_search

def main():
    try:
        filepath = 'map.osm'
        G = create_graph(filepath)
        print("Grafo carregado com sucesso.")

        # Verifica se o grafo é direcionado e escolhe a função apropriada
        if G.is_directed():
            component_function = nx.strongly_connected_components
        else:
            component_function = nx.connected_components

        # Encontrar todas as estações policiais
        police_nodes = [node for node, data in G.nodes(data=True) if data.get('amenity') == 'hospital']
        if not police_nodes:
            print("Nenhuma estação policial encontrada.")
            return

        # Selecionar um goal_node aleatório entre as estações policiais
        goal_node = random.choice(police_nodes)
        print("Nó de destino selecionado:", goal_node)

        # Determinar componentes conectados e escolher um start_node do mesmo componente
        start_node = random.choice(list(G.neighbors(goal_node)))
        print("Nó de origem selecionado:", start_node)

        print(list(G.neighbors(goal_node)))

        #if not nx.has_path(G, start_node, goal_node):
          #  print("Não há caminho entre os nós de origem e destino.")
        #else:
        print("Existe um caminho. Executando A*...")
        path, cost = a_star_search(G, start_node, goal_node)
        print("Caminho calculado com sucesso.")
        print("Caminho encontrado:", path)
        print("De:", start_node, "Para:", goal_node)
        print("Custo do caminho:", cost)

    except Exception as e:
        print("Erro ao executar:", e)

if __name__ == "__main__":
    main()

