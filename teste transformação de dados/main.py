import requests
import zipfile
import os
import pdfplumber
import pandas as pd

pdf_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
arquivo_pdf = "Anexo_1.pdf"

res = requests.get(pdf_url)#coleta o PDF da url definida acima
res.raise_for_status()

with open(arquivo_pdf, "wb") as file:#Escreve o PDF em um arquivo local
    file.write(res.content)
    
dados = []
with pdfplumber.open(arquivo_pdf) as pdf:#Coleta as tabelas página por página
    
    for pagina in pdf.pages:
        tabela = pagina.extract_table()#Extrai as tabelas localizadas
        
        if tabela:
            dados.extend(tabela)#inserindo os dados na lista
            
dataFrame = pd.DataFrame(dados)#coleta os dados e armazena como um data frame
dataFrame.columns = dataFrame.iloc[0]#Definindo a primeira linha (cabeçalho) como nome das colunas

dataFrame.rename(columns={
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatórial",
}, inplace = True)

dataFrame = dataFrame.dropna(how="all")
dataFrame = dataFrame.map(lambda x: x.strip() if isinstance(x, str) else x)

arquivo_csv = "Tabela_Anexo1.csv"
dataFrame.to_csv(arquivo_csv, index = False, encoding = "utf-8-sig", sep = ";")

arquivo_zip = "Teste_Bruno_Martins_Rodrigues.zip"
with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write(arquivo_csv, os.path.basename(arquivo_csv))
    
print(f"CSV compactado em {arquivo_zip}")