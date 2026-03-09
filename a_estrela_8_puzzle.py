import heapq    #Fila de Prioridade: O menor elemento no topo

class PuzzleState:
    def __init__(self, estado_inicial, estado_anterior=None, movimento="", n_passos=0):    #Construtor
        self.estado_atual    = estado_inicial
        self.estado_anterior = estado_anterior
        self.movimento = movimento  #string: cima, baixo...
        self.n_passos = n_passos    #Custo == g(n)
        self.estado_final = (1, 2, 3, 4, 5, 6, 7, 8, 0)

        #calcula a distancia de manhattan uma única vez
        self.heuristica = self.distancia_manhattan()

    #sensor de direção
    def distancia_manhattan(self):
        distancia = 0 
        for i, peca in enumerate(self.estado_atual):
            if peca != 0:
                posicao_ideal = peca - 1
                atual_lin, atual_col = divmod(i, 3) #Tranforma cordenada lineares em Cartesianas usando mod 3
                ideal_lin, ideal_col = divmod(posicao_ideal, 3)
                #|x1(n) - x2(n)| + |y1(n) - y2(n)| = distancia de manhatan
                distancia += abs(atual_lin - ideal_lin) + abs(atual_col - ideal_col) #abs(garante q o resultado seja positivo)
        return distancia

    def __lt__ (self, other):   #Calculo do custo total estimado (calcular_prioridade)
        #A* (f = g + h) g == o custo do caminho
        # h == A heuritica(Estimativa) 'Resultado do calculo da distancia de manhattan'
        #A biblioteca heapq procura epecificamente pelo nome "__lt__" que significa "less than" --> "menor que"
        return (self. n_passos + self.distancia_manhattan()) < (other.n_passos + other.distancia_manhattan())
    
    def verificador_possibilidades(self):
        lista_estados = []
        p_zero = self.estado_atual.index(0) #pega posição da lista do peça 0
        lin_atual, col_atual = divmod(p_zero, 3) #calcula sua posição dentro da matriz
        lista_de_movimentos = {"cima": (-1, 0), "baixo": (1, 0), "esquerda": (0, -1), "direita": (0, 1)}

        for movimento, (m_lin, m_col) in lista_de_movimentos.items():
            linha, coluna = lin_atual + m_lin, col_atual + m_col    #Aplica cada movimento da lista

            if 0 <= linha < 3 and 0 <= coluna < 3: #se não ultrapassar a matriz o movimento é valido
                estado_atual = list(self.estado_atual)  #Salvando o estado inicial
                novo_p_zero = linha * 3 + coluna    #Transformas cordenadas catesianas em lineares

                #Executando movineto valido
                estado_atual[p_zero], estado_atual[novo_p_zero] = estado_atual[novo_p_zero], estado_atual[p_zero]
                lista_estados.append(PuzzleState(tuple(estado_atual), self, movimento, self.n_passos + 1))
        return lista_estados
    
def verificar_solucao(tabuleiro):
    lista = [peca for peca in tabuleiro if peca != 0]
    inversoes = 0

    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]: #se a peça da esquerda for maior que a da direita
                inversoes +=  1 #´é uma possivel inversão
                
    return inversoes % 2 == 0
        
def resolver_puzzle(estado_inicial):
    ponto_inicial = PuzzleState(tuple(estado_inicial))  #cria o ponto inicial do tabuleiro
    fila_de_prioridade = [ponto_inicial] #inicia a lista de prioridade com o ponto inicial
    estados_conhecidos = {tuple(estado_inicial)}

    while fila_de_prioridade:
        estado_atual = heapq.heappop(fila_de_prioridade)   #calcula a prioridade
        #A* (f = g + h) g == o custo do caminho
        # h == A heuritica(Estimativa) 'Resultado do calculo da distancia de manhattan'

        if estado_atual.estado_atual == (ponto_inicial.estado_final):
            historico = []
            temp = estado_atual
            while temp.estado_anterior is not None:
                historico.append((temp.movimento, temp.estado_atual))   #salva o movimento e o estado atual do tabuleiro
                temp = temp.estado_anterior
            return historico[::-1]  #retorna lista de traz para frente (ordem correta)
        
        for possibilidade in estado_atual.verificador_possibilidades():
            if possibilidade.estado_atual not in estados_conhecidos:
                estados_conhecidos.add(possibilidade.estado_atual)   #adiciona o estado atual em estados conhecidos
                heapq.heappush(fila_de_prioridade, possibilidade)    #adiciona uma nova possibilidade
    return None

def print_tabuleiro(tabuleiro):
    for i in range(0, 9, 3):
        linha = [str(x) if x != 0 else 'X' for x in tabuleiro[i:i+3]]
        print(" ".join(linha))

            
if __name__ == "__main__":
    print("""Digite seu tabuleiro
          exemplo de entrada: 1 2 3 4 0 5 7 8 6""")
    
    try:
        entrada = input("Digite os 9 números separado por espaço: ")
        estado_inicial = list(map(int, entrada.split()))  #Tranforma a string do usuario no em lista
        
        if len(estado_inicial) != 9 or set(estado_inicial) != set(range(9)):    #valida a entrada do usuario
            print("erro...")
        elif not verificar_solucao(estado_inicial):
            print("Tabuleiro impossivel de se resolver")
            print_tabuleiro(estado_inicial)
        else:
            print("Tabuleiro: ")
            print_tabuleiro(estado_inicial)

            print("Calculando Solução...")
            solucao_mais_rapida = resolver_puzzle(estado_inicial)

            if solucao_mais_rapida:
                print(f"Jogo Resolvido com {len(solucao_mais_rapida)} movimentos.")

                for movimento, tabuleiro in solucao_mais_rapida:
                    print(f"Movimento: {movimento}")
                    print_tabuleiro(tabuleiro)
            else:
                print("Jogo sem solução")
    except ValueError:
        print("Entrada invalida.")







                


    

    