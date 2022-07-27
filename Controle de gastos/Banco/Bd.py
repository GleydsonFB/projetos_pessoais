import mysql.connector


class Conector:
    def __init__(self, host, user, pword, bd):
        self.host = host
        self.user = user
        self.pasw = pword
        self.bd = bd
        self.conexao = mysql.connector.connect(host=self.host, database=self.bd, user=self.user, password=self.pasw)
        self.cursor = self.conexao.cursor()

    def conectar(self):
        return self.conexao

    def desconectar(self):
        self.conexao.close()
        if self.conexao.is_connected():
            print('Desconexão falhou')
        else:
            print('Desconectado do banco')

    def select_simples(self, coluna1, coluna2, tabela):
        if self.conexao.is_connected():
            sql = f"SELECT {coluna1}, {coluna2} FROM {tabela};"
            self.cursor.execute(sql)
            for c1, c2 in self.cursor:
                return c1, c2
        else:
            print('Sem conexão com o servidor')

    def select_composto(self, total_colunas, tabela, coluna1, coluna2, colunap, pesquisa, *demais_colunas):
        if self.conexao.is_connected():
            match total_colunas:
                case 1:
                    sql = f"SELECT {coluna1} FROM {tabela} WHERE {colunap} = {pesquisa}"
                    self.cursor.execute(sql)
                    for c1 in self.cursor:
                        return c1
                case 2:
                    sql = f"SELECT {coluna1}, {coluna2} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    for c1, c2 in self.cursor:
                        return c1, c2
                case 3:
                    sql = \
                        f"SELECT {coluna1}, {coluna2}, {demais_colunas[0]} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    for c1, c2, c3 in self.cursor:
                        return c1, c2, c3
                case 4:
                    sql = \
                        f"SELECT {coluna1}, {coluna2}, {demais_colunas[0]}, {demais_colunas[1]} FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    for c1, c2, c3, c4 in self.cursor:
                        return c1, c2, c3, c4
                case 5:
                    sql = \
                        f"SELECT * FROM {tabela} WHERE {colunap} = {pesquisa};"
                    self.cursor.execute(sql)
                    for c1, c2, c3, c4, c5 in self.cursor:
                        return c1, c2, c3, c4, c5
        else:
            print('Sem conexão com servidor')

    def somar_gasto(self, mes):
        if self.conexao.is_connected():
            sql = f"SELECT SUM(registro) FROM valor WHERE mes = {mes};"
            self.cursor.execute(sql)
            for c1 in self.cursor:
                return c1
        else:
            print('Sem conexão com servidor')


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
            print('Sem conexão com o servidor')

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
                print('Opção inválida')

    #def deletar_categoria(self):

    def somar_gasto_cat(self, mes, categoria):
        if self.conexao.is_connected():
            sql = f"SELECT SUM({categoria}) FROM valor WHERE mes = {mes};"
            self.cursor.execute(sql)
            for c1 in self.cursor:
                return c1


class Compra:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = self.conexao.cursor()

    def adicionar_valor(self, valor, mes, categoria, total_compra=''):
        if self.conexao.is_connected():
            if total_compra != '':
                sql = 'INSERT INTO valor (registro, mes, compra_total, categoria) VALUES ({}, {}, {}, {})' \
                    .format(valor, mes, total_compra, categoria)
                self.cursor.execute(sql)
                self.conexao.commit()
                print('Valor inserido com sucesso!')
            else:
                sql = 'INSERT INTO valor (registro, mes, categoria) VALUES ({}, {}, {})' \
                    .format(valor, mes, categoria)
                self.cursor.execute(sql)
                self.conexao.commit()
                print('Valor inserido com sucesso!')
        else:
            print('Sem conexão com o servidor')

    def adicionar_compra_p(self, total_compra, parcelas):
        if self.conexao.is_connected():
            sql = 'INSERT INTO total_compra (compra, t_parcela) VALUES ("{}", "{}")' \
                .format(total_compra, parcelas)
            self.cursor.execute(sql)
            self.conexao.commit()
            print('Valor inserido com sucesso!')
        else:
            print('Sem conexão com o servidor')

    def remover_compra_p(self, id_compra):
        if self.conexao.is_connected():
            sql = f'DELETE FROM valor WHERE compra_total = {id_compra}'
            sql2 = f'DELETE FROM total_compra WHERE id_compra = {id_compra}'
            self.cursor.execute(sql)
            self.conexao.commit()
            self.cursor.execute(sql2)
            self.conexao.commit()
            print('Compra retirada com sucesso')
        else:
            print('Erro no servidor')