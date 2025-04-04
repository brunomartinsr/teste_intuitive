<script>
import { ref } from "vue";
import { searchOperators } from "@/api";
import _ from "lodash";
import "@/styles/operadoras.css"

export default {
  setup() {
    const query = ref("");//variáveis reativas
    const result = ref([]);

    const search = async () => { //Chamando a função de busca da API
      if (query.value.length > 2) {// O usuário tem que ter digitado 3 caracteres no mínimo
        result.value = await searchOperators(query.value); //chamando a função
      } else {
        result.value = []; //limpa o result.value para não ter buscas desnecessárias
      }
    };

    const debouncedSearch = _.debounce(search, 500);// evitando muitas requisições

    return { query, result, debouncedSearch }; //retornando para o template
  },
};
</script>

<template>
  <div class="container">
    <h2>Buscar Operadora</h2>
    <!-- campo de busca -->
    <input 
      v-model="query" 
      @input="debouncedSearch" 
      placeholder="Digite a cidade ou nome" 
      class="search-input"
    />
    <!-- exibindo os resultados -->
    <ul v-if="result.length" class="result-list">
      <li v-for="operadora in result" :key="operadora.Registro_ANS" class="result-item">
        <strong>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</strong> 
        <span> - {{ operadora.Cidade }} ({{ operadora.UF }})</span>
      </li>
    </ul>

    <p v-else-if="query" class="no-results">Nenhuma operadora encontrada.</p>
  </div>
</template>