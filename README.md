# Projeto Senac

## Executar o servidor

No PowerShell, na pasta do projeto, ative o ambiente e inicie o Django:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Abra http://127.0.0.1:8000/ para ver a tabela de empregados. A página consulta
as tabelas `empregado` e `filial` no PostgreSQL, usando as variáveis
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD` definidas em `.env`.