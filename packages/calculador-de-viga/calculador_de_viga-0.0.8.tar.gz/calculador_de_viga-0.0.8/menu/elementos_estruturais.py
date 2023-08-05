from pegador import *
from calculador import *

class VigaDeMadeira:

    def __init__(self):
        self.circulo_ou_retangulo = PegadorViga.escolhe_tipo_elemento()
        self.dimensoes = PegadorViga.pega_dimensoes(self)
        self.comprimento = PegadorViga.pega_comprimento()
        self.peso_proprio, self.carga_acidental = PegadorViga.pega_cargas()
        self.classe, self.categoria, self.duracao = PegadorViga.pega_classe_categoria_e_duracao()
        self.classe_umidade = PegadorViga.pega_classe_umidade()
        self.Fc0k = PegadorViga.pega_Fc0k(self)
        self.kmod, self.kmods = PegadorViga.pega_kmod(self)
        self.Ec0m = PegadorViga.pega_Ec0m(self)

        self.area = CalculadorViga.calcula_area(self)
        self.inercia = CalculadorViga.calcula_inercia(self)
        self.modulo_resistencia = CalculadorViga.calcula_resistencia(self)
        self.carga_permanente = CalculadorViga.calcula_carga_permanente(self)
        self.momento_fletor = CalculadorViga.calcula_momento_fletor(self)
        self.tensao_normal = CalculadorViga.calcula_tensao_normal(self)
        self.fc0d = CalculadorViga.calcula_fc0d(self)
        self.flecha_maxima = CalculadorViga.calcula_flecha_maxima(self)
        self.modulo_elasticidade = CalculadorViga.calcula_modulo_elasticidade(self)
        self.flecha_efetiva = CalculadorViga.calcula_flecha_efetiva(self)

        print(self)

    def compara_estado_limite_ultimo(self):
        if self.tensao_normal <= self.fc0d:
            return 'Passou!'
        else:
            return 'Não passou!'

    def compara_flecha(self):
        if self.flecha_efetiva <= self.flecha_maxima:
            return 'Passou!'
        else:
            return 'Não passou!'

    def __str__(self):
        return f'''

Área (A): {round(self.area, 3)} m²
Momento de Inércia (Iz): {round(self.inercia, 3)} m⁴
Módulo de Resistência (W): {round(self.modulo_resistencia, 3)} m³
Carga Permanente (gk): {round(self.carga_permanente, 3)} kN/m
Momento Fletor Máximo (Mzd): {round(self.momento_fletor, 3)} kNm
Tensão Máxima (σMzd): {round(self.tensao_normal, 3)} MPa
Resistência a Compressão (Fc0k): {self.Fc0k} MPa
Kmod1, Kmod2, Kmod3: {self.kmods}
Kmod: {self.kmod}
Resistência da Madeira (Fc0d): {self.fc0d} MPa

Verificação Parte 3: {round(self.tensao_normal, 3)} <= {self.fc0d}
        {self.compara_estado_limite_ultimo()}

Flecha Limite (Vlim): {self.flecha_maxima} mm
Ec0m: {self.Ec0m} MPa
Modulo de Elasticidade Efetivo (Eef): {self.modulo_elasticidade} kN/m²
Flecha Efetiva (Vef): {round(self.flecha_efetiva, 3)} mm

Verificação Parte 4: {round(self.flecha_efetiva, 3)} <= {self.flecha_maxima}
        {self.compara_flecha()}


'''


class PilarDeMadeira:

    def __init__(self):
        self.circulo_ou_retangulo = PegadorPilar.escolhe_tipo_elemento()
        self.dimensoes = PegadorPilar.pega_dimensoes(self)
        self.comprimento = PegadorPilar.pega_comprimento()
        self.flexao_composta, self.momento_z, self.momento_y = PegadorPilar.pega_cargas()
        self.classe, self.categoria, self.duracao = PegadorPilar.pega_classe_categoria_e_duracao()
        self.classe_umidade = PegadorPilar.pega_classe_umidade()
        self.Fc0k = PegadorPilar.pega_Fc0k(self)
        self.kmod, self.kmods = PegadorPilar.pega_kmod(self)

        self.area = CalculadorPilar.calcula_area(self)
        self.inercia = CalculadorPilar.calcula_inercia(self)
        self.modulo_resistencia = CalculadorPilar.calcula_resistencia(self)
        self.raio_giracao = CalculadorPilar.calcula_raio_giracao(self)
        self.indice_esbeltez = CalculadorPilar.calcula_indice_esbeltez(self)
        self.fc0d = CalculadorPilar.calcula_fc0d(self)
        self.tensao_normal = CalculadorPilar.calcula_tensao_normal(self)
        self.tensao_momento_fletor = CalculadorPilar.calcula_tensao_momento_fletor(self)

        print(self)

    def verificacao_parte_1(self):
        verificacao = ((self.tensao_normal/self.fc0d)**2 +
                       self.tensao_momento_fletor[1]/self.fc0d +
                       0.5 * (self.tensao_momento_fletor[0]/self.fc0d))
        if verificacao < 1:
            return 'Passou!', verificacao
        else:
            return 'Não passou!', verificacao

    def verificacao_parte_2(self):
        verificacao = ((self.tensao_normal/self.fc0d)**2 +
                       0.5 * (self.tensao_momento_fletor[1]/self.fc0d) +
                       self.tensao_momento_fletor[0]/self.fc0d)
        if verificacao < 1:
            return 'Passou!', verificacao
        else:
            return 'Não passou!', verificacao

    def __str__(self):
        return f'''

Área (A): {round(self.area, 3)} cm²
Momento de Inércia em z (Iz): {round(self.inercia[0],3 )} cm⁴
Momento de Inércia em y (Iy): {round(self.inercia[1], 3)} cm⁴
Módulo de Resistência em z (Wz): {round(self.modulo_resistencia[0], 3)} cm³
Módulo de Resistência em y (Wy): {round(self.modulo_resistencia[1], 3)} cm³
Raio de Giração em z (iz): {round(self.raio_giracao[0], 3)} cm
Raio de Giração em y (iy): {round(self.raio_giracao[1], 3)} cm
Índice de Esbeltez em z (λz): {round(self.indice_esbeltez[0], 3)}
Índice de Esbeltez em y (λy): {round(self.indice_esbeltez[1], 3)}
Resistência a Compressão (Fc0k): {self.Fc0k} MPa
Kmod1, Kmod2, Kmod3: {self.kmods}
Kmod: {self.kmod}
Resistência da Madeira (Fc0d): {self.fc0d} MPa
Tensão Normal (σNd): {round(self.tensao_normal, 3)} MPa
Tensão Momento Fletor em z (σMz): {round(self.tensao_momento_fletor[0], 3)} MPa
Tensão Momento Fletor em y (σMy): {round(self.tensao_momento_fletor[1], 3)} MPa

Verificação Parte 3.1: {round(self.verificacao_parte_1()[1], 3)} < 1
        {self.verificacao_parte_1()[0]}

Verificação Parte 3.2: {round(self.verificacao_parte_2()[1], 3)} < 1
        {self.verificacao_parte_2()[0]}


'''

