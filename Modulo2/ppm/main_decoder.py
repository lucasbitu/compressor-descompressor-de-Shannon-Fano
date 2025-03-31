from processors.ppm_processor import PPMProcessor
from processors.ppm_decoder import PPMDecoder
from utils.file_handler import write_string_to_file

def main():
    # Parâmetros
    k_max = 1
    verbose = True
    
    # String de bits codificados
    encoded_data = "0001001100111000011010100"
    
    print(f"Bits codificados: {encoded_data}")
    
    # Decodifica os dados
    decoder = PPMDecoder(k_max, verbose)
    decoded_text = decoder.decode_sequence(encoded_data)
    
    print("\n--- Resultado ---")
    print(f"Texto decodificado: {decoded_text}")
    print(f"Texto esperado: abracadabra")
    print(f"Correspondência: {'Sim' if decoded_text == 'abracadabra' else 'Não'}")
    
    # Escreve o resultado em um arquivo (opcional)
    # file_handler = FileHandler()
    #file_handler.write_file('ppm/data/decoded_output.txt', decoded_text)
    
if __name__ == "__main__":
    main() 