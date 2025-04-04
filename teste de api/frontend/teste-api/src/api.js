import axios from "axios"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

export const searchOperators = async (query) => {
    try {
        const res = await api.get("/consultar_relatorio/", {
            params: { query: query.trim() }
        })
        console.log(res.data)
        return res.data
    } catch(error) {
        console.error("Erro na busca:", error.response?.data || error.message);
        return [];
    }
}
