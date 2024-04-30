# SuaAjuda

SuaAjuda é uma aplicação destinada a mulheres vítimas de violência, oferecendo a menor rota para abrigos ou serviços de apoio próximos. Utilizando algoritmos de busca como A* e busca em largura, integrados ao mapeamento do OpenStreetMap, a aplicação garante eficiência e discrição no acesso.


## Tecnologias Utilizadas

- Python
- OSMnx
- NetworkX
- Folium para visualização de mapas

## Instalação

### Pré-requisitos

- Python 3.x
- Conda (Ubuntu) 

### Ubuntu

1. Clone o repositório e prepare o ambiente:
   ```bash
   git clone https://github.com/lebraga1/Atendimento-grafos.git
   cd Atendimento-grafos
   conda create --name safepath python=3.x
   conda activate safepath
   conda install -c conda-forge osmnx networkx folium fastapi uvicorn

2. Em seguida, vá ate a raiz da busca IA-graph  e iniciar a aplicação:
    ```bash
    uvicorn map:app --reload

3. Acesse a raiz do backend e faça:
    ```bash
    npm install
    npm start

então acesse em http://localhost:3000 

