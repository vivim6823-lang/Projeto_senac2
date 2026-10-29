import logging

import psycopg2
from django.http import HttpResponseServerError
from django.shortcuts import render

from app import conectar_banco


logger = logging.getLogger(__name__)


def home(request):
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT e.id, e.nome_completo, e.funcao, e.salario,
                           e.data_admissao, e.ativo, f.nome AS filial,
                           f.cidade
                    FROM empregado e
                    INNER JOIN filial f ON f.id = e.filial_id
                    ORDER BY e.id
                    """
                )
                empregados = [
                    dict(zip((coluna[0] for coluna in cursor.description), linha))
                    for linha in cursor.fetchall()
                ]
    except (psycopg2.Error, ValueError):
        logger.exception("Não foi possível carregar os empregados do PostgreSQL")
        return HttpResponseServerError(
            "Não foi possível carregar os empregados. Verifique a conexão "
            "com o PostgreSQL e as tabelas empregado e filial."
        )

    return render(request, "empregados.html", {"empregados": empregados})
