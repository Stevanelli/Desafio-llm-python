# Desafio Acadêmico – Processamento de Resenhas com LLM Local

Este projeto foi desenvolvido como parte de um desafio acadêmico com o objetivo de integrar **Python** a um **Modelo de Linguagem Local (LLM)** utilizando o **LM Studio**, aplicando boas práticas de programação, processamento de texto e análise de dados.

---

## 🎯 Objetivo

O projeto realiza as seguintes etapas:

1. Leitura de um arquivo `.txt` contendo resenhas do aplicativo ChatGPT (JetGPT) em vários idiomas  
2. Envio dessas resenhas para um LLM executado localmente  
3. Extração estruturada das informações em formato JSON  
4. Tradução das resenhas para português  
5. Classificação do sentimento (positiva, negativa ou neutra)  
6. Análise final com contagem de avaliações e geração de texto unificado  

---

## 🧠 Tecnologias Utilizadas

- Python 3.10+
- LM Studio (LLM local)
- Modelo: `google/gemma-3-1b`
- Requests (HTTP client)
- JSON
- Pathlib

---

## 📁 Estrutura do Projeto

```text
desafio-llm-python/
│
├── main.py
├── README.md
├── .gitignore
└── data/
    └── Resenhas_App_ChatGpt.txt
