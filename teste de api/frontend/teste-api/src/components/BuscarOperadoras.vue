<script>
import { ref } from "vue";
import { buscarOperadoras } from "@/api";
import _ from "lodash";
import "@/styles/operadoras.css"

export default {
  setup() {
    const query = ref("");
    const resultados = ref([]);

    const buscar = async () => {
      if (query.value.length > 2) {
        resultados.value = await buscarOperadoras(query.value);
      } else {
        resultados.value = [];
      }
    };

    const debouncedBuscar = _.debounce(buscar, 500);

    return { query, resultados, debouncedBuscar };
  },
};
</script>

<template>
  <div class="container">
    <h2>Buscar Operadora</h2>
    <input 
      v-model="query" 
      @input="debouncedBuscar" 
      placeholder="Digite a cidade ou nome" 
      class="search-input"
    />
    
    <ul v-if="resultados.length" class="result-list">
      <li v-for="operadora in resultados" :key="operadora.Registro_ANS" class="result-item">
        <strong>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</strong> 
        <span> - {{ operadora.Cidade }} ({{ operadora.UF }})</span>
      </li>
    </ul>

    <p v-else-if="query" class="no-results">Nenhuma operadora encontrada.</p>
  </div>
</template>