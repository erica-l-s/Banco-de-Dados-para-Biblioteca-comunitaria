-- Criação da tabela para usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    endereco VARCHAR(255),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela para livros
CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    ano_publicacao YEAR,
    categoria VARCHAR(100),
    status ENUM('disponível', 'emprestado') DEFAULT 'disponível',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela para empréstimos
CREATE TABLE emprestimos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_livro INT,
    data_emprestimo DATE NOT NULL,
    data_devolucao DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_livro) REFERENCES livros(id)
);

-- Criação da tabela para funcionários da biblioteca
CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(15)
);

-- Criação da tabela para registros de feedback
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    comentario TEXT,
    data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

-- Inserção de usuários
INSERT INTO usuarios (nome, email, telefone, endereco) VALUES
('João da Silva', 'joao.silva@email.com', '123456789', 'Rua A, 123'),
('Maria Oliveira', 'maria.oliveira@email.com', '987654321', 'Rua B, 456');

-- Inserção de livros
INSERT INTO livros (titulo, autor, isbn, ano_publicacao, categoria) VALUES
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', '978-85-07-01258-8', 1943, 'Infantil'),
('1984', 'George Orwell', '978-85-07-04476-4', 1949, 'Ficção');

-- Inserção de funcionários
INSERT INTO funcionarios (nome, cargo, email, telefone) VALUES
('João da Silva', 'Diretor', 'joao.diretor@biblioteca.com', '123456789'),
('Maria da Silva', 'Gerente', 'maria.gerente@biblioteca.com', '987654321');

-- Inserção de feedback
INSERT INTO feedback (id_usuario, comentario) VALUES
(1, 'Ótimo sistema de gerenciamento de livros.'),
(2, 'O sistema precisa melhorar na busca por livros.');