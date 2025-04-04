from fastapi import APIRouter, Query
import pandas as pd

router = APIRouter()

dataFrame = pd.read_csv("data/Relatorio_cadop.csv", dtype=str, sep=";", encoding="utf-8-sig")#lendo o arquivo CSV

@router.get("/consultar_relatorio/")#Definindo a endpoint
def consultar_relatorio(query: str = Query(..., description="Texto para buscar operadoras")):
    query = query.lower().strip() #definindo e tratando a query (otimização)

    text_columns = ["Razao_Social", "Nome_Fantasia", "Cidade", "UF"]#Algumas colunas selecionadas para a busca da operadora
    dataFrame[text_columns] = dataFrame[text_columns].apply(lambda x: x.str.strip().fillna(""))

    filter = ( #Verificando se a consulta aparece em algumas das colunas
        dataFrame["Razao_Social"].str.contains(query, case=False, na=False) |
        dataFrame["Nome_Fantasia"].str.contains(query, case=False, na=False) |
        dataFrame["Cidade"].str.contains(query, case=False, na=False) |
        dataFrame["UF"].str.contains(query, case=False, na=False)
    )

    result = dataFrame[filter].copy() #Dataframe com o que foi filtrado

    result["prioridade"] = ( #Montando uma prioridade durante a busca
        result["Razao_Social"].str.lower().str.startswith(query).astype(int) +
        result["Nome_Fantasia"].str.lower().str.startswith(query).astype(int)
    )

    result = result.sort_values(by=["prioridade"], ascending=False).drop(columns=["prioridade"]) #ordenando os dados mais relevantes

    result = result.where(pd.notna(result), None) #substituindo o valor NaN por None (otimização)

    print(result)
    return result.to_dict(orient="records") #convertendo o data frame em dicionários