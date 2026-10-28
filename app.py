import os
from datetime import date

import psycopg2
from dotenv import load_dotenv

load_dotenv()

FILIAIS = (
    ("Filial Norte", "Porto"),
    ("Filial Sul", "Lisboa"),
    ("Filial Centro", "Coimbra"),
    ("Filial Ilhas", "Funchal"),
    ("Filial Litoral", "Aveiro"),
)

EMPREGADOS = (
    ("Ana Ferreira", "Assistente", 1850.00, date(2024, 1, 15), True, 0),
    ("Bruno Almeida", "Analista", 2650.00, date(2022, 6, 3), True, 1),
    ("Carla Rodrigues", "Técnica", 2150.00, date(2023, 9, 18), True, 2),
    ("Daniela Costa", "Supervisora", 3100.00, date(2021, 4, 12), True, 3),
    ("Eduardo Martins", "Gestor", 3700.00, date(2020, 2, 10), True, 4),
    ("Filipa Sousa", "Assistente", 1900.00, date(2024, 3, 11), True, 0),
    ("Gonçalo Pereira", "Analista", 2750.00, date(2022, 8, 22), True, 1),
    ("Helena Ribeiro", "Técnica", 2250.00, date(2023, 5, 9), True, 2),
    ("Igor Carvalho", "Supervisor", 3200.00, date(2021, 7, 19), True, 3),
    ("Joana Mendes", "Gestora", 3800.00, date(2019, 11, 4), True, 4),
    ("Luís Gomes", "Assistente", 1950.00, date(2024, 2, 5), True, 0),
    ("Mariana Lopes", "Analista", 2800.00, date(2022, 10, 17), True, 1),
    ("Nuno Fernandes", "Técnico", 2300.00, date(2023, 6, 26), True, 2),
    ("Olga Santos", "Supervisora", 3250.00, date(2021, 9, 13), True, 3),
    ("Paulo Nunes", "Gestor", 3900.00, date(2019, 8, 20), True, 4),
    ("Rita Teixeira", "Assistente", 2000.00, date(2024, 4, 8), True, 0),
    ("Samuel Correia", "Analista", 2850.00, date(2022, 12, 1), True, 1),
    ("Teresa Castro", "Técnica", 2350.00, date(2023, 7, 14), True, 2),
    ("Vasco Pinto", "Supervisor", 3300.00, date(2021, 10, 25), True, 3),
    ("Adriana Moreira", "Gestora", 4000.00, date(2019, 5, 6), True, 4),
    ("Beatriz Cardoso", "Assistente", 2050.00, date(2024, 5, 20), True, 0),
    ("Carlos Neves", "Analista", 2900.00, date(2023, 1, 16), True, 1),
    ("Diana Machado", "Técnica", 2400.00, date(2023, 8, 7), True, 2),
    ("Emanuel Reis", "Supervisor", 3350.00, date(2022, 1, 24), True, 3),
    ("Fátima Azevedo", "Gestora", 4100.00, date(2018, 12, 3), True, 4),
)


def conectar_banco():
    variaveis_obrigatorias = (
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    )
    variaveis_em_falta = [
        nome for nome in variaveis_obrigatorias if not os.getenv(nome)
    ]
    if variaveis_em_falta:
        raise ValueError(
            "Variáveis de conexão ausentes: " + ", ".join(variaveis_em_falta)
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=10,
    )


def preparar_tabelas(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS filial (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cidade VARCHAR(100) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empregado (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            filial_id BIGINT NOT NULL,
            nome_completo VARCHAR(150) NOT NULL,
            funcao VARCHAR(100) NOT NULL,
            salario NUMERIC(10, 2) NOT NULL,
            data_admissao DATE NOT NULL,
            ativo BOOLEAN NOT NULL DEFAULT TRUE,
            CONSTRAINT fk_empregado_filial
                FOREIGN KEY (filial_id) REFERENCES filial(id)
        )
        """
    )
    cursor.execute(
        """
        ALTER TABLE empregado
            ADD COLUMN IF NOT EXISTS salario NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
            ADD COLUMN IF NOT EXISTS data_admissao DATE NOT NULL DEFAULT CURRENT_DATE,
            ADD COLUMN IF NOT EXISTS ativo BOOLEAN NOT NULL DEFAULT TRUE
        """
    )


def obter_filiais(cursor):
    ids_filiais = []
    for nome, cidade in FILIAIS:
        cursor.execute(
            "SELECT id FROM filial WHERE nome = %s AND cidade = %s",
            (nome, cidade),
        )
        resultado = cursor.fetchone()
        if resultado is None:
            cursor.execute(
                """
                INSERT INTO filial (nome, cidade)
                VALUES (%s, %s)
                RETURNING id
                """,
                (nome, cidade),
            )
            resultado = cursor.fetchone()
        ids_filiais.append(resultado[0])
    return ids_filiais


def imprimir_empregados(titulo, empregados):
    print(f"\n{titulo}")
    if not empregados:
        print("(nenhum registro)")
        return

    print("ID | Filial | Nome | Função | Salário | Admissão | Ativo")
    for empregado in empregados:
        print(" | ".join(str(valor) for valor in empregado))


def buscar_empregado(cursor, empregado_id):
    cursor.execute(
        """
        SELECT e.id, f.nome, e.nome_completo, e.funcao,
               e.salario, e.data_admissao, e.ativo
        FROM empregado e
        INNER JOIN filial f ON f.id = e.filial_id
        WHERE e.id = %s
        """,
        (empregado_id,),
    )
    return cursor.fetchone()


def executar_crud(cursor):
    ids_filiais = obter_filiais(cursor)

    # CREATE: inserir 25 empregados; a chave id é gerada pelo PostgreSQL.
    ids_criados = []
    for nome, funcao, salario, admissao, ativo, indice_filial in EMPREGADOS:
        cursor.execute(
            """
            INSERT INTO empregado (
                filial_id, nome_completo, funcao, salario, data_admissao, ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                ids_filiais[indice_filial],
                nome,
                funcao,
                salario,
                admissao,
                ativo,
            ),
        )
        ids_criados.append(cursor.fetchone()[0])
    print(f"CREATE: {len(ids_criados)} empregados inseridos.")

    # READ: listar todos, depois filtrar e ordenar os empregados ativos.
    cursor.execute(
        """
        SELECT e.id, f.nome, e.nome_completo, e.funcao,
               e.salario, e.data_admissao, e.ativo
        FROM empregado e
        INNER JOIN filial f ON f.id = e.filial_id
        ORDER BY e.id
        """
    )
    imprimir_empregados("READ: todos os empregados, ordenados por ID", cursor.fetchall())

    cursor.execute(
        """
        SELECT e.id, f.nome, e.nome_completo, e.funcao,
               e.salario, e.data_admissao, e.ativo
        FROM empregado e
        INNER JOIN filial f ON f.id = e.filial_id
        WHERE e.ativo = %s AND e.salario >= %s
        ORDER BY e.salario DESC, e.nome_completo ASC
        """,
        (True, 3000.00),
    )
    imprimir_empregados(
        "READ: empregados ativos com salário >= 3000, ordenados por salário",
        cursor.fetchall(),
    )

    # UPDATE: alterar apenas um dos registros criados nesta execução.
    id_atualizado = ids_criados[0]
    antes = buscar_empregado(cursor, id_atualizado)
    print(f"\nUPDATE antes: {antes}")
    cursor.execute(
        "UPDATE empregado SET funcao = %s WHERE id = %s",
        ("Assistente Sênior", id_atualizado),
    )
    depois = buscar_empregado(cursor, id_atualizado)
    print(f"UPDATE depois: {depois}")

    # DELETE: excluir apenas outro registro criado nesta execução.
    id_excluido = ids_criados[-1]
    antes = buscar_empregado(cursor, id_excluido)
    print(f"\nDELETE antes: {antes}")
    cursor.execute("DELETE FROM empregado WHERE id = %s", (id_excluido,))
    depois = buscar_empregado(cursor, id_excluido)
    print(f"DELETE depois: {depois}")


if __name__ == "__main__":
    conexao = conectar_banco()
    try:
        with conexao:
            with conexao.cursor() as cursor:
                preparar_tabelas(cursor)
                executar_crud(cursor)
    finally:
        conexao.close()
