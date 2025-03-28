from collections import defaultdict
import string

# Quantidade máxima de K's 2 para abracadabra e 5 para projeto
K_max = 2

# cria dicionário aninhado com contador de inteiros interno , depois adicionar probabilidade ou calcular fora da tabela
def nested_defaultdict():
    # Usando defaultdict(int) em vez de nested_defaultdict
    return defaultdict(lambda: defaultdict(int))

# Função para ler arquivo
def read_file_to_string(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Lê arquivo 
# file_content = read_file_to_string('data/MemoriasPostumas_preprocessado.txt')
file_content = read_file_to_string('data/abracadabra.txt')

# Lista para descarte de caracteres
discarded_chars = []

# lista para caracteres ignorados
ignore_chars = []

# array codificação

# Criando o dicionário para armazenar os contextos de k = -1 até k_max
ppm_structure = {k: nested_defaultdict() for k in range(-1, K_max+1)}

# constrói k = -1 , com alfabeto 
for letra in string.ascii_lowercase:
    ppm_structure[-1]["NO_CONTEXT"][letra] = 1
# adiciona o espaço também
ppm_structure[-1]["NO_CONTEXT"][" "] = 1

# Iterando pelos caracteres do texto
for char in file_content:
    # print(char)
    elemento_encontrado = False
    # pilha vazia ?
    if not discarded_chars:
        # chama função codificar para k = -1

        # remove elemento de k = -1
        del ppm_structure[-1]["NO_CONTEXT"][char]

        # incrementa o elemento e ro em k = 0
        ppm_structure[0]["NO_CONTEXT"][char] += 1
        ppm_structure[0]["NO_CONTEXT"]['ç'] += 1
    else:
        TAMANHO_ARRAY_DESCARTADOS = len(discarded_chars)

        # DEFINE K BASEADO NA PILHA DE DESCARTES
        for k in range(TAMANHO_ARRAY_DESCARTADOS, -2, -1):
            # print(k)
            #  se k = 0 OU K = -1 , não tem contexto (FLAG NO_CONTEXT)
            if k > 0:
                contexto = ''.join(discarded_chars[:k])
            else:
                contexto = "NO_CONTEXT"
    
            # Verifica no K correspondente se o contexto já existe no dicionário.
            if contexto in ppm_structure[k]:
                # print(contexto)
                # print("sim")
                # verifica se o caracter existe dentro do contexto
                if char in ppm_structure[k][contexto]:
                    # print("sim caracter em contexto")
                    # está em k = -1 ?
                    if k == -1:
                        # print("está em k = -1")
                        # chama função codificar para k = -1

                        # remove elemento de k = -1
                        del ppm_structure[k][contexto][char]

                        # não precisa incrementar o ro e o elemento por que eles já foram incrementados quando k era igual a 0
                        # ppm_structure[0]["NO_CONTEXT"]['ç'] += 1
                        # ppm_structure[0]["NO_CONTEXT"][char] += 1
                    else:
                        # print("não está em k = -1")
                        if elemento_encontrado == False:
                            # print("caracter encontrado a primeira vez")
                            # chama função codificar com array ignorados(sem o ro dentro de array ignorados)
                            pass
                        else:
                            # print("caracter já foi encontrado")
                            pass

                        # incremente o elemento encontrado dentro dos contextos
                        ppm_structure[k][contexto][char] += 1
                        elemento_encontrado = True
                else:
                    # print("caracter não está em contexto")
                    if k == -1:
                        # print("k == -1")
                        pass
                    else:
                        # adiciona a array ignorados
                        elementos = set(ppm_structure[k][contexto].keys())
                        ignore_chars = list(set(ignore_chars) | elementos)

                        if elemento_encontrado == False:
                            # print("caracter não foi encontrado ainda")
                            
                            # chama função codificar para ro

                            # incrementa ro
                            ppm_structure[k][contexto]['ç'] += 1
                            pass
                        else:
                            # print("caracter já foi encontrado")
                            pass

                        # adiciona elemento ao contexto
                        ppm_structure[k][contexto][char] += 1
            else:
                # print("não")
                # adiciona o contexto que não foi encontrado junto do caracter e ro
                ppm_structure[k][contexto][char] += 1
                ppm_structure[k][contexto]['ç'] += 1


    # adiciona a pilha de descarte
    if len(discarded_chars) == K_max:
        discarded_chars.pop()  # Remove o último elemento
    discarded_chars.insert(0, char)

    # print("array descartados ")
    # print(discarded_chars)

    # print("array ignorados ")
    # print(ignore_chars)

    # esvazia array ignora
    ignore_chars = []

    # verifica ro pra saber onde precisa exluir
    # exemplo k = -1 vazio exclue ro de k=0
    # ideia : verifica se no k correspodente e no contexto correspondente já existem todas as letras do alfabeto e o espaço se tiver elimina

    # falta incrementar array codificação e probabilidades

    print(ppm_structure)
