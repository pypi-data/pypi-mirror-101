import pandas as pd
from abc import abstractmethod

informacoes_classe = {'Classe': ('C20', 'C30', 'C40', 'C60'),
                      'Fc0k': (20, 30, 40, 60),
                      'Ec0m': (9500, 14500, 19500, 24500)}
tabela_classe = pd.DataFrame(informacoes_classe, index=(1, 2, 3, 4))

informacoes_kmod1 = {'Permanente': 0.6,
                     'Longa Duração': 0.7,
                     'Média Duração': 0.8,
                     'Curta Duração': 0.9,
                     'Instantânea': 1.1}

duracoes = ('Permanente', 'Longa Duração', 'Média Duração', 'Curta Duração', 'Instantânea')

informacoes_kmod2 = {'1': 1,
                     '2': 1,
                     '3': 0.8,
                     '4': 0.8}

informacoes_kmod3 = {'1ª Categoria': 1, '2ª Categoria': 0.8}

categorias = ('1ª Categoria', '2ª Categoria')


class Pegador:

    @staticmethod
    @abstractmethod
    def pega_dimensoes(elemento):
        pass

    @staticmethod
    @abstractmethod
    def pega_comprimento():
        pass

    @staticmethod
    @abstractmethod
    def pega_cargas():
        pass

    @staticmethod
    def escolhe_tipo_elemento():

        mensagem = f'''O elemento é retangular ou circular?

                        (1) Circular
                        (2) Retangular

                    '''

        circulo_ou_retangulo = input(mensagem)
        if circulo_ou_retangulo in ('1', '2'):
            return circulo_ou_retangulo
        else:
            raise ValueError('Digite um valor válido.')

    @staticmethod
    def pega_classe_categoria_e_duracao():
        mensagem_classe = '''Informe a classe da madeira. 

                (1) C20
                (2) C30
                (3) C40
                (4) C60

                '''

        mensagem_categoria = '''Informe a categoria da madeira.

                (1) 1ª categoria
                (2) 2ª categoria

                '''

        mensagem_duracao = '''Informe a duração do carregamento.

                (1) Permanente
                (2) Longa Duração
                (3) Média Duração
                (4) Curta Duração
                (5) Instantânea

                '''

        classe = int(input(mensagem_classe))
        if classe not in (1, 2, 3, 4):
            raise ValueError('Digite um valor válido para classe. ')

        categoria = int(input(mensagem_categoria))
        if categoria not in (1, 2):
            raise ValueError('Digite um valor válido para categoria. ')

        duracao = int(input(mensagem_duracao))
        if duracao not in (1, 2, 3, 4, 5):
            raise ValueError('Digite um valor válido para duração. ')

        return classe, categoria, duracao

    @staticmethod
    def pega_classe_umidade():
        umidade = int(input('Informe a umidade ambiente. '))

        if umidade <= 65:
            classe_umidade = '1'
        elif 65 < umidade <= 75:
            classe_umidade = '2'
        elif 75 < umidade <= 85:
            classe_umidade = '3'
        else:
            classe_umidade = '4'

        return classe_umidade

    @staticmethod
    def pega_Fc0k(viga):
        fc0k = tabela_classe.loc[viga.classe, 'Fc0k']
        return fc0k

    @staticmethod
    def pega_kmod(viga):
        duracao = duracoes[viga.duracao - 1]
        kmod1 = informacoes_kmod1[duracao]

        kmod2 = informacoes_kmod2[viga.classe_umidade]

        categoria = categorias[viga.categoria - 1]
        kmod3 = informacoes_kmod3[categoria]

        kmod = kmod1 * kmod2 * kmod3

        return round(kmod, 3), (kmod1, kmod2, kmod3)


class PegadorViga(Pegador):

    @staticmethod
    def pega_dimensoes(viga):
        if viga.circulo_ou_retangulo == '1':
            diametro = float(input('Informe o diâmetro em centímetro da peça. '))
            return diametro / 100
        else:
            base = float(input('Informe a medida da base em centímetro da peça. '))
            altura = float(input('Informe a medida da altura em centímetro da peça. '))
            return base / 100, altura / 100

    @staticmethod
    def pega_comprimento():
        comprimento = float(input('Informe o comprimento em metro da viga. '))
        return comprimento

    @staticmethod
    def pega_cargas():
        peso_proprio = float(input('Informe o peso próprio da viga. '))
        carga_acidental = float(input('Informe a carga acidental da viga. '))

        return peso_proprio, carga_acidental

    @staticmethod
    def pega_Ec0m(viga):
        Ec0m = tabela_classe.loc[viga.classe, 'Ec0m']
        return Ec0m


class PegadorPilar(Pegador):

    @staticmethod
    def pega_dimensoes(pilar):
        if pilar.circulo_ou_retangulo == '1':
            diametro = float(input('Informe o diâmetro em centímetro da peça. '))
            return diametro
        else:
            base = float(input('Informe a medida da base em centímetro da peça. '))
            altura = float(input('Informe a medida da altura em centímetro da peça. '))
            return base, altura

    @staticmethod
    def pega_comprimento():
        comprimento = float(input('Informe a altura em metro do pilar. '))
        return comprimento * 100

    @staticmethod
    def pega_cargas():
        flexao_composta = float(input('Informe o esforço de Flexão Composta (Nd) do pilar. '))
        momento_z = float(input('Informe o Momento Fletor no eixo Z (Mzd) do pilar. '))
        momento_y = float(input('Informe o Momento Fletor no eixo Y (Myd) do pilar. '))

        return flexao_composta, momento_z, momento_y

