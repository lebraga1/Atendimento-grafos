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

        # Encontrar todas as estações policiais
        police_nodes = [node for node, data in G.nodes(data=True) if data.get('amenity') == 'hospital']
        if not police_nodes:
            print("Nenhuma estação policial encontrada.")
            return

        # Escolher um start_node aleatório
        start_node = random.choice(list(G.nodes()))
        print(f"Nó de início escolhido: {start_node}")

        # Avaliar todos os caminhos para as estações policiais e encontrar o mais curto
        min_path_cost = float('inf')
        best_path = []
        best_goal_node = None

        for goal_node in police_nodes:
            if nx.has_path(G, start_node, goal_node):
                print(f"Calculando caminho para a estação policial em {goal_node}...")
                path, cost = a_star_search(G, start_node, goal_node)
                if cost < min_path_cost:
                    min_path_cost = cost
                    best_path = path
                    best_goal_node = goal_node
                print(f"Caminho para {goal_node} com custo {cost}")

        if best_path:
            print("Caminho calculado com sucesso.")
            print("Melhor caminho encontrado:", best_path)
            print(f"De: {start_node} Para: {best_goal_node}")
            print(f"Menor custo do caminho: {min_path_cost}")
        else:
            print("Não foi possível encontrar um caminho para qualquer estação policial.")

    except Exception as e:
        print("Erro ao executar:", e)

if __name__ == "__main__":
    main()
