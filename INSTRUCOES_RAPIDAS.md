# 🚀 INSTRUÇÕES RÁPIDAS - Sistema de Gestão de Tickets

## ⚡ Começar em 5 minutos!

### 1. **Configurar Banco de Dados**
```sql
CREATE DATABASE gestao_tickets;
```

### 2. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 3. **Configurar Conexão** (se necessário)
Edite `config.py` com suas credenciais MySQL:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'gestao_tickets',
    'user': 'root',
    'password': 'sua_senha_aqui',
    'port': 3306
}
```

### 4. **Executar Exemplos** (opcional)
```bash
python exemplo_uso.py
```

### 5. **Iniciar Aplicação**
```bash
python tickets_app.py
```

## 🎯 **Primeiro Acesso**

1. **Clique em "Criar Nova Conta"**
2. **Preencha seus dados**
3. **Faça login**
4. **Comece a usar!**

## 📱 **Funcionalidades Principais**

- **Dashboard**: Estatísticas e visão geral
- **Meus Tickets**: Visualizar e gerenciar tickets
- **Novo Ticket**: Criar solicitações
- **Usuários**: Gerenciar usuários (apenas admin)

## 🔧 **Arquivos Importantes**

- `tickets_app.py` - Aplicação principal
- `database.py` - Gerenciador do banco
- `*.ui` - Interfaces do Qt Designer
- `config.py` - Configurações

## ❓ **Problemas Comuns**

### **Erro de Conexão MySQL**
- Verifique se o MySQL está rodando
- Confirme o nome do banco: `gestao_tickets`
- Verifique usuário/senha no `config.py`

### **Módulos não encontrados**
```bash
pip install PyQt5 mysql-connector-python
```

### **Interface não carrega**
- Verifique se todos os arquivos `.ui` estão presentes
- Confirme instalação do PyQt5

## 📞 **Suporte**

- Leia o `README.md` completo
- Execute `exemplo_uso.py` para testes
- Verifique logs no terminal

---

**🎉 Pronto! Seu sistema de tickets está funcionando!**
