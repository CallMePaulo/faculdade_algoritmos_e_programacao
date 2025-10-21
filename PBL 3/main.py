# main.py

# Importa todas as funções, a lista 'movimentacoes' e configurações do func.py
# NOTA: O código anterior foi enviado como um bloco único, assumindo um ficheiro
# chamado func.py com todas as funções dentro.
from func import * # O loop principal, que é o coração do programa

rodando = True

while rodando:
    # A variável 'rodando' é atualizada com o valor retornado por menu().
    # Se a opção 4 for selecionada, menu() retorna False e o loop termina.
    rodando = menu()
    
# Mensagem de finalização
print("Programa finalizado.")