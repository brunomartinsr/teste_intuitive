import requests
import zipfile
import os
import pdfplumber
import pandas as pd

pdf_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
pdf_file = "Anexo_1.pdf"

res = requests.get(pdf_url)#coleta o PDF da url definida acima
res.raise_for_status()

with open(pdf_file, "wb") as file:#Escreve o PDF em um arquivo local
    file.write(res.content)
    
data = []
with pdfplumber.open(pdf_file) as pdf:#Coleta as tabelas página por página
    
    for page in pdf.pages:
        table = page.extract_table()#Extrai as tabelas localizadas
        
        if table:
            data.extend(table)#inserindo os dados na lista
            
dataFrame = pd.DataFrame(data)#coleta os dados e armazena como um data frame
dataFrame.columns = dataFrame.iloc[0]#Definindo a primeira linha (cabeçalho) como nome das colunas

dataFrame.rename(columns={
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatórial",
}, inplace = True)

dataFrame = dataFrame.dropna(how="all")
dataFrame = dataFrame.map(lambda x: x.strip() if isinstance(x, str) else x)

csv_file = "Tabela_Anexo1.csv"
dataFrame.to_csv(csv_file, index = False, encoding = "utf-8-sig", sep = ";")

zip_file = "Teste_Bruno_Martins_Rodrigues.zip"
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zip:
    zip.write(csv_file, os.path.basename(csv_file))
    
print(f"CSV compactado em {zip_file}")