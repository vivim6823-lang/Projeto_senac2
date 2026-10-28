-- database: :memory:
-- Consultas para visualizar a tabela empregado.
SELECT * FROM empregado;

-- Ver as colunas e os tipos de dados da tabela empregado.
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'empregado'
ORDER BY ordinal_position;

-- Ver os empregados junto com o nome e a cidade da filial relacionada.
SELECT
    e.id AS id_empregado,
    e.nome_completo,
    e.funcao,
    e.salario,
    e.data_admissao,
    e.ativo,
    f.nome AS filial,
    f.cidade
FROM empregado e
INNER JOIN filial f ON f.id = e.filial_id
ORDER BY e.id;

-- delete from empregado where id = 19;

-- UPDATE empregado
-- SET ativo = FALSE
-- WHERE ativo = TRUE AND id = 13;
