import sqlite3
import os
import pytest

# --- Funções que vamos testar ---

# Criar uma conexão temporária para o banco de teste
@pytest.fixture
def conexao_banco_teste():
    # Cria um banco de dados em memória (não cria arquivo físico)
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Cria a tabela
    cursor.execute('''
        CREATE TABLE livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            preco REAL NOT NULL,
            data_publicacao TEXT
        )
    ''')
    conn.commit()

    yield conn, cursor

    conn.close()

# Testar cadastro de livro
def test_cadastrar_livro(conexao_banco_teste):
    conn, cursor = conexao_banco_teste

    # Dados de teste
    titulo = "O Senhor dos Anéis"
    autor = "J.R.R. Tolkien"
    preco = 59.90
    data_publicacao = "1954-07-29"

    cursor.execute('''
        INSERT INTO livros (titulo, autor, preco, data_publicacao)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, preco, data_publicacao))
    conn.commit()

    # Buscar o livro para ver se foi salvo
    cursor.execute('SELECT * FROM livros WHERE titulo = ?', (titulo,))
    livro = cursor.fetchone()

    assert livro is not None
    assert livro[1] == titulo
    assert livro[2] == autor
    assert livro[3] == preco
    assert livro[4] == data_publicacao

# Testar listagem de livros
def test_listar_livros(conexao_banco_teste):
    conn, cursor = conexao_banco_teste

    # Inserir dois livros
    livros = [
        ("Livro A", "Autor A", 25.0, "2021-01-01"),
        ("Livro B", "Autor B", 30.0, "2022-02-02")
    ]
    cursor.executemany('''
        INSERT INTO livros (titulo, autor, preco, data_publicacao)
        VALUES (?, ?, ?, ?)
    ''', livros)
    conn.commit()

    cursor.execute('SELECT * FROM livros')
    resultado = cursor.fetchall()

    assert len(resultado) == 2
    assert resultado[0][1] == "Livro A"
    assert resultado[1][1] == "Livro B"

# Testar busca por ID
def test_buscar_livro_por_id(conexao_banco_teste):
    conn, cursor = conexao_banco_teste

    cursor.execute('''
        INSERT INTO livros (titulo, autor, preco, data_publicacao)
        VALUES (?, ?, ?, ?)
    ''', ("Livro Teste", "Autor Teste", 99.9, "2020-05-05"))
    conn.commit()

    cursor.execute('SELECT id FROM livros WHERE titulo = ?', ("Livro Teste",))
    livro_id = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
    livro = cursor.fetchone()

    assert livro is not None
    assert livro[1] == "Livro Teste"

# Testar atualização de livro
def test_atualizar_livro(conexao_banco_teste):
    conn, cursor = conexao_banco_teste

    cursor.execute('''
        INSERT INTO livros (titulo, autor, preco, data_publicacao)
        VALUES (?, ?, ?, ?)
    ''', ("Livro Original", "Autor Original", 10.0, "2010-01-01"))
    conn.commit()

    # Atualizar o livro
    cursor.execute('''
        UPDATE livros
        SET titulo = ?, autor = ?, preco = ?, data_publicacao = ?
        WHERE titulo = ?
    ''', ("Livro Atualizado", "Autor Atualizado", 20.0, "2020-02-02", "Livro Original"))
    conn.commit()

    cursor.execute('SELECT * FROM livros WHERE titulo = ?', ("Livro Atualizado",))
    livro = cursor.fetchone()

    assert livro is not None
    assert livro[1] == "Livro Atualizado"
    assert livro[2] == "Autor Atualizado"
    assert livro[3] == 20.0
    assert livro[4] == "2020-02-02"

# Testar deleção de livro
def test_deletar_livro(conexao_banco_teste):
    conn, cursor = conexao_banco_teste

    cursor.execute('''
        INSERT INTO livros (titulo, autor, preco, data_publicacao)
        VALUES (?, ?, ?, ?)
    ''', ("Livro Para Deletar", "Autor X", 50.0, "2015-03-03"))
    conn.commit()

    cursor.execute('SELECT id FROM livros WHERE titulo = ?', ("Livro Para Deletar",))
    livro_id = cursor.fetchone()[0]

    # Deletar o livro
    cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
    conn.commit()

    cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
    livro = cursor.fetchone()

    assert livro is None
