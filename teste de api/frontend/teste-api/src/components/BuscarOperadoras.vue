<script>
  import { ref } from "vue";
  import { buscarOperadoras } from "@/api";
  import _ from "lodash";

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
    <input v-model="query" @input="debouncedBuscar" placeholder="Escreva a cidade ou nome" />
    <ul v-if="resultados.length">
      <li v-for="operadora in resultados" :key="operadora.Registro_ANS">
        <strong>{{ operadora.Nome_Fantasia || operadora.Razao_Social }}</strong> - {{ operadora.Cidade }} ({{ operadora.UF }})
      </li>
    </ul>
    <p v-else-if="query">Nenhuma operadora foi encontrada durante a busca</p>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 5px;
  border-bottom: 1px solid #ccc;
}
</style>
