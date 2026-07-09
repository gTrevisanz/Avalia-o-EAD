import os
import csv

ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_LIVROS = "livros.csv"

MATRIZ_USUARIOS = []
MATRIZ_LIVROS = []
USUARIO_LOGADO = None


def carregar_dados():
    """Carrega os dados dos arquivos CSV para as matrizes na memória se existirem."""
    global MATRIZ_USUARIOS, MATRIZ_LIVROS
    
    
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, mode='r', encoding='utf-8', newline='') as f:
            leitor = csv.reader(f)
            MATRIZ_USUARIOS = list(leitor)
            
  
    if os.path.exists(ARQUIVO_LIVROS):
        with open(ARQUIVO_LIVROS, mode='r', encoding='utf-8', newline='') as f:
            leitor = csv.reader(f)
            
            for linha in leitor:
                if len(linha) == 10:
                    linha[7] = int(linha[7])  
                    linha[8] = int(linha[8])  #
                    MATRIZ_LIVROS.append(linha)

def salvar_usuarios():
    """Salva a matriz atual de usuários no arquivo CSV."""
    with open(ARQUIVO_USUARIOS, mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerows(MATRIZ_USUARIOS)

def salvar_livros():
    """Salva a matriz atual de livros no arquivo CSV."""
    with open(ARQUIVO_LIVROS, mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerows(MATRIZ_LIVROS)




def verificar_usuario_existente(username_procurado):
    for usuario in MATRIZ_USUARIOS:
        if usuario[1] == username_procurado:
            return True
    return False

def buscar_nome_usuario(username_alvo):
    for usuario in MATRIZ_USUARIOS:
        if usuario[1] == username_alvo:
            return usuario[0]
    return ""

def registrar_usuario():
    print("\nREGISTRO DE USUÁRIO")
    nome = input("Nome completo: ")
    username = input("Username (login): ").strip().lower()
    
    if verificar_usuario_existente(username):
        print("Erro: Este username já está em uso!")
        return
        
    senha = input("Senha: ")
    nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    
    novo_usuario = [nome, username, senha, nascimento]
    MATRIZ_USUARIOS.append(novo_usuario)
    
    salvar_usuarios() 
    print(f"Usuário '{username}' registrado com sucesso!")

def validar_credenciais(username_digitado, senha_digitada):
    for usuario in MATRIZ_USUARIOS:
        if usuario[1] == username_digitado and usuario[2] == senha_digitada:
            return True
    return False

def login_usuario():
    global USUARIO_LOGADO
    print("\nLOGIN")
    username = input("Username: ").strip().lower()
    senha = input("Senha: ")
    
    if validar_credenciais(username, senha):
        USUARIO_LOGADO = username
        nome_completo = buscar_nome_usuario(username)
        print(f"Bem-vindo(a), {nome_completo}!")
    else:
        print("Erro: Username ou senha incorretos.")

def exibir_dados_usuario():
    if not USUARIO_LOGADO:
        print("Necessário estar logado.")
        return
        
    for usuario in MATRIZ_USUARIOS:
        if usuario[1] == USUARIO_LOGADO:
            print("\nMEUS DADOS")
            print(f"Nome: {usuario[0]}")
            print(f"Username: {usuario[1]}")
            print(f"Data de Nascimento: {usuario[3]}")
            return

def editar_usuario():
    global USUARIO_LOGADO
    if not USUARIO_LOGADO:
        print("Necessário estar logado.")
        return
        
    for i in range(len(MATRIZ_USUARIOS)):
        if MATRIZ_USUARIOS[i][1] == USUARIO_LOGADO:
            print("\nEDITAR DADOS")
            MATRIZ_USUARIOS[i][0] = input(f"Novo Nome [{MATRIZ_USUARIOS[i][0]}]: ") or MATRIZ_USUARIOS[i][0]
            MATRIZ_USUARIOS[i][2] = input("Nova Senha: ") or MATRIZ_USUARIOS[i][2]
            MATRIZ_USUARIOS[i][3] = input(f"Nova Data Nasc. [{MATRIZ_USUARIOS[i][3]}]: ") or MATRIZ_USUARIOS[i][3]
            
            salvar_usuarios()  
            print("Dados atualizados com sucesso!")
            return

def excluir_usuario():
    global USUARIO_LOGADO
    if not USUARIO_LOGADO:
        print("Necessário estar logado.")
        return
        
    certeza = input("Tem certeza que deseja excluir sua conta? (S/N): ").upper()
    if certeza == 'S':
        for i in range(len(MATRIZ_USUARIOS)):
            if MATRIZ_USUARIOS[i][1] == USUARIO_LOGADO:
                MATRIZ_USUARIOS.pop(i)
                salvar_usuarios()  
                
                
                global MATRIZ_LIVROS
                MATRIZ_LIVROS = [livro for livro in MATRIZ_LIVROS if livro[9] != USUARIO_LOGADO]
                salvar_livros()
                
                print("Conta excluída com sucesso.")
                USUARIO_LOGADO = None
                return
    else:
        print("Operação cancelada.")

def cadastrar_livro():
    if not USUARIO_LOGADO:
        print("Faça login para gerenciar livros.")
        return
        
    print("\nCADASTRO DE LIVRO")
    titulo = input("Título: ")
    autor = input("Autor: ")
    editora = input("Editora: ")
    edicao = input("Edição: ")
    year = input("Ano: ")
    isbn = input("ISBN: ")
    status = input("Status (Quero ler / Lendo / Lido): ")
    
    try:
        paginas_totais = int(input("Páginas Totais: "))
        paginas_lidas = int(input("Páginas Lidas: "))
    except ValueError:
        print("Erro: Páginas devem ser números inteiros.")
        return
        
    novo_livro = [titulo, autor, editora, edicao, year, isbn, status, paginas_totais, paginas_lidas, USUARIO_LOGADO]
    MATRIZ_LIVROS.append(novo_livro)
    
    salvar_livros() 
    print(f"Livro '{titulo}' cadastrado com sucesso!")

def exibir_livros():
    if not USUARIO_LOGADO:
        print("Faça login para ver seus livros.")
        return
        
    print("\nMEUS LIVROS")
    encontrou = False
    for idx, livro in enumerate(MATRIZ_LIVROS):
        if livro[9] == USUARIO_LOGADO:
            encontrou = True
            print(f"\nID: {idx}")
            print(f"Título: {livro[0]} | Autor: {livro[1]}")
            print(f"Editora: {livro[2]} | Edição: {livro[3]} | Ano: {livro[4]}")
            print(f"ISBN: {livro[5]} | Status: {livro[6]}")
            print(f"Progresso: {livro[8]}/{livro[7]} páginas")
            
    if not encontrou:
        print("Nenhum livro cadastrado ainda.")

def editar_livro():
    if not USUARIO_LOGADO:
        print("Faça login primeiro.")
        return
        
    exibir_livros()
    try:
        idx = int(input("\nDigite o ID do livro que deseja editar: "))
        if idx >= len(MATRIZ_LIVROS) or MATRIZ_LIVROS[idx][9] != USUARIO_LOGADO:
            print("ID inválido ou o livro não pertence a você.")
            return
            
        print("Deixe em branco para manter o valor atual.")
        MATRIZ_LIVROS[idx][0] = input(f"Título [{MATRIZ_LIVROS[idx][0]}]: ") or MATRIZ_LIVROS[idx][0]
        MATRIZ_LIVROS[idx][1] = input(f"Autor [{MATRIZ_LIVROS[idx][1]}]: ") or MATRIZ_LIVROS[idx][1]
        MATRIZ_LIVROS[idx][6] = input(f"Status [{MATRIZ_LIVROS[idx][6]}]: ") or MATRIZ_LIVROS[idx][6]
        
        pag_lidas = input(f"Páginas Lidas [{MATRIZ_LIVROS[idx][8]}]: ")
        if pag_lidas:
            MATRIZ_LIVROS[idx][8] = int(pag_lidas)
            
        salvar_livros()  
        print("Livro updated com sucesso!")
    except ValueError:
        print("Entrada inválida.")

def remover_livro():
    if not USUARIO_LOGADO:
        print("Faça login primeiro.")
        return
        
    exibir_livros()
    try:
        idx = int(input("\nDigite o ID do livro que deseja remover: "))
        if idx >= len(MATRIZ_LIVROS) or MATRIZ_LIVROS[idx][9] != USUARIO_LOGADO:
            print("ID inválido.")
            return
            
        MATRIZ_LIVROS.pop(idx)
        salvar_livros()  
        print("Livro removido com sucesso!")
    except ValueError:
        print("Entrada inválida.")

def menu_logado():
    global USUARIO_LOGADO
    while USUARIO_LOGADO is not None:
        print(f"\n BOOKTRACK (Logado como: {USUARIO_LOGADO})")
        print("1. Meus Dados")
        print("2. Editar Perfil")
        print("3. Excluir Conta")
        print("4. Cadastrar Livro")
        print("5. Listar Meus Livros")
        print("6. Editar Livro")
        print("7. Remover Livro")
        print("8. Logout")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1': exibir_dados_usuario()
        elif opcao == '2': editar_usuario()
        elif opcao == '3': excluir_usuario()
        elif opcao == '4': cadastrar_livro()
        elif opcao == '5': exibir_livros()
        elif opcao == '6': editar_livro()
        elif opcao == '7': remover_livro()
        elif opcao == '8':
            print("Saindo da conta...")
            USUARIO_LOGADO = None
        else:
            print("Opção inválida.")

def menu_principal():
    while True:
        print("BEM-VINDO AO BOOKTRACK")
        print("1. Fazer Login")
        print("2. Registrar Novo Usuário")
        print("3. Sair do Programa")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            login_usuario()
            if USUARIO_LOGADO:
                menu_logado()
        elif opcao == '2':
            registrar_usuario()
        elif opcao == '3':
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    carregar_dados()  # Inicializa o sistema carregando os dados salvos previamente
    menu_principal()
