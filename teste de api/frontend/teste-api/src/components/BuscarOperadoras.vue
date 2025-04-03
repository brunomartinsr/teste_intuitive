<script>
import { ref } from "vue";
import { searchOperators } from "@/api";
import _ from "lodash";
import "@/styles/operadoras.css"

export default {
  setup() {
    const query = ref("");
    const result = ref([]);

    const search = async () => {
      if (query.value.length > 2) {
        result.value = await searchOperators(query.value);
      } else {
        result.value = [];
      }
    };

    const debouncedSearch = _.debounce(search, 500);

    return { query, result, debouncedSearch };
  },
};
</script>

<template>
  <div class="container">
    <h2>Buscar Operadora</h2>
    <input 
      v-model="query" 
      @input="debouncedSearch" 
      placeholder="Digite a cidade ou nome" 
      class="search-input"
    />
    
    <ul v-if="result.length" class="result-list">
      <li v-for="operadora in result" :key="operadora.Registro_ANS" class="result-item">
        <strong>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</strong> 
        <span> - {{ operadora.Cidade }} ({{ operadora.UF }})</span>
      </li>
    </ul>

    <p v-else-if="query" class="no-results">Nenhuma operadora encontrada.</p>
  </div>
</template>