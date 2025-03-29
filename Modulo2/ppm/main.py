from app import PPMApp

def main():
    # Valores configuráveis
    K_MAX = 1
    INPUT_FILE = '/Users/moises/Documents/iti/Modulo2/ppm/data/abracadabra.txt'
    
    # Criação e execução da aplicação
    app = PPMApp(K_MAX)
    
    encoded_sequence = app.run(INPUT_FILE)
    print(encoded_sequence)
    # Acesso ao modelo para análise ou debug
    ppm_model = app.save_model_structure_to_file("model.json")
    
    # Exemplo de como obter probabilidades de um contexto específico
    # if len(app.processor.discarded_chars) > 0:
    #     context_str = app.processor.discarded_chars[0]
    #     print(app.processor.discarded_chars)
    #     probabilities = ppm_model.get_probabilities(context_str, 1)
    #     print(f"Probabilidades para contexto '{context_str}' no nível k=1:")
    #     for char, prob in probabilities.items():
    #         print(f"  {char}: {prob:.4f}")

if __name__ == "__main__":
    main() 