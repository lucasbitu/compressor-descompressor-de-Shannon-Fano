import heapq
import os
import sys


def codificacao_shannon_fano(lista_simbolos):
    """
    Algoritmo de codificação Shannon-Fano.

    """
    # Ordena os símbolos por frequência em ordem decrescente (mais frequentes primeiro)
    lista_simbolos.sort(key=lambda x: x[1], reverse=True)

    def dividir_grupos(simbolos):
        """
        Função recursiva que divide a lista de símbolos em dois grupos e atribui os códigos binários.

        """
        # Caso base: Se restar apenas um símbolo, ele recebe um código vazio
        if len(simbolos) == 1:
            return {simbolos[0][0]: ""}

        # Calcula a soma total das frequências
        total = sum(frequencia for _, frequencia in simbolos)
        acumulado = 0
        indice_divisao = -1

        # Encontra o ponto de divisão onde a soma das frequências é aproximadamente a metade do total
        for i, (_, frequencia) in enumerate(simbolos):
            if (acumulado + frequencia) >= total / 2:
                # Escolhe o melhor ponto de divisão minimizando a diferença das metades
                if abs((acumulado + frequencia - (total / 2))) < abs((acumulado - (total / 2))):
                    indice_divisao = i
                else:
                    indice_divisao = i - 1
                break
            acumulado += frequencia

        # Divide os símbolos em dois grupos
        grupo1 = simbolos[:indice_divisao + 1]
        grupo2 = simbolos[indice_divisao + 1:]

        # Dicionário para armazenar os códigos
        codigos = {}

        # Adiciona prefixo "0" para o primeiro grupo e "1" para o segundo grupo
        for simbolo, codigo in dividir_grupos(grupo1).items():
            codigos[simbolo] = "0" + codigo
        for simbolo, codigo in dividir_grupos(grupo2).items():
            codigos[simbolo] = "1" + codigo

        return codigos

    return dividir_grupos(lista_simbolos)


def comprimir_texto(texto, codigos):
    """
    Converte o texto em um código binário comprimido usando Shannon-Fano.
    """
    codigo_binario = ''.join(codigos[char]for char in texto if char in codigos)

    # Descobre quantos bits sobram para completar um byte
    sobra_bits = len(codigo_binario) % 8
    sobra_bits = 8 - sobra_bits if sobra_bits != 0 else 0

    # Adiciona zeros extras para completar o último byte
    codigo_binario += "0" * sobra_bits

    # Grava o código binário comprimido em um arquivo binário
    with open('comprimido.bin', 'wb') as arquivo:
        for i in range(0, len(codigo_binario), 8):
            byte = int(codigo_binario[i:i+8], 2)  # Converte para inteiro
            arquivo.write(bytes([byte]))  # Escreve no arquivo

    return sobra_bits  # Retorna a quantidade de bits adicionados para alinhamento


def ler_arquivo_comprimido(bits_extra):
    """
    Lê o arquivo binário comprimido e retorna seu conteúdo em formato binário.
    """
    with open('comprimido.bin', 'rb') as arquivo:
        conteudo = arquivo.read()
        conteudo_binario = ''.join(format(byte, '08b') for byte in conteudo)

    # Remove os bits adicionados para alinhamento
    return conteudo_binario[:len(conteudo_binario)-bits_extra]


def descomprimir_texto(codigo_binario, codigos):
    """
    Descomprime um código binário gerado pelo algoritmo de Shannon-Fano de volta ao texto original.

    """
    # Inverte o dicionário de códigos para facilitar a decodificação {código_binário: símbolo}
    codigos_invertidos = {v: k for k, v in codigos.items()}

    texto_decodificado = ""  # Armazena o texto reconstruído
    codigo_temp = ""  # Acumula os bits para identificar um caractere

    # Percorre cada bit do código binário
    for bit in codigo_binario:
        codigo_temp += bit  # Adiciona o bit ao código temporário

        # Verifica se o código temporário corresponde a um símbolo no dicionário
        if codigo_temp in codigos_invertidos:
            # Adiciona o símbolo correspondente ao texto
            texto_decodificado += codigos_invertidos[codigo_temp]
            codigo_temp = ""  # Reinicia o código temporário para o próximo símbolo

    return texto_decodificado


def calcular_taxa_compressao(texto_original, codigo_binario):
    """
    Calcula a taxa de compressão do texto original em relação ao binário comprimido.
    """
    bits_totais = len(codigo_binario)  # Total de bits após compressão
    # Número de caracteres no texto original
    numero_simbolos = len(texto_original)
    bits_por_simbolo = bits_totais / numero_simbolos
    taxa_compressao = 5 / bits_por_simbolo  # Calcula a taxa de compressão

    return taxa_compressao


def verificar_tamanho_arquivos():
    """
    Verifica o tamanho dos arquivos gerados e exibe o resultado.
    """
    arquivo_original = "original.txt"
    arquivo_comprimido = "comprimido.bin"

    tamanho_original = os.path.getsize(
        arquivo_original) if os.path.exists(arquivo_original) else 0
    tamanho_comprimido = os.path.getsize(
        arquivo_comprimido) if os.path.exists(arquivo_comprimido) else 0

    print(f"Tamanho do arquivo original: {tamanho_original} bytes")
    print(f"Tamanho do arquivo comprimido: {tamanho_comprimido} bytes")


def salvar_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, "wb") as arquivo:
        arquivo.write(conteudo)


# Lista de símbolos com suas frequências na língua portuguesa
simbolos_frequencias = [
    (' ', 17.00), ('E', 14.63), ('A', 13.72), ('O', 10.73), ('S', 7.81),
    ('R', 6.53), ('I', 6.18), ('N', 5.05), ('D', 4.99), ('M', 4.74),
    ('U', 4.63), ('T', 4.34), ('C', 3.88), ('L', 2.78), ('P', 2.52),
    ('V', 1.67), ('G', 1.30), ('H', 1.28), ('Q', 1.20), ('B', 1.04),
    ('F', 1.02), ('Z', 0.47), ('J', 0.40), ('X', 0.27), ('K', 0.02),
    ('W', 0.01), ('Y', 0.01)
]

# Gera os códigos Shannon-Fano
codigos = codificacao_shannon_fano(simbolos_frequencias)

# Texto para teste
texto_original = "LUCAS FREITAS BITU SATIRO CRATO CEARA"

# Compressão
bits_extra = comprimir_texto(texto_original, codigos)
texto_comprimido = ler_arquivo_comprimido(bits_extra)
texto_descomprimido = descomprimir_texto(texto_comprimido, codigos)

# Salvar o texto original
salvar_arquivo("original.txt", texto_original.encode())

# Calcular taxa de compressão
taxa_compressao = calcular_taxa_compressao(texto_original, texto_comprimido)

# Exibir resultados
print("Códigos Shannon-Fano:")
for simbolo, codigo in codigos.items():
    print(f"{simbolo}: {codigo}")
print("\nTexto original:", texto_original)
print("Texto comprimido:", texto_comprimido)
print("Texto descomprimido:", texto_descomprimido)
print("Taxa de compressão:", taxa_compressao)
# Chamada da função para exibir os tamanhos
verificar_tamanho_arquivos()
