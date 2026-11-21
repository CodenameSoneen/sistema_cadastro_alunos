import psycopg
import os

def conectar_banco():
    senha = os.getenv("DB_SENHA")
    if senha is None:
        print("Defina a variável de ambiente DB_SENHA antes de rodar.")
        exit()

    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password=senha
    )
    return conn



def criar_tabela():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        idade INTEGER NOT NULL,
        nota NUMERIC(4,2) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()



def cadastrar_aluno():
    nome = input("Nome do aluno: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return

    if len(nome) > 100:
            print("O nome deve ter no máximo 100 caracteres.")
            return

    try:
        idade = int(input("Idade: "))
        nota = float(input("Nota (0 a 10): ").replace(",", "."))
    except ValueError:
        print("Idade e nota devem ser números.")
        return

    if idade <= 0 or idade > 120:
            print("A idade deve ir de 1 a 120!")
            return

    if not 0 <= nota <= 10:
        print("A nota deve estar entre 0 e 10.")
        return
    
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alunos (nome, idade, nota) VALUES (%s, %s, %s)",
        (nome, idade, nota)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Aluno cadastrado com sucesso!")



def listar_alunos():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, idade, nota FROM alunos ORDER BY id")
    alunos = cur.fetchall()
    cur.close()
    conn.close()

    if len(alunos) == 0:
        print("Nenhum aluno cadastrado.")
        return

    for id_aluno, nome, idade, nota in alunos:
        print(f"ID: {id_aluno} | Nome: {nome} | Idade: {idade} | Nota: {nota}")



def buscar_alunos():
    nome = input("Nome do aluno a buscar: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return

    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nome, idade, nota FROM alunos WHERE nome ILIKE %s ORDER BY id",
        (f"%{nome}%",)
    )
    alunos = cur.fetchall()
    cur.close()
    conn.close()

    if len(alunos) == 0:
        print("Nenhum aluno encontrado com esse nome.")
        return

    for id_aluno, nome_aluno, idade, nota in alunos:
        print(f"ID: {id_aluno} | Nome: {nome_aluno} | Idade: {idade} | Nota: {nota}")



def atualizar_aluno():
    try:
        id_aluno = int(input("ID do aluno a atualizar: "))
    except ValueError:
        print("O ID deve ser um número inteiro.")
        return

    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT nome, idade, nota FROM alunos WHERE id = %s", (id_aluno,))
    aluno = cur.fetchone()
    cur.close()
    conn.close()

    if aluno is None:
        print("Aluno não encontrado.")
        return

    print(f"Dados atuais -> Nome {aluno[0]} | Idade: {aluno[1]} | Nota: {aluno[2]}")

    nome = input("Novo nome: ").strip()
    if nome == "":
        print("O nome não pode ficar vazio.")
        return

    if len(nome) > 100:
            print("O nome deve ter no máximo 100 caracteres.")
            return

    try:
        idade = int(input("Nova idade: "))
        nota = float(input("Nova nota (0 a 10): ").replace(",", "."))
    except ValueError:
        print("Idade e nota devem ser números.")
        return

    if idade <= 0 or idade > 120:
        print("A idade deve ir de 1 a 120!")
        return

    if not 0 <= nota <= 10:
        print("A nota deve estar entre 0 e 10.")
        return

    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alunos SET nome = %s, idade = %s, nota = %s WHERE id = %s",
        (nome, idade, nota, id_aluno)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Aluno atualizado com sucesso!")



def remover_aluno():
    try:
        id_aluno = int(input("ID do aluno a remover: "))
    except ValueError:
        print("O ID deve ser um número inteiro.")
        return

    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM alunos WHERE id = %s", (id_aluno,))
    aluno = cur.fetchone()

    if aluno is None:
        print("Aluno não encontrado.")
        cur.close()
        conn.close()
        return

    confirmacao = input(f"Remover {aluno[0]}? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Remoção cancelada.")
        cur.close()
        conn.close()
        return

    cur.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
    conn.commit()
    cur.close()
    conn.close()
    print("Aluno removido com sucesso!")



def media_geral():
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT AVG(nota) FROM alunos")
    media = cur.fetchone()[0]
    cur.close()
    conn.close()

    if media is None:
        print("Nenhum aluno cadastrado.")
        return
    print(f"Média geral das notas: {media:.2f}")



def menu():
    while True:
        print("\n=== SISTEMA DE CADASTRO DE ALUNOS ===")
        print("1. Cadastrar aluno")
        print("2. Listar todos os alunos")
        print("3. Buscar aluno pelo nome")
        print("4. Atualizar dados de um aluno")
        print("5. Remover aluno")
        print("6. Mostrar média geral das notas")
        print("7. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            buscar_alunos()
        elif opcao == "4":
            atualizar_aluno()
        elif opcao == "5":
            remover_aluno()
        elif opcao == "6":
            media_geral()
        elif opcao == "7":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Digite um número de 1 a 7.")



if __name__ == "__main__":
    criar_tabela()
    menu()