import psycopg2 
from psycopg2 import Error 

# Função para criar uma conexão com o banco de dados PostgreSQL
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="sua_base_de_dados",
            user="seu_usuario",
            password="sua_senha",
            host="localhost",
            port="5432"
        )
        print("Conexão com o banco de dados PostgreSQL bem-sucedida.")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# Função para criar tabelas
def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                telefone VARCHAR(15),
                endereco VARCHAR(255),
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                autor VARCHAR(100) NOT NULL,
                isbn VARCHAR(20) UNIQUE NOT NULL,
                ano_publicacao INTEGER,
                categoria VARCHAR(100),
                status VARCHAR(20) DEFAULT 'disponível',
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emprestimos (
                id SERIAL PRIMARY KEY,
                id_usuario INTEGER REFERENCES usuarios(id),
                id_livro INTEGER REFERENCES livros(id),
                data_emprestimo DATE NOT NULL,
                data_devolucao DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(50),
                email VARCHAR(100) UNIQUE NOT NULL,
                telefone VARCHAR(15)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                id_usuario INTEGER REFERENCES usuarios(id),
                comentario TEXT,
                data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("Tabelas criadas com sucesso.")
    except Error as e:
        print(f"Erro ao criar tabelas: {e}")

# Função para adicionar um usuário
def add_usuario(conn, nome, email, telefone, endereco):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, email, telefone, endereco) 
            VALUES (%s, %s, %s, %s)
        ''', (nome, email, telefone, endereco))
        conn.commit()
        print("Usuário adicionado com sucesso.")
    except Error as e:
        print(f"Erro ao adicionar usuário: {e}")

# Função para adicionar um livro
def add_livro(conn, titulo, autor, isbn, ano_publicacao, categoria):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO livros (titulo, autor, isbn, ano_publicacao, categoria) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (titulo, autor, isbn, ano_publicacao, categoria))
        conn.commit()
        print("Livro adicionado com sucesso.")
    except Error as e:
        print(f"Erro ao adicionar livro: {e}")

# Função para emprestar um livro
def emprestar_livro(conn, id_usuario, id_livro, data_emprestimo):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo) 
            VALUES (%s, %s, %s)
        ''', (id_usuario, id_livro, data_emprestimo))
        
        cursor.execute('''
            UPDATE livros
            SET status = 'emprestado'
            WHERE id = %s
        ''', (id_livro,))
        conn.commit()
        print("Livro emprestado com sucesso.")
    except Error as e:
        print(f"Erro ao emprestar livro: {e}")

# Função para devolver um livro
def devolver_livro(conn, id_emprestimo, data_devolucao):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE emprestimos
            SET data_devolucao = %s
            WHERE id = %s
        ''', (data_devolucao, id_emprestimo))
        
        cursor.execute('''
            UPDATE livros
            SET status = 'disponível'
            WHERE id = (SELECT id_livro FROM emprestimos WHERE id = %s)
        ''', (id_emprestimo,))
        conn.commit()
        print("Livro devolvido com sucesso.")
    except Error as e:
        print(f"Erro ao devolver livro: {e}")

# Função para adicionar feedback
def add_feedback(conn, id_usuario, comentario):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (id_usuario, comentario) 
            VALUES (%s, %s)
        ''', (id_usuario, comentario))
        conn.commit()
        print("Feedback adicionado com sucesso.")
    except Error as e:
        print(f"Erro ao adicionar feedback: {e}")

# Função principal para executar o sistema
def main():
    conn = create_connection()
    
    if conn:
        create_tables(conn)
        add_usuario(conn, "João Silva", "joao.silva@example.com", "123456789", "Rua A, 123")
        add_livro(conn, "O Senhor dos Anéis", "J.R.R. Tolkien", "1234567890123", 1954, "Fantasia")
        emprestar_livro(conn, 1, 1, "2024-09-01")
        devolver_livro(conn, 1, "2024-09-15")
        add_feedback(conn, 1, "Ótima biblioteca, muito organizada!")
        conn.close()

if __name__ == '__main__':
    main()
