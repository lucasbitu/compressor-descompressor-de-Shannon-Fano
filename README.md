# 📦 Compactadores de Shannon-Fano e PPM-Huffman

Este repositório contém a implementação de dois algoritmos clássicos de compressão de dados desenvolvidos como parte dos trabalhos práticos da disciplina **Introdução à Teoria da Informação** (2024.2) da Universidade Federal da Paraíba.

## 🧠 Sobre os Trabalhos

### 🔹 Trabalho 1 — Shannon-Fano Estático Não Contextual

Desenvolvemos um compressor e descompressor baseado no algoritmo de Shannon-Fano, utilizando uma tabela fixa de frequências da língua portuguesa. O texto de entrada é pré-processado para conter apenas os caracteres da tabela, e espaços repetidos são eliminados.

- **Entrada**: Texto contendo nome completo, cidade e estado de nascimento.
- **Saída**: Arquivo comprimido e descomprimido, com cálculo da razão de compressão.
- **Objetivo**: Demonstrar compressão básica baseada em probabilidade simbólica estática.

### 🔹 Trabalho 2 — PPM-Huffman

Implementamos um compressor-descompressor utilizando o algoritmo PPM (Prediction by Partial Matching) combinado com Huffman, aplicando-o ao texto "Memórias Póstumas de Brás Cubas" (pré-processado). Foram realizados testes com contextos de tamanho `K` variando de 0 a 5.

- **Símbolos**: Letras minúsculas (sem acentos ou cedilha) e espaço.
- **Métricas analisadas**:
  - Comprimento médio dos códigos
  - Entropia
  - Tempo de compressão e descompressão
  - Comparação com compressores comerciais (WinRAR, 7Zip etc.)


