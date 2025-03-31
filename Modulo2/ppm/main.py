from app import PPMApp
import time


def comprimir_texto(codigo_binario):
    """
    Converte o texto em um código binário comprimido usando Shannon-Fano.
    """
    # Descobre quantos bits sobram para completar um byte
    sobra_bits = len(codigo_binario) % 8
    sobra_bits = 8 - sobra_bits if sobra_bits != 0 else 0

    # Adiciona zeros extras para completar o último byte
    codigo_binario += "0" * sobra_bits

    # Grava o código binário comprimido em um arquivo binário
    with open('/Users/lucas/OneDrive/Documentos/lucas/pdi/ITI/PrimeiroProjetoITI/Modulo2/ppm/data/comprimido.bin', 'wb') as arquivo:
        for i in range(0, len(codigo_binario), 8):
            byte = int(codigo_binario[i:i+8], 2)  # Converte para inteiro
            arquivo.write(bytes([byte]))  # Escreve no arquivo

    return sobra_bits  # Retorna a quantidade de bits adicionados para alinhamento


def ler_arquivo_comprimido(bits_extra):
    """
    Lê o arquivo binário comprimido e retorna seu conteúdo em formato binário.
    """
    with open('/Users/lucas/OneDrive/Documentos/lucas/pdi/ITI/PrimeiroProjetoITI/Modulo2/ppm/data/comprimido.bin', 'rb') as arquivo:
        conteudo = arquivo.read()
        conteudo_binario = ''.join(format(byte, '08b') for byte in conteudo)

    # Remove os bits adicionados para alinhamento
    return conteudo_binario[:len(conteudo_binario)-bits_extra]


def main():
    # Valores configuráveis
    K_MAX = 5
    INPUT_FILE = '/Users/lucas/OneDrive/Documentos/lucas/pdi/ITI/PrimeiroProjetoITI/Modulo2/ppm/data/MemoriasPostumas_preprocessado.txt'

    # Criação e execução da aplicação
    app = PPMApp(K_MAX)

    inicio = time.time()
    encoded_sequence = app.run(INPUT_FILE)
    fim = time.time()
    print(encoded_sequence)
    string_encoded = ''
    entropia = 0
    # tamanho da mensagem original
    N = len(app.text)

    for i in encoded_sequence:
        string_encoded += i[3]
        entropia += i[5]

    # código da mensagem
    # print(f"Encoded antes da compressão: {string_encoded}")

    # comprime o código em um arquivo binário
    bits_extra = comprimir_texto(string_encoded)
    codigo_descomprimido = ler_arquivo_comprimido(bits_extra)
    # print(f"encoded depois da descompressão: {codigo_descomprimido}")

    if string_encoded == codigo_descomprimido:
        print("A descompreção é IGUAL ao código comprimido")
    else:
        print("A descompreção é DIFERENTE ao código comprimido")

    print(f"para k: {K_MAX}")

    # tempo de compressão
    print(f"Tempo de compressão: {fim - inicio:.4f} segundos")

    # entropia
    print(f"Entropia: {abs(entropia/N)}")
    # comprimento médio
    print(f"Comprimento Médio {(len(string_encoded)/(len(app.text)))}")

    # Acesso ao modelo para análise ou debug
    ppm_model = app.save_model_structure_to_file("model.json")


if __name__ == "__main__":
    main()
