#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do Sistema de Gestão de Tickets

Este arquivo demonstra como usar as principais funcionalidades do sistema.
Execute este arquivo para ver exemplos práticos.
"""

from database import DatabaseManager
from datetime import datetime

def exemplo_criar_usuarios():
    """Exemplo de criação de usuários"""
    print("=== Criando Usuários de Exemplo ===")
    
    db = DatabaseManager()
    
    # Criar usuário administrador
    if db.create_user("Admin", "admin@exemplo.com", "admin123", "admin"):
        print("✅ Usuário administrador criado com sucesso!")
    else:
        print("❌ Erro ao criar usuário administrador")
    
    # Criar usuário cliente
    if db.create_user("João Silva", "joao@exemplo.com", "123456", "cliente"):
        print("✅ Usuário cliente criado com sucesso!")
    else:
        print("❌ Erro ao criar usuário cliente")
    
    # Criar mais alguns usuários
    usuarios_exemplo = [
        ("Maria Santos", "maria@exemplo.com", "123456", "cliente"),
        ("Pedro Costa", "pedro@exemplo.com", "123456", "cliente"),
        ("Ana Oliveira", "ana@exemplo.com", "123456", "cliente")
    ]
    
    for nome, email, senha, tipo in usuarios_exemplo:
        if db.create_user(nome, email, senha, tipo):
            print(f"✅ Usuário {nome} criado com sucesso!")
        else:
            print(f"❌ Erro ao criar usuário {nome}")
    
    print()

def exemplo_criar_tickets():
    """Exemplo de criação de tickets"""
    print("=== Criando Tickets de Exemplo ===")
    
    db = DatabaseManager()
    
    # Autenticar um usuário para criar tickets
    user = db.authenticate_user("joao@exemplo.com", "123456")
    if not user:
        print("❌ Usuário não encontrado para criar tickets")
        return
    
    # Criar alguns tickets de exemplo
    tickets_exemplo = [
        ("Problema com Login", "Não consigo fazer login no sistema, aparece erro de senha incorreta."),
        ("Solicitação de Nova Funcionalidade", "Gostaria de solicitar a implementação de um sistema de notificações por email."),
        ("Bug na Interface", "A interface está com problemas de layout em telas pequenas."),
        ("Dúvida sobre Uso", "Como faço para alterar minha senha no sistema?"),
        ("Relatório de Erro", "O sistema está apresentando erro 500 ao tentar gerar relatórios.")
    ]
    
    for titulo, descricao in tickets_exemplo:
        ticket_id = db.create_ticket(titulo, descricao, user['id'])
        if ticket_id:
            print(f"✅ Ticket '{titulo}' criado com ID: {ticket_id}")
        else:
            print(f"❌ Erro ao criar ticket '{titulo}'")
    
    print()

def exemplo_listar_tickets():
    """Exemplo de listagem de tickets"""
    print("=== Listando Tickets ===")
    
    db = DatabaseManager()
    
    # Listar todos os tickets
    tickets = db.get_tickets()
    print(f"Total de tickets: {len(tickets)}")
    
    for ticket in tickets:
        print(f"ID: {ticket['id']} | Título: {ticket['titulo']} | Status: {ticket['status']}")
    
    print()
    
    # Listar tickets por status
    print("=== Tickets por Status ===")
    for status in ['aberto', 'pausado', 'fechado']:
        tickets_status = db.get_tickets(status=status)
        print(f"Status '{status}': {len(tickets_status)} tickets")
    
    print()

def exemplo_autenticacao():
    """Exemplo de autenticação de usuários"""
    print("=== Testando Autenticação ===")
    
    db = DatabaseManager()
    
    # Testar login com usuário válido
    user = db.authenticate_user("admin@exemplo.com", "admin123")
    if user:
        print(f"✅ Login bem-sucedido: {user['nome']} ({user['tipo']})")
    else:
        print("❌ Login falhou para admin")
    
    # Testar login com usuário cliente
    user = db.authenticate_user("joao@exemplo.com", "123456")
    if user:
        print(f"✅ Login bem-sucedido: {user['nome']} ({user['tipo']})")
    else:
        print("❌ Login falhou para joao")
    
    # Testar login com credenciais inválidas
    user = db.authenticate_user("usuario@inexistente.com", "senhaerrada")
    if user:
        print("❌ Login inesperadamente bem-sucedido")
    else:
        print("✅ Login falhou corretamente para usuário inexistente")
    
    print()

def exemplo_comentarios():
    """Exemplo de criação de comentários"""
    print("=== Criando Comentários de Exemplo ===")
    
    db = DatabaseManager()
    
    # Autenticar usuários
    admin = db.authenticate_user("admin@exemplo.com", "admin123")
    cliente = db.authenticate_user("joao@exemplo.com", "123456")
    
    if not admin or not cliente:
        print("❌ Usuários não encontrados para criar comentários")
        return
    
    # Buscar um ticket para comentar
    tickets = db.get_tickets()
    if not tickets:
        print("❌ Nenhum ticket encontrado para comentar")
        return
    
    ticket = tickets[0]
    
    # Criar comentários
    comentarios = [
        (cliente['id'], "Olá! Preciso de ajuda com este problema."),
        (admin['id'], "Olá! Vou analisar seu ticket e retornar em breve."),
        (cliente['id'], "Obrigado! Aguardo o retorno."),
        (admin['id'], "Ticket analisado. Solução implementada na próxima atualização.")
    ]
    
    for usuario_id, texto in comentarios:
        if db.add_comment(ticket['id'], usuario_id, texto):
            print(f"✅ Comentário adicionado: {texto[:50]}...")
        else:
            print(f"❌ Erro ao adicionar comentário")
    
    # Listar comentários do ticket
    print(f"\n=== Comentários do Ticket {ticket['id']} ===")
    comentarios = db.get_comments(ticket['id'])
    for comentario in comentarios:
        print(f"{comentario['usuario_nome']}: {comentario['texto']}")
    
    print()

def main():
    """Função principal que executa todos os exemplos"""
    print("🎫 SISTEMA DE GESTÃO DE TICKETS - EXEMPLOS DE USO")
    print("=" * 60)
    print()
    
    try:
        # Executar exemplos
        exemplo_criar_usuarios()
        exemplo_criar_tickets()
        exemplo_listar_tickets()
        exemplo_autenticacao()
        exemplo_comentarios()
        
        print("🎉 Todos os exemplos foram executados com sucesso!")
        print("\nAgora você pode executar a aplicação principal:")
        print("python tickets_app.py")
        
    except Exception as e:
        print(f"❌ Erro durante a execução dos exemplos: {e}")
        print("\nVerifique se:")
        print("1. O MySQL está rodando")
        print("2. O banco 'gestao_tickets' foi criado")
        print("3. As credenciais estão corretas no arquivo database.py")

if __name__ == "__main__":
    main()
