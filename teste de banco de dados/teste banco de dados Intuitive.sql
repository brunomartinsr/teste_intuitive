-- 3.3 Crie queries para estruturar tabelas necessárias para o arquivo csv.:
CREATE DATABASE teste_intuitive;
USE teste_intuitive;

CREATE TABLE operadoras (
    registro_ans INT PRIMARY KEY,
    cnpj VARCHAR(20) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(10),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(3),
    telefone VARCHAR(15),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_de_comercializacao TEXT,
    data_registro_ans DATE
);

CREATE TABLE demonstracoes_contabeis (
    data DATE NOT NULL,
    registro_ans INT NOT NULL,
    cd_conta_contabil VARCHAR(50),
    descricao TEXT,
    vl_saldo_inicial DECIMAL(18,2),
    vl_saldo_final DECIMAL(18,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- 3.4 Elabore queries para importar o conteúdo dos arquivos preparados, atentando para o encoding correto:
SHOW VARIABLES LIKE 'secure_file_priv';

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\Relatorio_cadop.csv'#caminho do secure_file_priv
INTO TABLE operadoras #tabela que irá receber os dados
FIELDS TERMINATED BY ';' #O separador é ; (isso foi conferido ao abrir o arquivo no VS Code)
ENCLOSED BY '"' #delimitação dos textos importados
LINES TERMINATED BY '\n' #adicionando quebra de linhas
IGNORE 1 ROWS #Ignorando o nome das colunas
(
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade, #Registrando nas colunas certas
    logradouro, numero, complemento, bairro, cidade, uf, cep,
    ddd, telefone, fax, endereco_eletronico, representante,
    cargo_representante, regiao_de_comercializacao, @data_registro_ans
) SET data_registro_ans = STR_TO_DATE(@data_registro_ans, '%d/%m/%Y'); #Convertendo a data

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\1T2023'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\2T2023'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\3T2023'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\4T2023'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\1T2024'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\2T2024'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\3T2024'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.3\\Uploads\\4T2024'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @data, registro_ans, cd_conta_contabil, descricao,
    vl_saldo_inicial, vl_saldo_final
) SET data = STR_TO_DATE(@data, '%d/%m/%Y');

-- 3.5 . Desenvolva uma query analítica para responder:
-- Quais as 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?
--CONSULTA:
SELECT 
    o.registro_ans, 
    o.razao_social, 
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.descricao LIKE '%SINISTROS CONHECIDOS OU AVISADOS%'
AND d.data >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) # último trimestre
GROUP BY o.registro_ans, o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;

--Quais as 10 operadoras com maiores despesas nessa categoria no último ano?
--CONSULTA:
SELECT 
    o.registro_ans, 
    o.razao_social, 
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.descricao LIKE '%SINISTROS CONHECIDOS OU AVISADOS%'
AND d.data >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH) # Últimos 12 meses
GROUP BY o.registro_ans, o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;
