-- CREATE TABLE IF NOT EXISTS filial (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     nome VARCHAR(100) NOT NULL,
--     cidade VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS empregado (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     filial_id BIGINT NOT NULL,
--     nome_completo VARCHAR(150) NOT NULL,
--     funcao VARCHAR(100) NOT NULL,
--     salario NUMERIC(10, 2) NOT NULL,
--     data_admissao DATE NOT NULL,
--     ativo BOOLEAN NOT NULL DEFAULT TRUE,
--     CONSTRAINT fk_empregado_filial
--         FOREIGN KEY (filial_id) REFERENCES filial(id)
-- );

-- ALTER TABLE empregado
--     ADD COLUMN IF NOT EXISTS salario NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
--     ADD COLUMN IF NOT EXISTS data_admissao DATE NOT NULL DEFAULT CURRENT_DATE,
--     ADD COLUMN IF NOT EXISTS ativo BOOLEAN NOT NULL DEFAULT TRUE;

-- COMMENT ON COLUMN empregado.id IS
--     'Chave primária numérica gerada automaticamente pelo PostgreSQL.';
-- COMMENT ON COLUMN empregado.nome_completo IS
--     'VARCHAR(150): texto limitado para armazenar o nome completo.';
-- COMMENT ON COLUMN empregado.funcao IS
--     'VARCHAR(100): texto limitado para armazenar a função.';
-- COMMENT ON COLUMN empregado.salario IS
--     'NUMERIC(10, 2): valor monetário com precisão fixa de duas casas decimais.';
-- COMMENT ON COLUMN empregado.data_admissao IS
--     'DATE: data de admissão sem informação de horário.';
-- COMMENT ON COLUMN empregado.ativo IS
--     'BOOLEAN: indica se o empregado está ativo.';

-- INSERT INTO filial (nome, cidade)
-- SELECT novos.nome, novos.cidade
-- FROM (VALUES
--     ('Filial Norte', 'Porto'),
--     ('Filial Sul', 'Lisboa'),
--     ('Filial Centro', 'Coimbra'),
--     ('Filial Ilhas', 'Funchal'),
--     ('Filial Litoral', 'Aveiro')
-- ) AS novos(nome, cidade)
-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM filial f
--     WHERE f.nome = novos.nome AND f.cidade = novos.cidade
-- );

-- -- CREATE: cinco empregados de demonstração; os IDs são gerados pelo banco.
-- INSERT INTO empregado (
--     filial_id, nome_completo, funcao, salario, data_admissao, ativo
-- )
-- SELECT f.id, novos.nome_completo, novos.funcao, novos.salario,
--        novos.data_admissao, novos.ativo
-- FROM (VALUES
--     ('Filial Norte', 'Porto', 'SQLTools - Ana', 'Assistente', 1850.00, DATE '2024-01-15', TRUE),
--     ('Filial Sul', 'Lisboa', 'SQLTools - Bruno', 'Analista', 2650.00, DATE '2022-06-03', TRUE),
--     ('Filial Centro', 'Coimbra', 'SQLTools - Carla', 'Técnica', 2150.00, DATE '2023-09-18', TRUE),
--     ('Filial Ilhas', 'Funchal', 'SQLTools - Daniel', 'Supervisor', 3100.00, DATE '2021-04-12', TRUE),
--     ('Filial Litoral', 'Aveiro', 'SQLTools - Eva', 'Gestora', 3700.00, DATE '2020-02-10', TRUE)
-- ) AS novos(nome_filial, cidade_filial, nome_completo, funcao, salario, data_admissao, ativo)
-- JOIN filial f
--     ON f.nome = novos.nome_filial AND f.cidade = novos.cidade_filial
-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM empregado e
--     WHERE e.filial_id = f.id AND e.nome_completo = novos.nome_completo
-- );

-- -- READ: listar empregados junto aos dados da filial pela chave estrangeira.
-- SELECT
--     e.id AS id_empregado,
--     f.nome AS filial,
--     f.cidade,
--     e.nome_completo,
--     e.funcao,
--     e.salario,
--     e.data_admissao,
--     e.ativo
-- FROM empregado e
-- INNER JOIN filial f ON e.filial_id = f.id;

-- -- READ: filtrar por empregados ativos.
-- SELECT id, nome_completo, funcao, salario
-- FROM empregado
-- WHERE ativo = TRUE;

-- -- READ: ordenar por salário, do maior para o menor.
-- SELECT id, nome_completo, funcao, salario
-- FROM empregado
-- ORDER BY salario DESC;

-- -- UPDATE: conferir antes, alterar com WHERE e conferir depois.
-- SELECT id, nome_completo, funcao
-- FROM empregado
-- WHERE nome_completo = 'SQLTools - Ana';

-- UPDATE empregado
-- SET funcao = 'Assistente Sênior'
-- WHERE nome_completo = 'SQLTools - Ana';

-- SELECT id, nome_completo, funcao
-- FROM empregado
-- WHERE nome_completo = 'SQLTools - Ana';

-- -- DELETE: conferir antes, excluir somente o registro de demonstração e conferir depois.
-- SELECT id, nome_completo, funcao
-- FROM empregado
-- WHERE nome_completo = 'SQLTools - Eva';

-- DELETE FROM empregado
-- WHERE nome_completo = 'SQLTools - Eva';

-- SELECT id, nome_completo, funcao
-- FROM empregado
-- WHERE nome_completo = 'SQLTools - Eva';
