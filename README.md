# Sistema de Cadastro de Alunos

Sistema de cadastro de alunos em Python com banco de dados PostgreSQL, executado no terminal.

## Integrantes

| Matrícula | Nome |
|---|---|
| 01948678 | José Antônio Rocha de Lima |

## Como executar

1. Instale o psycopg: `python -m pip install "psycopg[binary]"`
2. Tenha o PostgreSQL instalado e em execução (porta 5432).
3. Defina a senha do PostgreSQL na variável de ambiente `DB_SENHA`:
   `setx DB_SENHA "sua_senha"` (feche e reabra o terminal depois).
4. Execute: `python main.py`

A tabela `alunos` é criada automaticamente na primeira execução.