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
                larg_val = f"R${registro[2]:.2f}".center(larg)
                larg_dat = str(registro[3]).center(larg)
                
                dados_form = f"{larg_tip} | {larg_des} | {larg_val} | {larg_dat}"
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