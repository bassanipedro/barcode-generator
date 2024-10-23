# Gerador de Códigos de Barras

Este é um aplicativo simples de geração de códigos de barras usando Python e a biblioteca Tkinter para a interface gráfica. O usuário pode inserir códigos de barras e o aplicativo os gera em formato de imagem.

## Funcionalidades

- Insira códigos de barras (um por linha).
- Geração automática de imagens de códigos de barras no formato PNG.
- Exibição dos códigos gerados em uma nova janela.

## Tecnologias Utilizadas

- **Python**
- **Tkinter** (para interface gráfica)
- **Barcode** (para geração de códigos de barras)
- **Pillow** (para manipulação de imagens)

## Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema. Você pode baixar o Python em [python.org](https://www.python.org).

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/bassanipedro/barcode-generator
   cd barcode-generator
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   python index.py
   ```

## Como Usar

1. Ao abrir o aplicativo, insira os códigos de barras no campo de texto (um código por linha).
2. Clique no botão "Gerar Códigos de Barras".
3. Uma nova janela será aberta exibindo as imagens geradas.
