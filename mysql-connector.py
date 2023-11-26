import mysql.connector
import string
import random


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# configuração do banco 
config = {
    'user':'root',
    'password':'root',
    'host':'localhost',
    'database':'metrica_AB',
    'raise_on_warnings': True
}

def connect():
    try:
        connection = mysql.connector.connect(**config)
        print("Conexão estabelecida com sucesso!")
        return connection
    except mysql.connector.Error as err:
        print(f'Erro:{err}')
        return None

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


# Função para criar a tabela (apenas uma vez)
def Criar_tabela():
    connection = connect()
    if connection is not None:
        cursor = connection.cursor()
#        verificando se a tabela ja existe
        cursor.execute('SHOW TABLES LIKE "usuario"')
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuario (
                    email VARCHAR(255) PRIMARY KEY NOT NULL,
                    tolken CHAR(6) NOT NULL
                );
            ''')
            print('tabela criada com sucesso!')
        else:
            print('tabela ja existe!!')
        connection.commit()
        connection.close()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#função para gerar uma senha aleatoria de 6 digitos
def Gerar_Senha():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    tamanho_senha = 6

    while True:
        tolken = ''.join(random.sample(caracteres, tamanho_senha))
        if(any(c.islower() for c in tolken) and
           any(c.isupper() for c in tolken) and
           any(c.isdigit() for c in tolken) and
           any(c in string.punctuation for c in tolken)):
           return tolken


#Função para validar os dados
def Validar_Dados(email):
    if  ' ' in email.strip() or email.strip() == '':
        return False
    return True


# Função para inserir um novo usuário
def criar_usuario():
    try:
        email = input("digite seu email: ")
        tolken = Gerar_Senha()
        if not Validar_Dados(email):
            print('Erro: digite um email valido!')
            return

        connection = connect()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO usuario (email, tolken) VALUES(%s, %s)''',(email, tolken))
            connection.commit()
            connection.close()
            print(f'USUARIO CRIADO COM SUCESSO, seu tolken é {tolken}') 
    except Exception as e:
        print(f'erro{e}')

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Funçõao para Listar todos os usuarios
def Listar_usuarios():
    connection = connect()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute('''SELECT email FROM usuario''')
        usuarios = cursor.fetchall()
        connection.commit()
        connection.close()
        return usuarios

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Criar_tabela()

opcao = input('deseja adicionar um novo email? ')
if opcao == 'sim':
    criar_usuario()
else:
    usuarios = Listar_usuarios()
    print(f'{usuarios}')
