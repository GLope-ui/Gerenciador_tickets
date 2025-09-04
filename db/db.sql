-- Tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL, -- senha hash
    tipo ENUM('admin', 'cliente') NOT NULL
);

-- Tabela de Tickets
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    cliente_id INT NOT NULL, -- FK para usuarios(id)
    status ENUM('aberto', 'pausado', 'fechado') DEFAULT 'aberto',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tempo_resposta INTERVAL, -- tempo total respondido (ex: 00:10:23)
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
);

-- Tabela de Comentários
CREATE TABLE comentarios (
    id SERIAL PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    texto TEXT NOT NULL,
    data_comentario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
