import unicodedata
import re


def preprocess_text(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Substituir quebras de linha por espaços
    text = text.replace("\n", " ")

    # Remover acentos e normalizar caracteres
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Manter apenas letras minúsculas e espaços
    text = text.lower()
    text = re.sub(r"[^a-z ]", "", text)

    # Remover espaços extras
    text = re.sub(r"\s+", " ", text).strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Texto pré-processado salvo em: {output_path}")


# Caminhos dos arquivos de entrada e saída
input_file = "data/MemoriasPostumas.txt"
output_file = "data/MemoriasPostumas_preprocessado.txt"

# Executar pré-processamento
preprocess_text(input_file, output_file)
