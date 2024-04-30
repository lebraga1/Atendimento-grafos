import heapq # Para a fila de prioridades

def heuristic(a, b, G):
    # Utiliza a distância euclidiana como heurística
    x1, y1 = G.nodes[a]['y'], G.nodes[a]['x']
    x2, y2 = G.nodes[b]['y'], G.nodes[b]['x']
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def a_star_search(G, start, goal):
    
    frontier = [] # Fila de prioridades
    heapq.heappush(frontier, (0, start)) # Adiciona o nó inicial à fila
    came_from = {start: None} 
    cost_so_far = {start: 0}
    nodes_expanded = 0
    
    while frontier:
        current_priority, current = heapq.heappop(frontier) # Remove o nó com a menor prioridade
        nodes_expanded += 1  # Incrementa a cada nó processado
        #print(f"Processando nó: {current}")

        if current == goal:
            #print("Objetivo alcançado. Preparando para sair...")
            break
        
        
        for neighbor in G.neighbors(current): # Itera sobre os vizinhos do nó atual

     
            edge_data = G.get_edge_data(current, neighbor) # Obtém os dados da aresta entre os nós
            #print(f"Current edge data from {current} to {neighbor}: {edge_data}")

            if edge_data: # Se houver conexão entre os nós

                # Itera sobre cada conexão (caso existam múltiplas arestas entre dois nós)
                for key, attr in edge_data.items():
                    weight = attr.get('weight')
                    if weight is None: # Se o peso não estiver definido
                        weight = 10
                        #print("Weight not set for this connection.")

            new_cost = cost_so_far[current] + weight # Calcula o novo custo para alcançar o vizinho

            #print(f"Checando vizinho {neighbor}, novo custo calculado: {new_cost}")

            # Se o vizinho não foi visitado ou se o novo custo é menor que o custo anterior
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost # Atualiza o custo para alcançar o vizinho
                priority = new_cost + heuristic(neighbor, goal, G) 
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    path = [] 
    current = goal
    while current != start: # Reconstrói o caminho a partir do nó final
        if current in came_from:
            path.append(current)
            current = came_from[current]
        else:
            print("No path found.")
            return [], float('inf')  # Retorna imediatamente se um caminho não pôde ser construído completamente

    path.append(start)
    path.reverse()
    
    #print("Fim da busca. Retornando caminho e custo...")

    return path, cost_so_far.get(goal, float('inf')), nodes_expanded


def bfs_search(G, start, goal, max_depth=14): 

    def bfs_with_depth_limit(start, depth_limit): # Função auxiliar para a busca em largura com limite de profundidade
        queue = [(start, [start], 0)]  
        nodes_expanded = 0  

        while queue: # Enquanto houver nós na fila

            current, path, cost = queue.pop(0) 
            nodes_expanded += 1  
           # print(f"Processando nó: {current}, Profundidade Atual: {len(path) - 1}")
            if current == goal:
                #print("Objetivo alcançado. Preparando para sair...")
                return path, cost, nodes_expanded
            
            if len(path) - 1 < depth_limit:  # Se a profundidade atual for menor que o limite
                for neighbor in G.neighbors(current): # Itera sobre os vizinhos do nó atual
                    if neighbor not in path:  # Se o vizinho não foi visitado
                        edge_data = G.get_edge_data(current, neighbor) # Obtém os dados da aresta entre os nós
                            #print(f"Current edge data from {current} to {neighbor}: {edge_data}")
                        if edge_data: # Se houver conexão entre os nós
                            # Itera sobre cada conexão (caso existam múltiplas arestas entre dois nós)
                            for key, attr in edge_data.items():
                                weight = attr.get('weight')
                                if weight is None:
                                    weight = 10
                        #print("Weight not set for this connection.")

                        queue.append((neighbor, path + [neighbor], cost + weight)) # Adiciona o vizinho à fila

        return [], float('inf'), nodes_expanded  # Retorna imediatamente se um caminho não pôde ser construído completamente

    for depth in range(max_depth + 1): # Itera sobre os limites de profundidade
        #print(f"Tentando com limite de profundidade: {depth}")
        path, cost, nodes_expanded = bfs_with_depth_limit(start, depth)
        if path: # Se um caminho foi encontrado 
            return path, cost, nodes_expanded

    print(f"Nenhum caminho encontrado dentro do limite de profundidade de {max_depth}.")
    return [], float('inf'), 0