import requests
import os
import zipfile
from bs4 import BeautifulSoup

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

res = requests.get(url) #Realizando a requisição para baixar o conteúdo
res.raise_for_status() #Verificando o status da req

content = BeautifulSoup(res.text, "html.parser") #Convertendo o código HTML

pdfs = [
    link["href"] for link in content.find_all("a", href=True)
    if link["href"].endswith(".pdf") and ("Anexo_I" in link["href"] or "Anexo_II" in link["href"])
]#Procurando PDFs Anexo I e II e criando a lista usando compreensão de lista

if not pdfs:#Verificando se há PDFs na página em questão
    print("Nenhum PDF encontrado na página")
else:
    print(f"Coletando PDFs da página\n")

#Criando a pasta para armazenar os PDFs
os.makedirs("pdfs_baixados", exist_ok=True)

arquivos_baixados = [] # Lista para armazenar os arquivos baixados
# Baixando os PDFs
for pdf_url in pdfs:
    if pdf_url.startswith("/"): # Verificando se o link é relativo (sem domínio)
        pdf_url = "https://www.gov.br" + pdf_url

    pdf_nome = pdf_url.split("/")[-1]
    pdf_path = os.path.join("pdfs_baixados", pdf_nome)

    try:
        pdf_res = requests.get(pdf_url, timeout=10)# Realiza o download com timeout
        pdf_res.raise_for_status()#Verificando o status do download
        
    except requests.exceptions.RequestException as e:#Tratando possíveis erros
        print(f"Erro ao baixar o {pdf_nome}: {e}")
        continue

    with open(pdf_path, "wb") as file:
        file.write(pdf_res.content) # Acessa a pasta criada e escreve o conteúdo

    arquivos_baixados.append(pdf_path) # Adiciona o caminho do PDF à lista
    print(f"Baixado com sucesso: {pdf_nome}")

print("\nPDFs Baixados")

arquivo_zip = "arquivos.zip"
with zipfile.ZipFile(arquivo_zip, "w") as zip:#Compacta os arquivos
    for file in arquivos_baixados:
        zip.write(file, os.path.basename(file))

print(f"\nConfira os arquivos em {arquivo_zip}")
