from fastapi import APIRouter, Query
import pandas as pd

router = APIRouter()

dataFrame = pd.read_csv("data/Relatorio_cadop.csv", dtype=str, sep=";", encoding="utf-8-sig")

@router.get("/consultar_relatorio/")
def consultar_relatorio(query: str = Query(..., description="Texto para buscar operadoras")):
    query = query.lower().strip()

    text_columns = ["Razao_Social", "Nome_Fantasia", "Cidade", "UF"]
    dataFrame[text_columns] = dataFrame[text_columns].apply(lambda x: x.str.strip().fillna(""))

    filter = (
        dataFrame["Razao_Social"].str.contains(query, case=False, na=False) |
        dataFrame["Nome_Fantasia"].str.contains(query, case=False, na=False) |
        dataFrame["Cidade"].str.contains(query, case=False, na=False) |
        dataFrame["UF"].str.contains(query, case=False, na=False)
    )

    result = dataFrame[filter].copy()

    result["prioridade"] = (
        result["Razao_Social"].str.lower().str.startswith(query).astype(int) +
        result["Nome_Fantasia"].str.lower().str.startswith(query).astype(int)
    )

    result = result.sort_values(by=["prioridade"], ascending=False).drop(columns=["prioridade"])

    result = result.where(pd.notna(result), None) 

    print(result)
    return result.to_dict(orient="records")
