from fastapi import APIRouter, Query
import pandas as pd

router = APIRouter()

dataFrame = pd.read_csv("data/Relatorio_cadop.csv", dtype=str, sep=";", encoding="utf-8-sig")

@router.get("/consultar_relatorio/")
def consultar_relatorio(query: str = Query(..., description="Texto para buscar operadoras")):
    query = query.lower().strip()

    colunas_texto = ["Razao_Social", "Nome_Fantasia", "Cidade", "UF"]
    dataFrame[colunas_texto] = dataFrame[colunas_texto].apply(lambda x: x.str.strip().fillna(""))

    filtro = (
        dataFrame["Razao_Social"].str.contains(query, case=False, na=False) |
        dataFrame["Nome_Fantasia"].str.contains(query, case=False, na=False) |
        dataFrame["Cidade"].str.contains(query, case=False, na=False) |
        dataFrame["UF"].str.contains(query, case=False, na=False)
    )

    resultados = dataFrame[filtro].copy()

    resultados["prioridade"] = (
        resultados["Razao_Social"].str.lower().str.startswith(query).astype(int) +
        resultados["Nome_Fantasia"].str.lower().str.startswith(query).astype(int)
    )

    resultados = resultados.sort_values(by=["prioridade"], ascending=False).drop(columns=["prioridade"])

    resultados = resultados.where(pd.notna(resultados), None) 

    print(resultados)
    return resultados.to_dict(orient="records")
