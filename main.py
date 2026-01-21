# ============================
# IMPORTAÇÕES
# ============================
from pathlib import Path
import requests
import json
import time


# ============================
# CONFIGURAÇÃO DO LM STUDIO
# ============================
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-3-1b"


# ============================
# LEITURA DO ARQUIVO TXT
# ============================
def carregar_resenhas(caminho_arquivo: Path) -> list[str]:
    """
    Lê um arquivo .txt e retorna uma lista com cada linha.
    """
    resenhas = []

    with caminho_arquivo.open("r", encoding="utf-8", errors="ignore") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:
                resenhas.append(linha)

    return resenhas


# ============================
# CRIAÇÃO DO PROMPT
# ============================
def criar_prompt(resenha: str) -> str:
    return f"""
Você receberá uma resenha de aplicativo.

Responda SOMENTE em JSON válido, sem qualquer texto fora do JSON.

Campos obrigatórios:
- usuario
- resenha_original
- traducao_pt
- avaliacao (positiva, negativa ou neutra)

Resenha:
{resenha}
"""


# ============================
# EXTRAÇÃO SEGURA DO JSON
# ============================
def extrair_json(texto: str) -> dict:
    """
    Extrai o primeiro JSON válido encontrado em um texto.
    """
    inicio = texto.find("{")
    fim = texto.rfind("}")

    if inicio == -1 or fim == -1:
        raise ValueError("Nenhum JSON encontrado na resposta do modelo.")

    json_str = texto[inicio:fim + 1]
    return json.loads(json_str)


# ============================
# CONSULTA AO LLM (LM STUDIO)
# ============================
def consultar_llm(prompt: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente que responde apenas em JSON válido."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(LMS_STUDIO_URL := LM_STUDIO_URL, headers=headers, json=payload)
    response.raise_for_status()

    resposta_texto = response.json()["choices"][0]["message"]["content"]

    try:
        return extrair_json(resposta_texto)
    except Exception as erro:
        print("\n❌ ERRO AO PROCESSAR RESPOSTA DO MODELO")
        print("Resposta recebida:")
        print(resposta_texto)
        raise erro


# ============================
# PROCESSAMENTO DAS RESENHAS
# ============================
def processar_resenhas(lista_resenhas: list[str]) -> list[dict]:
    resultados = []

    for i, resenha in enumerate(lista_resenhas, start=1):
        print(f"Processando resenha {i}/{len(lista_resenhas)}...")

        prompt = criar_prompt(resenha)
        resposta = consultar_llm(prompt)
        resultados.append(resposta)

        time.sleep(0.5)  # evita sobrecarga do modelo

    return resultados


# ============================
# ANÁLISE FINAL DOS DADOS
# ============================
def analisar_resenhas(resenhas: list[dict], separador: str = " || "):
    contagem = {
        "positiva": 0,
        "negativa": 0,
        "neutra": 0
    }

    textos = []

    for item in resenhas:
        avaliacao = item.get("avaliacao", "neutra").lower()
        if avaliacao in contagem:
            contagem[avaliacao] += 1
        else:
            contagem["neutra"] += 1

        texto = (
            f"Usuário: {item.get('usuario')} | "
            f"Resenha: {item.get('traducao_pt')} | "
            f"Avaliação: {item.get('avaliacao')}"
        )

        textos.append(texto)

    texto_final = separador.join(textos)

    return contagem, texto_final


# ============================
# FUNÇÃO PRINCIPAL
# ============================
def main():
    BASE_DIR = Path(__file__).resolve().parent
    caminho_arquivo = BASE_DIR / "data" / "Resenhas_App_ChatGpt.txt"

    print("📄 Lendo arquivo:", caminho_arquivo)

    lista_resenhas = carregar_resenhas(caminho_arquivo)
    print(f"✅ Resenhas carregadas: {len(lista_resenhas)}")

    resenhas_processadas = processar_resenhas(lista_resenhas)

    contagem, texto_final = analisar_resenhas(resenhas_processadas)

    print("\n📊 Contagem de avaliações:")
    print(contagem)

    print("\n🧾 Texto unificado:")
    print(texto_final)


# ============================
# EXECUÇÃO
# ============================
if __name__ == "__main__":
    main()
