import datetime
import mysql.connector

data = datetime.datetime.now()
ano = data.date()


class Conector:
    def __init__(self, host, user, pword, bd):
        self.host = host
        self.user = user
        self.pasw = pword
        self.bd = bd
        self.conexao = mysql.connector.connect(host=self.host, database=self.bd, user=self.user, password=self.pasw, buffered=True)
        self.cursor = self.conexao.cursor()

    def conectar(self):
        return self.conexao

    def desconectar(self):
        self.conexao.close()

    def select_ultimo(self, nome_id, tabela):
        if self.conexao.is_connected():
            sql = f'SELECT MAX({nome_id}) FROM {tabela}'
            self.cursor.execute(sql)
            for c1 in self.cursor:
                return c1

    def somar_gasto_compra(self, mes):
        if self.conexao.is_connected():
            sql = f'SELECT SUM(registro) FROM valor WHERE mes = {mes} AND ano = {ano.year}'
            self.cursor.execute(sql)
        for c1 in self.cursor:
            return c1

    def select_simples(self, coluna1, coluna2, tabela):
        if self.conexao.is_connected():
            sql = f"SELECT {coluna1}, {coluna2} FROM {tabela};"
            retorno = []
            self.cursor.execute(sql)
            for c1, c2 in self.cursor:
                retorno.append(c1)
                retorno.append(c2)
            return retorno
        else:
            print('Sem conexão com o servidor.')

    def select_simples_1col(self, tabela, coluna):
        if self.conexao.is_connected():
            sql = f"SELECT {coluna} FROM {tabela};"
            retorno = []
            self.cursor.execute(sql)
            for c1 in self.cursor:
                retorno.append(c1)
            return retorno
        else:
            print('Sem conexão com o servidor.')

    def select_composto(self, total_colunas, tabela, coluna1, colunap, pesquisa, *demais_colunas):
        if self.conexao.is_connected():
            match total_colunas:
                case 0:
                    sql = f'SELECT {coluna1} FROM {tabela} WHERE {colunap} = "{pesquisa}"'
                    self.cursor.execute(sql)
                    for c1 in self.cursor:
                        return c1
                case 1:
                    sql = f"SELECT {coluna1} FROM {tabela} WHERE {colunap} = {pesquisa}"
                    self.cursor.execute(sql)
                    for c1 in self.cursor:
                        return c1
                case 2:
                    sql = f"SELECT {coluna1}, {demais_colunas[0]} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    retorno = []
                    for c1, c2 in self.cursor:
                        retorno.append(c1)
                        retorno.append(c2)
                    return retorno
                case 3:
                    sql = \
                        f"SELECT {coluna1}, {demais_colunas[0]}, {demais_colunas[1]} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    retorno = []
                    for c1, c2, c3 in self.cursor:
                        retorno.append(c1)
                        retorno.append(c2)
                        retorno.append(c3)
                    return retorno
                case 4:
                    sql = \
                        f"SELECT {coluna1}, {demais_colunas[0]}, {demais_colunas[1]}, {demais_colunas[2]} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    retorno = []
                    for c1, c2, c3, c4 in self.cursor:
                        retorno.append(c1)
                        retorno.append(c2)
                        retorno.append(c3)
                        retorno.append(c4)
                    return retorno
                case 5:
                    sql = \
                        f"SELECT * FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    retorno = []
                    for c1, c2, c3, c4, c5 in self.cursor:
                        retorno.append(c1)
                        retorno.append(c2)
                        retorno.append(c3)
                        retorno.append(c4)
                        retorno.append(c5)
                    return retorno
        else:
            print('Sem conexão com servidor.')


class Categoria:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()

    def inserir_categoria(self, nome, limite, minimo=0):
        if self.conexao.is_connected():
            if minimo != 0:
                sql = 'INSERT INTO categoria (nome, limite_gasto, minimo_gasto) VALUES ("{}", "{}", "{}")'.format(nome, limite, minimo)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f"Categoria {nome} adicionada com sucesso!")
            else:
                sql = 'INSERT INTO categoria (nome, limite_gasto) VALUES ("{}", "{}")'.format(nome, limite)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f"Categoria {nome} adicionada com sucesso!")
        else:
            print('Sem conexão com o servidor.')

    def alterar_categoria(self, id_cat, nome='', limite='', minimo=''):
        if self.conexao.is_connected():
            if nome != '' and limite == '' and minimo == '':
                sql = 'UPDATE categoria SET nome = "{}" WHERE id_cat = "{}"'.format(nome, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Novo nome da categoria definido como {nome}!')
            elif nome != '' and limite != '' and minimo == '':
                sql = 'UPDATE categoria SET nome = "{}", limite_gasto = "{}" WHERE id_cat = "{}"'.format(nome, limite, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Alterado nome e limite para: {nome} e {limite}!')
            elif nome != '' and limite != '' and minimo != '':
                sql = 'UPDATE categoria SET nome = "{}", limite_gasto = "{}", minimo_gasto = "{}" WHERE id_cat = "{}"'.format(nome, limite, minimo, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Alterado nome, limite e minimo gasto para: {nome}, R${limite} e R${minimo}!')
            elif nome == '' and limite != '' and minimo == '':
                sql = 'UPDATE categoria SET limite_gasto = "{}" WHERE id_cat = "{}"'.format(limite, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Novo limite definido para R${limite}!')
            elif nome == '' and limite != '' and minimo != '':
                sql = 'UPDATE categoria SET limite_gasto = "{}", minimo_gasto = "{}" WHERE id_cat = "{}"'.format(limite, minimo, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Novo limite definido para R${limite} e mínimo de R${minimo}!')
            elif nome == '' and limite == '' and minimo != '':
                sql = 'UPDATE categoria SET minimo_gasto = "{}" WHERE id_cat = "{}"'.format(minimo, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Novo valor mínimo definido para R${minimo}!')
            elif nome != '' and limite == '' and minimo != '':
                sql = 'UPDATE categoria SET nome = "{}", minimo_gasto = "{}" WHERE id_cat = "{}"'.format(nome, minimo, id_cat)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Nome alterado para {nome} e com novo valor mínimo de R${minimo}!')
            else:
                print('Opção inválida.')

    def somar_gasto_cat(self, mes, categoria):
        if self.conexao.is_connected():
            sql = f"SELECT SUM(registro) FROM valor WHERE mes = {mes} AND categoria = {categoria} AND ano = {ano.year};"
            self.cursor.execute(sql)
            for c1 in self.cursor:
                return c1


class Compra:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()

    def adicionar_valor(self, valor, mes, categoria, an=ano.year, nome_compra='', total_compra=0):
        if self.conexao.is_connected():
            if total_compra != 0 and nome_compra != '':
                sql = 'INSERT INTO valor (registro, mes, compra_total, categoria, ano, nome_compra) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'\
                    .format(valor, mes, total_compra, categoria, an, nome_compra)
                self.cursor.execute(sql)
                self.conexao.commit()
            elif total_compra != 0 and nome_compra == '':
                sql = 'INSERT INTO valor (registro, mes, compra_total, categoria, ano) VALUES ("{}", "{}", "{}", "{}", "{}")' \
                    .format(valor, mes, total_compra, categoria, an)
                self.cursor.execute(sql)
                self.conexao.commit()
            elif total_compra == 0 and nome_compra != '':
                sql = 'INSERT INTO valor (registro, mes, categoria, ano, nome_compra) VALUES ("{}", "{}", "{}", "{}", "{}")' \
                    .format(valor, mes, categoria, an, nome_compra)
                self.cursor.execute(sql)
                self.conexao.commit()
            else:
                sql = 'INSERT INTO valor (registro, mes, categoria, ano) VALUES ("{}", "{}", "{}", "{}")' \
                    .format(valor, mes, categoria, an)
                self.cursor.execute(sql)
                self.conexao.commit()
        else:
            print('Sem conexão com o servidor.')

    def alterar_valor(self, novo_valor, id_valor, total_compra=0, novo_valorc=0):
        if self.conexao.is_connected():
            if total_compra == 0:
                sql = 'UPDATE valor SET registro = "{}" WHERE id_valor = "{}"'.format(novo_valor, id_valor)
                self.cursor.execute(sql)
                self.conexao.commit()
                print(f'Novo valor para a compra ID {id_valor} alterado para R${novo_valor:.2f}.')
            else:
                sql = 'UPDATE valor SET registro = "{}" WHERE compra_total = "{}";'.format(novo_valor, total_compra)
                sql2 = 'UPDATE total_compra SET compra = "{}" WHERE id_compra = "{}"'.format(novo_valorc, total_compra)
                self.cursor.execute(sql)
                self.conexao.commit()
                self.cursor.execute(sql2)
                self.conexao.commit()
                print(f'Valor alterado para todas as parcelas vinculadas, sendo R${novo_valor:.2f} '
                      f'para cada uma e o total da compra é de R${novo_valorc:.2f}.')
        else:
            print('Sem conexão com servidor.')

    def deletar_valor(self, id_valor):
        if self.conexao.is_connected():
            sql = f'DELETE FROM valor WHERE id_valor = {id_valor}'
            self.cursor.execute(sql)
            self.conexao.commit()
            print(f'Valor de id {id_valor} removido com sucesso.')

    def adicionar_compra_p(self, total_compra, parcelas):
        if self.conexao.is_connected():
            sql = 'INSERT INTO total_compra (compra, t_parcela) VALUES ("{}", "{}")' \
                .format(total_compra, parcelas)
            self.cursor.execute(sql)
            self.conexao.commit()
        else:
            print('Sem conexão com o servidor.')

    def remover_compra_p(self, id_compra):
        if self.conexao.is_connected():
            sql = f'DELETE FROM valor WHERE compra_total = {id_compra}'
            sql2 = f'DELETE FROM total_compra WHERE id_compra = {id_compra}'
            self.cursor.execute(sql)
            self.conexao.commit()
            self.cursor.execute(sql2)
            self.conexao.commit()
            print('Compra removida de todos os meses atrelados.')
        else:
            print('Erro no servidor.')

    def antecipar_compra_p(self, id_compra, mes_atual, ano_atual):
        if self.conexao.is_connected():
            sql = f'SELECT V.registro, T.compra, V.mes, V.ano, V.nome_compra, C.nome FROM valor V INNER JOIN total_compra T ON V.compra_total = T.id_compra' \
                  f'INNER JOIN categoria C ON V.categoria = C.id_cat WHERE V.compra_total = {id_compra}'
            registros = []
            self.cursor.execute(sql)
            for c1, c2, c3, c4, c5, c6 in self.cursor:
                registros.append(c1)
                registros.append(c2)
                registros.append(c3)
                registros.append(c4)
                registros.append(c5)
                registros.append(c6)
            teste, teste1 = 0, 0
            for epoca in registros[3]:
                if epoca == 1:
                    teste = registros[3][epoca - 1]
                else:
                    if teste <= registros[3][epoca - 1]:
                        pass
                    else:
                        teste = registros[3][epoca - 1]
            for mes in registros[2]:
                if registros[3][mes - 1] == teste:
                    teste1 = registros[2][mes - 1]
                    for p_mes in registros[2]:
                        if teste1 <= registros[2][p_mes - 1]:
                            pass
                        else:
                            teste1 = registros[2][p_mes - 1]
                    break
                else:
                    pass
            conta = ((ano_atual - teste) * 12) + (mes_atual - teste1)
            if conta == 0:
                self.remover_compra_p(id_compra)
            else:
                self.remover_compra_p(id_compra)
                self.adicionar_compra_p(registros[0][0] * conta, conta)

        else:
            print('Erro no servidor.')

    def somar_gasto(self, mes):
        if self.conexao.is_connected():
            sql = f"SELECT SUM(registro) FROM valor WHERE mes = {mes};"
            self.cursor.execute(sql)
            for c1 in self.cursor:
                return c1
        else:
            print('Sem conexão com servidor.')


class SalarioRendimento:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()

    def inserir_salario(self, salario, mes, an=ano.year):
        if self.conexao.is_connected():
            sql = 'INSERT INTO salario (pagamento, mes, ano) VALUES ("{}", "{}", "{}")'.format(salario, mes, an)
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Salario inserido com sucesso!')
        else:
            print('Sem conexão com o servidor.')

    def alterar_salario(self, salario, id_sal):
        if self.conexao.is_connected():
            sql = 'UPDATE salario SET pagamento = "{}" WHERE id_sal = "{}"'.format(salario, id_sal)
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Salário alterado com sucesso!')
        else:
            print('Sem conexão com servidor.')

    def deletar_salario(self, id_sal):
        if self.conexao.is_connected():
            sql = f'DELETE FROM salario WHERE id_sal = {id_sal}'
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Salário deletado com sucesso!')
        else:
            print('Sem conexão com servidor.')

    def inserir_rendimento(self, rendimento, mes, an=ano.year):
        if self.conexao.is_connected():
            sql = 'INSERT INTO rendimento (valor, mes, ano) VALUES ("{}", "{}", "{}")'.format(rendimento, mes, an)
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Rendimento (valor extra) inserido com sucesso!')
        else:
            print('Sem conexão com o servidor.')

    def alterar_rendimento(self, rendimento, id_red):
        if self.conexao.is_connected():
            sql = 'UPDATE salario SET valor = "{}" WHERE id_red = "{}"'.format(rendimento, id_red)
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Rendimento (valor extra) alterado com sucesso!')
        else:
            print('Sem conexão com servidor.')

    def deletar_rendimento(self, id_red):
        if self.conexao.is_connected():
            sql = f'DELETE FROM rendimento WHERE id_red = {id_red}'
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Rendimento (valor extra) deletado com sucesso!')
        else:
            print('Sem conexão com servidor.')