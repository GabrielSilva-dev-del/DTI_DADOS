import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('livros.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    preco REAL NOT NULL,
    data_publicacao TEXT
)
''')
conn.commit()

# Função para listar todos os livros
def listar_livros():
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    if not livros:
        print("Nenhum livro encontrado.")
    else:
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | Preço: {livro[3]} | Data: {livro[4]}")

# Função para cadastrar novo livro
def cadastrar_livro():
    titulo = input("Digite o título do livro: ").strip()
    autor = input("Digite o autor do livro: ").strip()
    preco = float(input("Digite o preço do livro: "))
    data_publicacao = input("Digite a data de publicação (opcional, formato YYYY-MM-DD): ").strip()

    cursor.execute('''
    INSERT INTO livros (titulo, autor, preco, data_publicacao)
    VALUES (?, ?, ?, ?)
    ''', (titulo, autor, preco, data_publicacao if data_publicacao else None))

    conn.commit()
    print("Livro cadastrado com sucesso!")

# Função para buscar livro por ID
def buscar_livro_por_id():
    id_livro = input("Digite o ID do livro que deseja buscar: ").strip()
    cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
    livro = cursor.fetchone()
    if livro:
        print(f"\nID: {livro[0]}")
        print(f"Título: {livro[1]}")
        print(f"Autor: {livro[2]}")
        print(f"Preço: {livro[3]}")
        print(f"Data de Publicação: {livro[4]}")
    else:
        print("Livro não encontrado.")

# Função para atualizar dados de um livro
def atualizar_livro():
    id_livro = input("Digite o ID do livro que deseja atualizar: ").strip()
    cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
    livro = cursor.fetchone()
    if not livro:
        print("❌ Livro não encontrado.")
        return

    print("\n--- Dados atuais ---")
    print(f"Título atual: {livro[1]}")
    print(f"Autor atual: {livro[2]}")
    print(f"Preço atual: {livro[3]}")
    print(f"Data de publicação atual: {livro[4]}\n")

    novo_titulo = input("Novo título (enter para manter atual): ").strip()
    novo_autor = input("Novo autor (enter para manter atual): ").strip()
    novo_preco = input("Novo preço (enter para manter atual): ").strip()
    nova_data = input("Nova data de publicação (YYYY-MM-DD, enter para manter atual): ").strip()

    titulo = novo_titulo if novo_titulo else livro[1]
    autor = novo_autor if novo_autor else livro[2]
    preco = float(novo_preco) if novo_preco else livro[3]
    data_pub = nova_data if nova_data else livro[4]

    cursor.execute('''
        UPDATE livros
        SET titulo = ?, autor = ?, preco = ?, data_publicacao = ?
        WHERE id = ?
    ''', (titulo, autor, preco, data_pub, id_livro))
    conn.commit()
    print("✅ Livro atualizado com sucesso!")

# Função para deletar um livro
def deletar_livro():
    id_livro = input("Digite o ID do livro que deseja deletar: ").strip()
    cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
    livro = cursor.fetchone()
    if not livro:
        print("❌ Livro não encontrado.")
        return

    confirm = input(f"Tem certeza que deseja deletar '{livro[1]}'? (s/N): ").strip().lower()
    if confirm == 's':
        cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
        conn.commit()
        print("✅ Livro deletado com sucesso!")
    else:
        print("Operação cancelada.")

# Função do menu principal
def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Listar Livros")
        print("2 - Sair")
        print("3 - Cadastrar Livro")
        print("4 - Buscar Livro por ID")
        print("5 - Atualizar Livro")
        print("6 - Deletar Livro")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_livros()
        elif opcao == '2':
            print("Saindo...")
            break
        elif opcao == '3':
            cadastrar_livro()
        elif opcao == '4':
            buscar_livro_por_id()
        elif opcao == '5':
            atualizar_livro()
        elif opcao == '6':
            deletar_livro()
        else:
            print("Opção inválida! Tente novamente.")

# Rodar o menu
menu()

# Fechar a conexão ao banco de dados
conn.close()
