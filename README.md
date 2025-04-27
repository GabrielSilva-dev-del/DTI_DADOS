Documentação da Aplicação: Gerenciador de Livros
1. O que é a Aplicação?
A aplicação foi criada para gerenciar informações sobre livros, permitindo ao usuário cadastrar, listar, buscar, atualizar e excluir livros de um banco de dados SQLite. Ela oferece uma interface simples via terminal, onde o usuário pode interagir com essas funcionalidades de forma prática.

Propriedades do Livro
Cada livro tem os seguintes dados:

ID (obrigatório): Um número único gerado automaticamente para identificar o livro.

Título (obrigatório): O nome do livro.

Autor (obrigatório): O autor do livro.

Preço (obrigatório): O preço do livro em formato decimal.

Data de Publicação (opcional): A data de lançamento do livro, caso o usuário queira informar.

2. Linguagem Usada
A aplicação foi desenvolvida em Python, utilizando a biblioteca sqlite3 para gerenciar os dados no banco de dados SQLite. O SQLite é uma ótima escolha aqui, pois ele não requer um servidor separado e é fácil de usar, perfeito para um projeto simples como este.

3. Como Instalar as Dependências
Não há dependências externas além do próprio Python, pois a biblioteca sqlite3 já está incluída na instalação padrão do Python.

Como instalar o Python (se necessário):
Se você ainda não tem o Python instalado, pode baixá-lo em python.org.

Após instalar, verifique se deu tudo certo no terminal com o comando:

bash
Copiar
Editar
python --version
4. Como Rodar a Aplicação
Aqui estão os passos para colocar a aplicação para rodar:

Baixe o código: Clone o repositório ou baixe os arquivos do código.

Inicie o banco de dados: Quando você rodar a aplicação pela primeira vez, o banco de dados será criado automaticamente, junto com a tabela de livros.

Execute o código:

Abra o terminal e vá até o diretório onde o arquivo Python está.

Execute o comando:

bash
Copiar
Editar
python gerenciador_livros.py
Interaja com o Menu: O menu aparecerá no terminal, onde você pode escolher as opções de cadastro, listagem, atualização, etc.

5. Funcionalidades da Aplicação
A aplicação oferece várias funcionalidades úteis para gerenciar os livros:

Listar Livros
Mostra todos os livros cadastrados no banco de dados.

Exemplo: Se você escolher "1" no menu, todos os livros registrados serão exibidos.

Cadastrar Novo Livro
Permite adicionar um novo livro ao banco de dados.

Campos obrigatórios: título, autor e preço.

Exemplo: Se você escolher "3" no menu, será solicitado a inserir os dados do livro.

Buscar Livro por ID
Permite procurar um livro específico usando o ID.

Exemplo: Se você escolher "4" no menu, digite o ID do livro para visualizá-lo.

Atualizar Livro
Permite alterar os dados de um livro já existente.

Exemplo: Se você escolher "5", poderá atualizar informações do livro (título, autor, preço e data).

Deletar Livro
Permite excluir um livro do banco de dados.

Exemplo: Se você escolher "6", será solicitado a confirmar a exclusão do livro.

6. Diferenciais Opcionais
Testes Unitários
Os testes unitários ajudam a garantir que tudo esteja funcionando corretamente. Por exemplo, podemos testar a função de cadastrar um livro para garantir que os dados sejam inseridos corretamente no banco de dados.

Aqui está um exemplo de como um teste poderia ser feito para a função cadastrar_livro:

python
Copiar
Editar
import unittest
import sqlite3
from gerenciador_livros import cadastrar_livro

class TestCadastroLivro(unittest.TestCase):

    def setUp(self):
        # Configura um banco de dados temporário para o teste
        self.conn = sqlite3.connect(':memory:')  
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            preco REAL NOT NULL,
            data_publicacao TEXT
        )
        ''')

    def test_cadastrar_livro(self):
        # Testa o cadastro de um livro
        cadastrar_livro('Livro Teste', 'Autor Teste', 19.99, '2023-04-01')
        self.cursor.execute('SELECT * FROM livros WHERE titulo = "Livro Teste"')
        livro = self.cursor.fetchone()
        self.assertIsNotNone(livro)  # Verifica se o livro foi inserido
        self.assertEqual(livro[1], 'Livro Teste')

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
Conteinerização com Docker
Você pode usar o Docker para "empacotar" a aplicação em um contêiner, tornando-a fácil de rodar em qualquer ambiente sem se preocupar com configurações de sistema.

Para criar a imagem Docker:

Crie um arquivo Dockerfile no mesmo diretório do código Python:

Dockerfile
Copiar
Editar
FROM python:3.9-slim

# Instalando dependências
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir sqlite3

# Comando para rodar o script Python
CMD ["python", "gerenciador_livros.py"]
Construa e rode a imagem Docker:

No terminal, vá até a pasta onde está o Dockerfile e execute:

bash
Copiar
Editar
docker build -t gerenciador-livros .
docker run -it gerenciador-livros
Logs
A aplicação pode ser configurada para registrar operações importantes ou erros, usando o módulo logging do Python. O exemplo abaixo registra a ação de cadastrar um livro:

python
Copiar
Editar
import logging

# Configura o log
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    logging.info(f'Livro cadastrado: {titulo} por {autor}')
    print("Livro cadastrado com sucesso!")
O log será gravado no arquivo app.log.
