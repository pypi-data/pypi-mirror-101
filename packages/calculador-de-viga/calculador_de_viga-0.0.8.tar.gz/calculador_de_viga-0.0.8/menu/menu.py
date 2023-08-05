from elementos_estruturais import *


class MenuPrincipal:

    def __init__(self):
        print('\n\nBem vindo ao Calculador de Estruturas do 4º TE. A seguir, um pequeno tutorial de uso.\n\n')
        print('Não é necessário digitar as unidades dos valores, apenas o número é necessário.')
        print('Caso a unidade seja digitada, erros ocorrerão.')
        print('Quando aparecer um seletor, por exemplo: \n (1) Opção 1 \n (2) Opção 2')
        print('Digite somente o número que está dentro dos parênteses. Por exemplo, se sua a opção desejada for a 2,')
        print('digite apenas "2" (sem as aspas).\n\n')

        mensagem = '''Qual elemento estrutural irá ser calculado?
        
            (1) Pilar
            (2) Viga
            
            '''

        elemento = int(input(mensagem))

        if elemento == 1:
            PilarDeMadeira()
        elif elemento == 2:
            VigaDeMadeira()
        else:
            raise Exception('Digite um valor válido.')


if __name__ == '__main__':
    MenuPrincipal()
