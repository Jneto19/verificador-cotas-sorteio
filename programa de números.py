import fitz  # PyMuPDF
import re
import tkinter as tk
from tkinter import filedialog
import os

def escolher_varios_pdfs():
    root = tk.Tk()
    root.withdraw()
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return arquivos

def extrair_numeros_7_digitos(caminho_pdf):
    numeros = []
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto = pagina.get_text()
            encontrados = re.findall(r'\b\d{7}\b', texto)
            numeros.extend(encontrados)
    return numeros

def salvar_numeros_em_txt(numeros, nome_base):
    nome_arquivo = f"{nome_base}_numeros.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for numero in numeros:
            f.write(numero + "\n")
    print(f"Salvo: {nome_arquivo}")
    return nome_arquivo

def buscar_numero_em_arquivos(numero_procurado, arquivos_txt):
    encontrado = False
    for arquivo in arquivos_txt:
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                if linha.strip() == numero_procurado:
                    print(f"✅ Número encontrado no arquivo: {arquivo}")
                    encontrado = True
    if not encontrado:
        print("❌ Número NÃO encontrado em nenhum arquivo.")

# Programa principal
pdfs = escolher_varios_pdfs()
arquivos_gerados = []

if pdfs:
    for caminho_pdf in pdfs:
        numeros = extrair_numeros_7_digitos(caminho_pdf)
        nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]
        arquivo_txt = salvar_numeros_em_txt(numeros, nome_base)
        arquivos_gerados.append(arquivo_txt)

    # Perguntar número ao usuário
    while True:
        numero_desejado = input("\nDigite um número de 7 dígitos para buscar (ou 'sair'): ").strip()
        if numero_desejado.lower() == 'sair':
            break
        elif not re.fullmatch(r"\d{7}", numero_desejado):
            print("⚠️ Digite exatamente 7 dígitos.")
        else:
            buscar_numero_em_arquivos(numero_desejado, arquivos_gerados)
else:
    print("Nenhum arquivo foi selecionado.")
