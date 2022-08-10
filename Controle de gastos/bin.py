from Banco import Bd, Ajustes, Funcao
import datetime
data = datetime.datetime.now()
ano = data.date()
an = int(ano.year)
bd = Bd.Conector('localhost', 'root', 'root', 'controle_de_gastos')
categorias = Bd.Categoria(bd.conectar())
compras = Bd.Compra(bd.conectar())
contador, verificador = 0, 0
id_ultimo = bd.select_ultimo('id_compra', 'total_compra')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
         'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
#a = Funcao.apresentar_compras(bd.conectar(), 12, an)
while True:
    print('BEM VINDO(A) AO CONTROLE FINANCEIRO PESSOAL - by Gleydson\n'
          'DEFINA UMA DAS OPÇÕES ABAIXO:')
    menu = Ajustes.valida_int('[1] GERIR COMPRAS - [2] GERIR SALARIO - [3] GERIR RENDIMENTO - [4] GERIR CATEGORIA: ',
                              'Digite um número inteiro',
                              'Devido as tentativas sem sucesso, o programa será encerrado...', 2)
    match menu:
        case 0:
            break
        case 1:
            while True:
                Ajustes.limpa_tela(0)
                print('Nesta seção temos as opções para lidar com compras')
                escolha = Ajustes.valida_int('O que você deseja?\n'
                                             '[1] INSERIR COMPRA - [2] - ALTERAR COMPRA - [3] - DELETAR COMPRA - [4] - MENU ANTERIOR: ',
                                             'Digite um valor válido.', 10)
                if escolha == 1:
                    while True:
                        if contador > 0:
                            c = Funcao.continuar(contador, 'inserir nova compra?')
                            if c == 0:
                                contador = 0
                                break
                        print('Certo, primeiro determine o mês que irá conter a compra: ')
                        Ajustes.apresenta_mes()
                        mes = Funcao.escolher_mes()
                        if mes == 0:
                            break
                        else:
                            print(f'A compra será inserida no mês {meses[mes - 1]}')
                            ver_cat = bd.select_simples('id_cat', 'nome', 'categoria')
                            if len(ver_cat) > 0:
                                print('Escolha a categoria que a compra será inserida!')
                                for dado, tup in enumerate(ver_cat):
                                    if dado + 1 < len(ver_cat):
                                        print(f'Código: {ver_cat[dado]} --- {ver_cat[dado + 1]}.')
                                    else:
                                        break
                            escolha_cat = Ajustes.valida_int('Digite o código da categoria desejada: ', 'Opção inválida.',
                                                             'Tentativas encerradas, retornando ao menu anterior', 10)
                            if escolha_cat == 0:
                                break
                            elif escolha_cat > (len(ver_cat) / 2):
                                print('Opção não corresponde a nenhuma categoria.')
                                Ajustes.limpa_tela()
                            else:
                                tipo_compra = Ajustes.valida_int('A compra será parcelada[1] ou à vista[2]? ', 'Opção inválida',
                                                                 'Devido as tentativas sem sucesso, a opção retrocedeu', 10)
                                if tipo_compra == 0:
                                    break
                                elif tipo_compra == 1:
                                    limite = bd.select_composto(1, 'categoria', 'limite_gasto', 'id_cat', escolha_cat)
                                    limite_atual = limite[0]
                                    nome = bd.select_composto(1, 'categoria', 'nome', 'id_cat', escolha_cat)
                                    gasto_atual = categorias.somar_gasto_cat(mes, escolha_cat)
                                    if gasto_atual[0] is None:
                                        pass
                                    else:
                                        limite_atual = limite[0] - gasto_atual[0]
                                    valor = Ajustes.valida_float('Digite o valor da compra! R$: ', 'Digite um número real.')
                                    if valor > limite_atual:
                                        print(f'O limite mensal da categoria {nome[0]} é de R${limite[0]}.\n'
                                              f'A compra inserida ultrapassa esse valor...\n'
                                              f'Retornando ao menu inicial de compras.')
                                        Ajustes.limpa_tela()
                                        break
                                    else:
                                        parcela = Ajustes.valida_int('Digite a quantidade de parcelas ', 'Digite um número inteiro', '')
                                        total_valor = valor * parcela
                                        compras.adicionar_compra_p(total_valor, parcela)
                                        id_ultimo = bd.select_ultimo('id_compra', 'total_compra')
                                        for compra in range(parcela):
                                            if verificador == 0:
                                                compras.adicionar_valor(valor, mes, escolha_cat, an, id_ultimo[0])
                                                verificador += 1
                                                mes += verificador
                                            else:
                                                if mes <= 12:
                                                    compras.adicionar_valor(valor, mes, escolha_cat, an, id_ultimo[0])
                                                    mes += verificador
                                                else:
                                                    mes, verificador = 1, 1
                                                    an += 1
                                                    compras.adicionar_valor(valor, mes, escolha_cat, an, id_ultimo[0])
                                                    mes += verificador
                                        an = int(ano.year)
                                        verificador = 0
                                        print('Valores inseridos com sucesso!')
                                        Ajustes.limpa_tela()
                                        contador += 1
                                elif tipo_compra == 2:
                                    limite = bd.select_composto(1, 'categoria', 'limite_gasto', 'id_cat', escolha_cat)
                                    limite_atual = limite[0]
                                    nome = bd.select_composto(1, 'categoria', 'nome', 'id_cat', escolha_cat)
                                    gasto_atual = categorias.somar_gasto_cat(mes, escolha_cat)
                                    if gasto_atual[0] is None:
                                        pass
                                    else:
                                        limite_atual = limite[0] - gasto_atual[0]
                                    valor = Ajustes.valida_float('Digite o valor da compra! R$: ', 'Digite um número real.')
                                    if valor > limite_atual:
                                        print(f'O limite mensal da categoria {nome[0]} é de R${limite[0]}.\n'
                                              f'A compra inserida ultrapassa esse valor...\n'
                                              f'Retornando ao menu inicial de compras.')
                                        Ajustes.limpa_tela()
                                        break
                                    else:
                                        compras.adicionar_valor(valor, mes, escolha_cat)
                                        Ajustes.limpa_tela()
                                        contador += 1
                elif escolha == 2:
                    while True:
                        if contador > 0:
                            c = Funcao.continuar(contador, 'alterar outra compra?')
                            if c == 0:
                                contador = 0
                                break
                        else:
                            Ajustes.limpa_tela(0)
                            print('Perfeito, para isso agora defina o mês da compra a ser ajustada')
                            Ajustes.apresenta_mes()
                            mes = Funcao.escolher_mes()
                            if mes == 0:
                                break
                            else:
                                tabela = Funcao.apresentar_compras(bd.conectar(), mes, an)
                                print('Observação: As alterações são feitas apenas dentro do ano vigente. Se precisar mudar mais que isso'
                                      ', por favor, delete a compra e a insira novamente!')
                                if tabela == 0:
                                    Ajustes.limpa_tela(4)
                                    break
                                else:
                                    escolher_alt = Funcao.escolher_compra_edit(bd.conectar(),
                                                                               'Digite o ID que aparece na frente da compra que deseja mudar: ',
                                                                               tabela)
                                    if escolher_alt == 'n':
                                        Ajustes.limpa_tela()
                                        break
                                    else:
                                        novo_valor = Ajustes.valida_float(f'Digite o valor novo para a compra ID({escolher_alt}) R$:', 'Digite um valor válido.')
                                        id_gasto_t = bd.select_composto(1, 'valor', 'compra_total', 'id_valor', escolher_alt)
                                        if id_gasto_t[0] is None:
                                            compras.alterar_valor(novo_valor, escolher_alt)
                                        else:
                                            parcelas = bd.select_composto(1, 'total_compra', 't_parcela', 'id_compra', id_gasto_t[0])
                                            compras.alterar_valor(novo_valor, escolher_alt, id_gasto_t[0], novo_valor * parcelas[0])
                                            contador += 1
                                            Ajustes.limpa_tela(4)
        case 3:
            print('a')
        case 4:
            print('Voltando ao menu inicial.')
            Ajustes.limpa_tela()
            break