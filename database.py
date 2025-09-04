import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Conecta ao banco de dados MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='tiflux_db',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                print("Conectado ao banco de dados MySQL")
                self.create_tables()
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
    
    def create_tables(self):
        """Cria as tabelas se não existirem"""
        try:
            cursor = self.connection.cursor()
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    senha VARCHAR(255) NOT NULL,
                    tipo ENUM('admin', 'cliente') NOT NULL
                )
            """)
            
            # Tabela de tickets
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    descricao TEXT,
                    cliente_id INT NOT NULL,
                    status ENUM('aberto', 'pausado', 'fechado') DEFAULT 'aberto',
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tempo_resposta TIME DEFAULT '00:00:00',
                    FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
                )
            """)
            
            # Tabela de comentários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comentarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ticket_id INT NOT NULL,
                    usuario_id INT NOT NULL,
                    texto TEXT NOT NULL,
                    data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)
            
            self.connection.commit()
            cursor.close()
            print("Tabelas criadas/verificadas com sucesso")
            
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
    
    def hash_password(self, password):
        """Cria hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, nome, email, senha, tipo='cliente'):
        """Cria um novo usuário"""
        try:
            cursor = self.connection.cursor()
            hashed_password = self.hash_password(senha)
            
            query = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nome, email, hashed_password, tipo))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erro ao criar usuário: {e}")
            return False
    
    def authenticate_user(self, email, senha):
        """Autentica um usuário"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            hashed_password = self.hash_password(senha)
            
            query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
            cursor.execute(query, (email, hashed_password))
            
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Erro na autenticação: {e}")
            return None
    
    def create_ticket(self, titulo, descricao, cliente_id):
        """Cria um novo ticket"""
        try:
            cursor = self.connection.cursor()
            
            query = "INSERT INTO tickets (titulo, descricao, cliente_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (titulo, descricao, cliente_id))
            
            self.connection.commit()
            ticket_id = cursor.lastrowid
            cursor.close()
            return ticket_id
        except Error as e:
            print(f"Erro ao criar ticket: {e}")
            return None
    
    def get_tickets(self, user_id=None, status=None):
        """Busca tickets com filtros opcionais"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if user_id and status:
                query = """
                    SELECT t.*, u.nome as cliente_nome 
                    FROM tickets t 
                    JOIN usuarios u ON t.cliente_id = u.id 
                    WHERE t.cliente_id = %s AND t.status = %s
                    ORDER BY t.data_criacao DESC
                """
                cursor.execute(query, (user_id, status))
            elif user_id:
                query = """
                    SELECT t.*, u.nome as cliente_nome 
                    FROM tickets t 
                    JOIN usuarios u ON t.cliente_id = u.id 
                    WHERE t.cliente_id = %s
                    ORDER BY t.data_criacao DESC
                """
                cursor.execute(query, (user_id,))
            elif status:
                query = """
                    SELECT t.*, u.nome as cliente_nome 
                    FROM tickets t 
                    JOIN usuarios u ON t.cliente_id = u.id 
                    WHERE t.status = %s
                    ORDER BY t.data_criacao DESC
                """
                cursor.execute(query, (status,))
            else:
                query = """
                    SELECT t.*, u.nome as cliente_nome 
                    FROM tickets t 
                    JOIN usuarios u ON t.cliente_id = u.id 
                    ORDER BY t.data_criacao DESC
                """
                cursor.execute(query)
            
            tickets = cursor.fetchall()
            cursor.close()
            return tickets
        except Error as e:
            print(f"Erro ao buscar tickets: {e}")
            return []
    
    def update_ticket_status(self, ticket_id, status):
        """Atualiza o status de um ticket"""
        try:
            cursor = self.connection.cursor()
            
            query = "UPDATE tickets SET status = %s WHERE id = %s"
            cursor.execute(query, (status, ticket_id))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erro ao atualizar ticket: {e}")
            return False
    
    def add_comment(self, ticket_id, usuario_id, texto):
        """Adiciona um comentário a um ticket"""
        try:
            cursor = self.connection.cursor()
            
            query = "INSERT INTO comentarios (ticket_id, usuario_id, texto) VALUES (%s, %s, %s)"
            cursor.execute(query, (ticket_id, usuario_id, texto))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erro ao adicionar comentário: {e}")
            return False
    
    def get_comments(self, ticket_id):
        """Busca comentários de um ticket"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT c.*, u.nome as usuario_nome 
                FROM comentarios c 
                JOIN usuarios u ON c.usuario_id = u.id 
                WHERE c.ticket_id = %s 
                ORDER BY c.data_comentario ASC
            """
            cursor.execute(query, (ticket_id,))
            
            comments = cursor.fetchall()
            cursor.close()
            return comments
        except Error as e:
            print(f"Erro ao buscar comentários: {e}")
            return []
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o banco fechada")
