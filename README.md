# Sistema de Gestão de Tickets

Um sistema completo de gestão de tickets desenvolvido em Python com interface gráfica usando PyQt5 e banco de dados MySQL.

## 🚀 Funcionalidades

- **Sistema de Login/Registro**: Autenticação segura com hash de senhas
- **Dashboard**: Visualização de estatísticas e tickets recentes
- **Gestão de Tickets**: Criação, visualização e acompanhamento de tickets
- **Filtros**: Filtros por status (Aberto, Pausado, Fechado)
- **Controle de Acesso**: Diferentes níveis de usuário (Admin/Cliente)
- **Interface Moderna**: Design responsivo e intuitivo

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **PyQt5**: Interface gráfica
- **MySQL**: Banco de dados
- **Qt Designer**: Criação das interfaces

## 📋 Pré-requisitos

1. **Python 3.8 ou superior**
2. **MySQL Server** instalado e rodando
3. **Banco de dados** criado

## 🗄️ Configuração do Banco de Dados

### 1. Criar o banco de dados:
```sql
CREATE DATABASE gestao_tickets;
USE gestao_tickets;
```

### 2. As tabelas serão criadas automaticamente pelo sistema, mas você pode executar manualmente:

```sql
-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'cliente') NOT NULL
);

-- Tabela de tickets
CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    cliente_id INT NOT NULL,
    status ENUM('aberto', 'pausado', 'fechado') DEFAULT 'aberto',
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tempo_resposta TIME DEFAULT '00:00:00',
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
);

-- Tabela de comentários
CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    texto TEXT NOT NULL,
    data_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

## ⚙️ Instalação

### 1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd sistema-tickets
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configure a conexão com o banco:
Edite o arquivo `database.py` e ajuste as configurações de conexão:

```python
self.connection = mysql.connector.connect(
    host='localhost',           # Seu host MySQL
    database='gestao_tickets',  # Nome do banco
    user='root',                # Seu usuário MySQL
    password=''                 # Sua senha MySQL
)
```

## 🚀 Como Executar

### 1. Execute a aplicação:
```bash
python tickets_app.py
```

### 2. Na primeira execução, crie um usuário administrador:
- Clique em "Criar Nova Conta"
- Preencha os dados
- Faça login

## 📱 Como Usar

### **Login/Registro**
- Use o email e senha para fazer login
- Clique em "Criar Nova Conta" para se registrar

### **Dashboard**
- Visualize estatísticas dos tickets
- Veja tickets recentes
- Acesse todas as funcionalidades

### **Tickets**
- **Meus Tickets**: Visualize todos os seus tickets
- **Novo Ticket**: Crie um novo ticket
- **Filtros**: Filtre por status

### **Usuários** (Apenas Admin)
- Gerencie usuários do sistema
- Adicione novos usuários

## 🔧 Estrutura do Projeto

```
sistema-tickets/
├── database.py          # Gerenciador do banco de dados
├── login.ui            # Interface de login (Qt Designer)
├── register.ui         # Interface de registro (Qt Designer)
├── tickets_main.ui     # Interface principal (Qt Designer)
├── tickets_app.py      # Aplicação principal
├── requirements.txt    # Dependências
└── README.md          # Este arquivo
```

## 🎨 Personalização

### **Interfaces**
- Edite os arquivos `.ui` no Qt Designer
- Regenere os arquivos Python se necessário

### **Estilos**
- Modifique os arquivos `.ui` para alterar cores e layouts
- Use CSS-like styling do Qt

### **Funcionalidades**
- Adicione novas funcionalidades no arquivo `tickets_app.py`
- Implemente novos métodos na classe `DatabaseManager`

## 🐛 Solução de Problemas

### **Erro de Conexão com MySQL**
- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo `database.py`
- Verifique se o banco `gestao_tickets` existe

### **Erro de Módulos**
- Execute: `pip install -r requirements.txt`
- Verifique se o Python 3.8+ está instalado

### **Interface não carrega**
- Verifique se todos os arquivos `.ui` estão presentes
- Confirme se o PyQt5 está instalado corretamente

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📞 Suporte

Para suporte ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento

---

**Desenvolvido com ❤️ usando Python e PyQt5**
