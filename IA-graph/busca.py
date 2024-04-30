import heapq

def heuristic(a, b, G):
    # Utiliza a distância euclidiana como heurística
    x1, y1 = G.nodes[a]['y'], G.nodes[a]['x']
    x2, y2 = G.nodes[b]['y'], G.nodes[b]['x']
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def a_star_search(G, start, goal):
    # Fila de prioridades
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        current_priority, current = heapq.heappop(frontier)
        print(f"Processando nó: {current}")

        if current == goal:
            print("Objetivo alcançado. Preparando para sair...")
            break
        
        
        for neighbor in G.neighbors(current):
            edge_data = G.get_edge_data(current, neighbor)
            #print(f"Current edge data from {current} to {neighbor}: {edge_data}")
            if edge_data:
                # Itera sobre cada conexão (caso existam múltiplas arestas entre dois nós)
                for key, attr in edge_data.items():
                    weight = attr.get('weight')
                    if weight is None:
                        weight = 10
                        #print("Weight not set for this connection.")

            new_cost = cost_so_far[current] + weight

            print(f"Checando vizinho {neighbor}, novo custo calculado: {new_cost}")
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal, G)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    current = goal
    while current != start:
        if current in came_from:
            path.append(current)
            current = came_from[current]
        else:
            print("No path found.")
            return [], float('inf')  # Retorna imediatamente se um caminho não pôde ser construído completamente

    path.append(start)
    path.reverse()
    
    print("Fim da busca. Retornando caminho e custo...")

    return path, cost_so_far.get(goal, float('inf'))

