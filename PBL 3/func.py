import os #--> Importa o módulo os para interagir com o sistema operacional
import sqlite3

if os.name == "nt":  # 'nt' é para Windows #--> Define o comando de limpar tela conforme o sistema operacional
    comando_limpar = "cls"
else:  # 'posix' para Linux e macOS
    comando_limpar = "clear"


# Lista onde cada item é um dicionário representando uma transação.
movimentacoes = []


def menu():
    _ = os.system(comando_limpar) #--> Limpa a tela
    print("""-------------------------------------
Olá, seja bem vindo!
Escolha uma das opções abaixo:
    (1): Registrar Movimentação
    (2): Acompanhar Saldo
    (3): Relatórios
    (4): Sair
-------------------------------------""")
    return opcao()


def opcao():
    try:
        opcao = int(input("Opção desejada: "))
    except ValueError:
        print("Entrada inválida! Digite apenas o número da opção.")
        return True

    # Inicializa 'rodando' como True por padrão (continua rodando)
    rodando = True

    match opcao:
        case 1:
            registrar_movimentacao()
        case 2:
            acompanhar_saldo()
        case 3:
            relatorios()
        case 4:
            rodando = False
            print("\nVocê selecionou a opção Sair")
            print("Obrigado por usar nosso sistema. Encerrando.")
        case _:
            print("\nOpção Inválida! Selecione uma das opções disponíveis.")
            pass

    # Retorna o valor de 'rodando' (True ou False)
    return rodando


def registrar_movimentacao():
    _ = os.system(comando_limpar)
    print("--- REGISTRAR NOVA MOVIMENTAÇÃO ---")

    # Coleta os dados necessários
    while True:
        print("Tipo de Movimentação:")
        tipo = input("Digite R para Receita e D para Despesa: ").upper() #--> Converte a entrada para maiúscula
        if tipo in ["R", "D"]:
            tipo_completo = "Receita" if tipo == "R" else "Despesa"
            break
        else:
            print("Tipo inválido. Por favor, digite R ou D")

    descricao = input("Descrição da Transação: ")
    try:
        valor = float(input("Valor da Transação (ex: 100.00): "))
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        return  # Sai da função se o valor for inválido
    categoria = input("Categoria (ex: Receita, Salário, Alimentação, Transporte): ")
    data = input("Data da Transação (DD/MM/AAAA): ")

    valor_formatado = f"{valor:.2f}" #--> Formata o valor para duas casas decimais

    # Cria o dicionário com os dados da movimentação
    nova_transacao = {
        "tipo": tipo_completo,
        "descricao": descricao,
        "valor": valor_formatado,
        "categoria": categoria,
        "data": data,
    }

    # Adiciona o dicionário à lista de movimentações
    movimentacoes.append(nova_transacao)

    print("\n✅ Movimentação Registrada com Sucesso!")

    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


def acompanhar_saldo():
    _ = os.system(comando_limpar)
    # Calcula o saldo total (Receitas - Depesas) e exibe, usando o campo 'tipo'.

    total_receitas = 0.0
    total_despesas = 0.0

    if not movimentacoes:
        print("\n🚫 Nenhuma movimentação registrada ainda. Saldo: R$0.00")

    for transacao in movimentacoes:
        # Converte a string de volta para float para realizar o cálculo
        valor = float(transacao["valor"])

        # Verifica o campo 'tipo'
        if transacao["tipo"] == "Receita":
            total_receitas += valor
        elif transacao["tipo"] == "Despesa":
            total_despesas += valor
        # Transações sem tipo válido são ignoradas

    saldo_total = total_receitas - total_despesas

    print("\n--- SALDO DISPONÍVEL ---")
    print(f"Total de Receitas: R${total_receitas:.2f}")
    print(f"Total de Despesas: R${total_despesas:.2f}")

    # Exibe o saldo em verde/vermelho (opcional, mas legal)
    cor_inicio = "\033[92m" if saldo_total >= 0 else "\033[91m"
    cor_fim = "\033[0m"

    print(f"Saldo Atual:       {cor_inicio}R${saldo_total:.2f}{cor_fim}")
    print("------------------------")

    _ = input("Pressione qualquer botão para voltar ao menu inicial.")

def limpar_tabela(nome_tabela):
    try:
        con = sqlite3.connect('relatorio.db')
        cursor = con.cursor()
        con.commit()
        cursor.execute(f'DELETE FROM {nome_tabela} ')
    except sqlite3.OperationalError as e:
        print(f'Falha no sistema {e}')
    
    finally:
        if con:
            con.close()

def relatorios():
    _ = os.system(comando_limpar)
    print("--- RELATÓRIOS ---")

    # 1. TRATAMENTO INICIAL DE DADOS
    if not movimentacoes:
        print("\n🚫 Não há movimentações para gerar relatórios.")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        return 

    # 2. AGRUPAMENTO POR CATEGORIA (O NOVO PASSO ESSENCIAL!)
    movimentacoes_por_categoria = {}
    for mov in movimentacoes:
        categoria = mov['categoria'].strip() # Pega a categoria e remove espaços
        if categoria not in movimentacoes_por_categoria:
            # Se a categoria não existe no dicionário, cria uma nova chave com uma lista vazia
            movimentacoes_por_categoria[categoria] = []
        # Adiciona a movimentação à lista da sua respectiva categoria
        movimentacoes_por_categoria[categoria].append(mov)


    con = sqlite3.connect('relatorio.db')
    cursor = con.cursor()
    
    # Este 'finally' será executado no final, não importa o que aconteça
    try:
        # A. Criação da tabela auxiliar (agora com categoria)
        cursor.execute("CREATE TABLE IF NOT EXISTS relatorio (tipo TEXT, descricao TEXT, valor REAL, data TEXT, categoria TEXT)")
        con.commit() # Garante que a criação da tabela está salva

        Larg = 80
        larg = 15 # Largura padrão da coluna

        # 3. ITERAR E GERAR RELATÓRIO PARA CADA CATEGORIA
        for categoria_nome, lista_de_movs in movimentacoes_por_categoria.items():
            
            # --- TÍTULO DINÂMICO ---
            # O nome da categoria como título do relatório!
            titulo_relatorio = f"RELATÓRIO DE MOVIMENTAÇÕES: {categoria_nome.upper()}"
            print("\n" + "=" * Larg)
            print(titulo_relatorio.center(Larg))
            print("=" * Larg)

            # B. Limpa a tabela para o relatório da categoria atual
            # Usamos a sua função original, mas garantimos que ela limpa
            limpar_tabela('relatorio') # Limpa a tabela 'relatorio' ANTES de inserir os novos dados

            # C. Inserção dos dados da categoria ATUAL no banco (staging)
            for mov in lista_de_movs:
                cursor.execute(
                    "INSERT INTO relatorio(tipo, descricao, valor, data, categoria) VALUES (?, ?, ?, ?, ?)",
                    (mov['tipo'], mov['descricao'], float(mov['valor']), mov['data'], mov['categoria'])
                )
            con.commit() # Salva apenas os dados da categoria atual
            
            # D. Busca e Exibição dos Dados da Categoria Atual
            cursor.execute('''SELECT tipo, descricao, valor, data FROM relatorio''') # Selecionamos 4 colunas para simplificar o relatório
            dados = cursor.fetchall()
            
            # Cabeçalho da Tabela
            nome_colunas_exibir = ['TIPO', 'DESCRIÇÃO', 'VALOR', 'DATA']
            tamanho_cabecalho = larg * len(nome_colunas_exibir) + (len(nome_colunas_exibir) - 1) * 3 # Calcula o tamanho do cabeçalho
            
            cabeçalho = f'{nome_colunas_exibir[0].center(larg)} | {nome_colunas_exibir[1].center(larg)} | {nome_colunas_exibir[2].center(larg)} | {nome_colunas_exibir[3].center(larg)}'
            
            print(cabeçalho)
            print('-' * tamanho_cabecalho)

            # Exibição dos Registros
            for registro in dados:
                # Registro: (tipo, descricao, valor, data)
                larg_tip = str(registro[0]).center(larg)
                larg_des = str(registro[1]).center(larg)
                larg_val = str{registro[2]}.center(larg)
                larg_dat = str(registro[3]).center(larg)
                
                dados_form = f"{larg_tip} | {larg_des} | R${larg_val:.2f} | {larg_dat}"
                print(dados_form)
            
            print("-" * tamanho_cabecalho + "\n") # Separador após cada relatório

        # 4. Finalização
        _ = input("Relatórios concluídos. Pressione qualquer botão para voltar ao menu inicial.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro no banco de dados: {e}")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        
    finally:
        # A LIMPEZA FINAL da tabela é importante, pois ela é temporária
        # Usamos a sua função original de novo
        limpar_tabela('relatorio')
        cursor.close()
        con.close()