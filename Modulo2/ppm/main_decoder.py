from processors.ppm_processor import PPMProcessor
from processors.ppm_decoder import PPMDecoder
from utils.file_handler import write_string_to_file, FileHandler

def main():
    # Parâmetros
    k_max = 5
    verbose = False
    
    filename = 'G:/Code/compressor-descompressor-de-Shannon-Fano/Modulo2/ppm/data/abracadabra.txt' 

    file = FileHandler()

    text = file.read_file(filename)

    # String de bits codificados
    #encoded_data = "0001001100111000011010100"
    encoded_data = "01101100101010001101101111101000100001101101100000101010011000001101011101011001100001011001111001000110011000000001101100001011110000001001101110011000010000001100010011101001011010101001011100010000101110111000000000001011111101110001001111011100010011001000100001011011000010000110100111000010011010011100110011100100001000111001100100111001001100010011010000000010010010011011101000100111001100000100001111101111100100101110010010011010101110011011000101011001100010111010110111110110001010000101100100001100010110111"
    expected = "abcdacdbadcbaacdbab"
    print(f"Bits codificados: {encoded_data}")
    
    # Decodifica os dados
    decoder = PPMDecoder(k_max, verbose)
    decoded_text = decoder.decode_sequence(text)
    
    print("\n--- Resultado ---")
    print(f"Texto decodificado: {decoded_text}")
    print(f"Texto esperado: {expected}")
    print(f"Correspondência: {'Sim' if decoded_text == expected else 'Não'}")
    
    # Escreve o resultado em um arquivo (opcional)
    file_handler = FileHandler()
    file_handler.write_file('G:/Code/compressor-descompressor-de-Shannon-Fano/Modulo2/ppm/utils/output.txt', decoded_text)
    
if __name__ == "__main__":
    main() 