# Teste de API - Intuitive
## Este README possui uma rápida explicação sobre a solução do teste 4 (teste de API) e também algumas características que achei importante comentar

Este projeto consiste na implementação de uma API para realizar consultas em uma lista de operadoras armazenada em um arquivo CSV. O frontend foi desenvolvido com para interagir com a API, e os testes de requisição foram documentados em uma coleção do Postman assim como foi pedido no enunciador, também como um acréscimo, hospedei o projeto no Vercel, porém, para um teste completo rode localmente utilizando **npm run dev** dentro da pasta teste-api e **uvicorn main:app --reload** dentro da pasta backend.

## tecnologias utilizadas para a resolução

### **Backend (Python)**
- **FastAPI**: Framework rápido e eficiente para construção de APIs.
- **Uvicorn**: servidor para rodar a API FastAPI
- **Pandas**: Para manipulação e busca de dados no CSV
- OBS: Considerei o uso do Poetry mas achei que não seria extritamente necessário

### **Frontend (Vue.js)**
- **Vue.js**: Framework progressivo para construção da interface web.
- **Axios**: Cliente HTTP para comunicação com a API.

### **Hospedagem**
- Utilizei o Vercel para hospedar o projeto e manter on-line, endereço: https://teste-intuitive.vercel.app

## Estrutura do Projeto

A estrutura do projeto consiste em duas pastas principais, frontend e backend
-**backend/**: possui a pasta data e routes como principais

-**data/**: Possui os arquivos operadoras.csv (dados cadastrais das operadoras) e teste_api.postman_collection.json (coleção para testes com algumas consultas) que são dados utilizados para a solução do projeto

-**routes/** : fiz essa pasta para modularizar as rotas para uma melhor organização e manutenção do código, nele há o arquivo operadoras.py que é responsável por buscar as operadoras que estão sendo requisitadas pelo usuário no frontend

-**main.py** : arquivo responsável por inicializar o FastAPI, definir rotas e demais configurações

-**frontend/test-api** : Possui a estrutura de frontend utilizando vue.js

-**src/** : é a pasta principal, englobando a pasta components e arquivos essenciais

-**components/** : possui o arquivo BuscarOperadoras.vue, responsável por permitir que o usuário pesquise operadoras com base no valor do campo digitado

-**api.js/** : É o arquivo responsável por chamar a API e receber e retornar os dados que vieram da API

-**App.vue** : é o componente principal que renderiza a aplicação em Vue.js

-**main.js** : É responsável principalmente por inicializar o Vue.js e montar o coponente princimal

---
## instalação e execução (Orientação bem resumida documentada durante o desenvolvimento)

### **1. Configuração do Backend**

1. Instalação das tecnologias necessárias

2. Comando para rodar: uvicorn main:app --reload

3. necessário os arquivos de data/
---

### **2. Configuração do Frontend**

1. Instalação das tecnologias usadas

2. Inicie o servidor Vue.js com:
   npm run dev

### **3. Testes com Postman**

1. Importe o arquivo `teste_api.postman_collection.json` localizado na pasta `data/`.
2. Os testes rápidos desenvolvidos são:
   - `Buscar operadora por cidade`: Busca operadoras por uma cidade específica.
   - `buscar operadora por nome incompleto`: Mostra operadoras que possuem parte do nome digitado ou o nome digitado
   - `buscar operadora por nome`: Retorna operadora que tenha o nome digitado.

---

## Lógica Aplicada para Solução

1. **Leitura do CSV**: O backend carrega os dados das operadoras a partir do arquivo `operadoras.csv`.
2. **Criação de Rota de Busca**: Foi implementada uma rota `/consultar_relatorio/` para realizar buscas textuais.
3. **Busca Eficiente**: O FastAPI usa `pandas` para filtrar registros mais relevantes com base na consulta do usuário.
4. **Disparo das requisições:**: Utilizei o Lodash para aplicar debounce na função de busca, garantindo que as requisições só sejam feitas após 500ms de inatividade do usuário, foi uma forma que encontrei para evitar a sobrecarga da API e ainda deixar a busca mais interativa. 
5. **Integração com Vue.js**: O frontend envia requisições à API e exibe os resultados em uma interface interativa.
6. **Testes no Postman**: Requisições de exemplo para validar o funcionamento da API.

---
