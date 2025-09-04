import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QComboBox,
                             QFrame, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
from database import DatabaseManager

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Carrega a interface de login
        uic.loadUi('login.ui', self)
        self.db = DatabaseManager()
        self.setup_connections()
        
    def setup_connections(self):
        """Configura as conexões dos botões"""
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.show_register)
        
    def login(self):
        """Realiza o login do usuário"""
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()
        
        if not email or not senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
            
        user = self.db.authenticate_user(email, senha)
        if user:
            self.hide()
            self.main_window = MainTicketsWindow(user, self.db)
            self.main_window.show()
        else:
            QMessageBox.critical(self, "Erro", "Email ou senha incorretos!")
            
    def show_register(self):
        """Mostra a janela de registro"""
        self.hide()
        self.register_window = RegisterWindow(self.db, self)
        self.register_window.show()

class RegisterWindow(QMainWindow):
    def __init__(self, db, login_window):
        super().__init__()
        self.db = db
        self.login_window = login_window
        uic.loadUi('register.ui', self)
        self.setup_connections()
        
    def setup_connections(self):
        """Configura as conexões dos botões"""
        self.register_btn.clicked.connect(self.register_user)
        self.back_btn.clicked.connect(self.back_to_login)
        
    def register_user(self):
        """Registra um novo usuário"""
        nome = self.nome_input.text().strip()
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()
        confirmar_senha = self.confirmar_senha_input.text().strip()
        
        if not nome or not email or not senha or not confirmar_senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
            
        if senha != confirmar_senha:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return
            
        if len(senha) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres!")
            return
            
        if self.db.create_user(nome, email, senha):
            QMessageBox.information(self, "Sucesso", "Usuário criado com sucesso!")
            self.back_to_login()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao criar usuário. Email já pode estar em uso.")
            
    def back_to_login(self):
        """Volta para a tela de login"""
        self.hide()
        self.login_window.show()

class MainTicketsWindow(QMainWindow):
    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        uic.loadUi('tickets_main.ui', self)
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
    def setup_ui(self):
        """Configura a interface inicial"""
        # Configura o filtro de status
        self.status_filter.addItems(['Todos', 'Aberto', 'Pausado', 'Fechado'])
        
        # Configura as tabelas
        self.setup_tickets_table()
        self.setup_recent_tickets_table()
        self.setup_users_table()
        
        # Seleciona o dashboard por padrão
        self.dashboard_btn.setChecked(True)
        self.stackedWidget.setCurrentIndex(0)
        
    def setup_tickets_table(self):
        """Configura a tabela de tickets"""
        headers = ['ID', 'Título', 'Status', 'Data Criação', 'Ações']
        self.tickets_table.setColumnCount(len(headers))
        self.tickets_table.setHorizontalHeaderLabels(headers)
        self.tickets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def setup_recent_tickets_table(self):
        """Configura a tabela de tickets recentes"""
        headers = ['ID', 'Título', 'Status', 'Data Criação']
        self.recent_tickets_table.setColumnCount(len(headers))
        self.recent_tickets_table.setHorizontalHeaderLabels(headers)
        self.recent_tickets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def setup_users_table(self):
        """Configura a tabela de usuários"""
        headers = ['ID', 'Nome', 'Email', 'Tipo']
        self.users_table.setColumnCount(len(headers))
        self.users_table.setHorizontalHeaderLabels(headers)
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def setup_connections(self):
        """Configura as conexões dos botões"""
        # Botões da sidebar
        self.dashboard_btn.clicked.connect(lambda: self.change_page(0))
        self.tickets_btn.clicked.connect(lambda: self.change_page(1))
        self.new_ticket_btn.clicked.connect(lambda: self.change_page(2))
        self.users_btn.clicked.connect(lambda: self.change_page(3))
        self.logout_btn.clicked.connect(self.logout)
        
        # Botões de funcionalidade
        self.criar_ticket_btn.clicked.connect(self.create_ticket)
        self.cancelar_btn.clicked.connect(self.clear_ticket_form)
        self.add_user_btn.clicked.connect(self.show_add_user_dialog)
        
        # Filtros
        self.status_filter.currentTextChanged.connect(self.filter_tickets)
        
    def change_page(self, index):
        """Muda a página do stacked widget"""
        # Desmarca todos os botões
        for btn in [self.dashboard_btn, self.tickets_btn, self.new_ticket_btn, self.users_btn]:
            btn.setChecked(False)
            
        # Marca o botão correto
        if index == 0:
            self.dashboard_btn.setChecked(True)
        elif index == 1:
            self.tickets_btn.setChecked(True)
        elif index == 2:
            self.new_ticket_btn.setChecked(True)
        elif index == 3:
            self.users_btn.setChecked(True)
            
        self.stackedWidget.setCurrentIndex(index)
        
        # Recarrega os dados da página
        if index == 0:
            self.load_dashboard()
        elif index == 1:
            self.load_tickets()
        elif index == 3:
            self.load_users()
            
    def load_data(self):
        """Carrega todos os dados iniciais"""
        self.load_dashboard()
        
    def load_dashboard(self):
        """Carrega os dados do dashboard"""
        # Busca estatísticas
        tickets_abertos = len(self.db.get_tickets(status='aberto'))
        tickets_pausados = len(self.db.get_tickets(status='pausado'))
        tickets_fechados = len(self.db.get_tickets(status='fechado'))
        
        # Atualiza labels
        self.tickets_abertos_label.setText(str(tickets_abertos))
        self.tickets_pausados_label.setText(str(tickets_pausados))
        self.tickets_fechados_label.setText(str(tickets_fechados))
        
        # Carrega tickets recentes
        recent_tickets = self.db.get_tickets()[:5]  # Últimos 5 tickets
        self.load_recent_tickets_table(recent_tickets)
        
    def load_recent_tickets_table(self, tickets):
        """Carrega a tabela de tickets recentes"""
        self.recent_tickets_table.setRowCount(len(tickets))
        
        for row, ticket in enumerate(tickets):
            self.recent_tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket['id'])))
            self.recent_tickets_table.setItem(row, 1, QTableWidgetItem(ticket['titulo']))
            self.recent_tickets_table.setItem(row, 2, QTableWidgetItem(ticket['status'].title()))
            self.recent_tickets_table.setItem(row, 3, QTableWidgetItem(str(ticket['data_criacao'])))
            
    def load_tickets(self):
        """Carrega a lista de tickets"""
        if self.user['tipo'] == 'cliente':
            tickets = self.db.get_tickets(user_id=self.user['id'])
        else:
            tickets = self.db.get_tickets()
            
        self.tickets_table.setRowCount(len(tickets))
        
        for row, ticket in enumerate(tickets):
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket['id'])))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket['titulo']))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket['status'].title()))
            self.tickets_table.setItem(row, 3, QTableWidgetItem(str(ticket['data_criacao'])))
            
            # Botão de ação
            action_btn = QPushButton("Ver Detalhes")
            action_btn.clicked.connect(lambda checked, t=ticket: self.show_ticket_details(t))
            self.tickets_table.setCellWidget(row, 4, action_btn)
            
    def filter_tickets(self):
        """Filtra tickets por status"""
        status_filter = self.status_filter.currentText()
        
        if status_filter == 'Todos':
            if self.user['tipo'] == 'cliente':
                tickets = self.db.get_tickets(user_id=self.user['id'])
            else:
                tickets = self.db.get_tickets()
        else:
            status_map = {'Aberto': 'aberto', 'Pausado': 'pausado', 'Fechado': 'fechado'}
            status = status_map.get(status_filter, 'aberto')
            
            if self.user['tipo'] == 'cliente':
                tickets = self.db.get_tickets(user_id=self.user['id'], status=status)
            else:
                tickets = self.db.get_tickets(status=status)
                
        self.tickets_table.setRowCount(len(tickets))
        
        for row, ticket in enumerate(tickets):
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket['id'])))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket['titulo']))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket['status'].title()))
            self.tickets_table.setItem(row, 3, QTableWidgetItem(str(ticket['data_criacao'])))
            
            # Botão de ação
            action_btn = QPushButton("Ver Detalhes")
            action_btn.clicked.connect(lambda checked, t=ticket: self.show_ticket_details(t))
            self.tickets_table.setCellWidget(row, 4, action_btn)
            
    def create_ticket(self):
        """Cria um novo ticket"""
        titulo = self.titulo_input.text().strip()
        descricao = self.descricao_input.toPlainText().strip()
        
        if not titulo or not descricao:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
            
        ticket_id = self.db.create_ticket(titulo, descricao, self.user['id'])
        if ticket_id:
            QMessageBox.information(self, "Sucesso", "Ticket criado com sucesso!")
            self.clear_ticket_form()
            self.load_dashboard()  # Recarrega dashboard
        else:
            QMessageBox.critical(self, "Erro", "Erro ao criar ticket!")
            
    def clear_ticket_form(self):
        """Limpa o formulário de ticket"""
        self.titulo_input.clear()
        self.descricao_input.clear()
        
    def load_users(self):
        """Carrega a lista de usuários (apenas para admins)"""
        if self.user['tipo'] != 'admin':
            QMessageBox.warning(self, "Acesso Negado", "Apenas administradores podem ver esta página!")
            self.change_page(0)
            return
            
        # Aqui você implementaria a busca de usuários no banco
        # Por enquanto, mostra apenas o usuário atual
        self.users_table.setRowCount(1)
        self.users_table.setItem(0, 0, QTableWidgetItem(str(self.user['id'])))
        self.users_table.setItem(0, 1, QTableWidgetItem(self.user['nome']))
        self.users_table.setItem(0, 2, QTableWidgetItem(self.user['email']))
        self.users_table.setItem(0, 3, QTableWidgetItem(self.user['tipo'].title()))
        
    def show_add_user_dialog(self):
        """Mostra diálogo para adicionar usuário"""
        if self.user['tipo'] != 'admin':
            QMessageBox.warning(self, "Acesso Negado", "Apenas administradores podem adicionar usuários!")
            return
            
        # Implementar diálogo de adição de usuário
        QMessageBox.information(self, "Info", "Funcionalidade de adicionar usuário será implementada!")
        
    def show_ticket_details(self, ticket):
        """Mostra detalhes de um ticket"""
        # Implementar visualização detalhada do ticket
        QMessageBox.information(self, "Detalhes do Ticket", 
                              f"Título: {ticket['titulo']}\n"
                              f"Status: {ticket['status']}\n"
                              f"Data: {ticket['data_criacao']}\n"
                              f"Descrição: {ticket['descricao']}")
        
    def logout(self):
        """Faz logout do usuário"""
        reply = QMessageBox.question(self, 'Confirmar Logout', 
                                   'Deseja realmente sair?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db.close()
            self.close()
            # Aqui você pode implementar o retorno à tela de login

def main():
    app = QApplication(sys.argv)
    
    # Configura o estilo da aplicação
    app.setStyle('Fusion')
    
    # Cria e mostra a janela de login
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
