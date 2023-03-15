from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

lista_cidades = [
    ['BAMBUI', 5.25, 5.76, 5.1, 5.5, 5.32, 5.29, 5.55, 6.38, 5.8, 5.4, 4.79, 5.06],
    ['BELO HORIZONTE', 5.28, 5.71, 5.25, 5.3, 5.0, 5.11, 5.3, 5.97, 5.85, 5.52, 4.94, 5.08],
    ['BELO VALE', 5.31, 5.68, 5.22, 5.32, 5.04, 5.04, 5.23, 5.95, 5.69, 5.4, 4.88, 5.07],
    ['BETIM', 5.28, 5.73, 5.26, 5.36, 5.09, 5.13, 5.38, 6.04, 5.84, 5.48, 4.89, 5.06],
    ['BOM DESPACHO', 5.34, 5.85, 5.29, 5.51, 5.34, 5.33, 5.61, 6.27, 5.85, 5.48, 4.97, 5.14],
    ['BOM SUCESSO', 5.0, 5.5, 4.98, 5.14, 4.77, 4.8, 5.02, 5.79, 5.48, 5.21, 4.76, 5.02],
    ['BONFIM', 5.26, 5.67, 5.17, 5.29, 5.05, 5.05, 5.25, 5.98, 5.69, 5.36, 4.85, 5.04],
    ['BRUMADINHO', 5.37, 5.7, 5.24, 5.32, 5.07, 5.09, 5.31, 6.02, 5.8, 5.46, 4.94, 5.1],
    ['CAETE', 5.1, 5.62, 5.16, 5.14, 4.89, 4.95, 5.11, 5.79, 5.61, 5.3, 4.71, 4.99],
    ['CAPIM BRANCO', 5.41, 5.86, 5.34, 5.46, 5.23, 5.17, 5.48, 6.13, 5.96, 5.53, 5.02, 5.11],
    ['CAPITOLIO', 5.08, 5.59, 4.96, 5.33, 5.12, 5.09, 5.35, 6.03, 5.57, 5.39, 4.78, 4.95],
    ['CARMO DA MATA', 5.16, 5.66, 5.12, 5.37, 5.02, 5.11, 5.3, 5.97, 5.67, 5.38, 4.8, 5.04],
    ['CARMO DO CAJURU', 5.33, 5.76, 5.19, 5.41, 5.12, 5.15, 5.37, 6.05, 5.74, 5.48, 4.91, 5.1],
    ['CARMO DO RIO CLARO', 5.16, 5.66, 5.06, 5.21, 4.89, 4.74, 5.06, 5.82, 5.39, 5.34, 4.96, 5.11],
    ['CARMOPOLIS DE MINAS', 5.17, 5.62, 5.17, 5.37, 5.04, 5.07, 5.34, 5.97, 5.68, 5.39, 4.85, 5.08],
    ['CARRANCAS', 5.1, 5.63, 5.08, 4.93, 4.54, 4.53, 4.68, 5.52, 5.28, 5.16, 4.8, 5.13],
    ['CLAUDIO', 5.18, 5.66, 5.14, 5.38, 5.03, 5.08, 5.29, 5.96, 5.69, 5.41, 4.85, 5.06],
    ['CONCEICAO DA APARECIDA', 4.96, 5.47, 4.87, 5.09, 4.83, 4.8, 5.13, 5.93, 5.43, 5.23, 4.77, 4.9],
    ['CONCEICAO DO PARA', 5.36, 5.78, 5.26, 5.48, 5.2, 5.25, 5.47, 6.16, 5.84, 5.45, 4.92, 5.11],
    ['CONSELHEIRO LAFAIETE', 5.04, 5.66, 5.04, 5.02, 4.68, 4.67, 4.77, 5.68, 5.37, 5.15, 4.64, 5.02],
    ['CONTAGEM', 5.27, 5.72, 5.27, 5.36, 5.03, 5.1, 5.32, 6.0, 5.87, 5.51, 4.9, 5.06],
    ['COROMANDEL', 5.13, 5.69, 5.23, 5.61, 5.65, 5.51, 5.9, 6.57, 5.94, 5.57, 5.03, 5.16],
    ['CRUCILANDIA', 5.16, 5.59, 5.11, 5.21, 5.01, 5.04, 5.31, 5.95, 5.67, 5.32, 4.76, 4.97],
    ['DESTERRO DE ENTRE RIOS', 5.15, 5.59, 5.09, 5.16, 4.82, 4.91, 5.06, 5.83, 5.54, 5.31, 4.73, 5.03],
    ['DIVINOPOLIS', 5.35, 5.76, 5.25, 5.48, 5.16, 5.19, 5.39, 6.11, 5.79, 5.45, 4.93, 5.09],
    ['DORES DE GUANHAES', 5.19, 5.63, 4.99, 4.81, 4.48, 4.46, 4.64, 5.21, 5.2, 4.96, 4.41, 4.91],
    ['ESMERALDAS', 5.37, 5.8, 5.28, 5.45, 5.17, 5.21, 5.42, 6.06, 5.86, 5.48, 4.95, 5.13],
    ['FLORESTAL', 5.34, 5.78, 5.23, 5.4, 5.16, 5.21, 5.43, 6.09, 5.81, 5.44, 4.91, 5.06],
    ['FORTUNA DE MINAS', 5.46, 5.84, 5.33, 5.47, 5.27, 5.23, 5.55, 6.19, 5.94, 5.49, 4.99, 5.16],
    ['GUAPE', 5.1, 5.66, 5.1, 5.45, 5.13, 5.08, 5.3, 5.96, 5.49, 5.41, 4.95, 5.11],
    ['IBIRITE', 5.16, 5.64, 5.19, 5.26, 5.04, 5.07, 5.32, 6.01, 5.86, 5.48, 4.86, 5.03],
    ['IBITURUNA', 5.12, 5.54, 5.11, 5.2, 4.79, 4.75, 4.96, 5.78, 5.44, 5.25, 4.8, 5.05],
    ['IGARAPE', 5.33, 5.72, 5.2, 5.29, 5.06, 5.13, 5.38, 6.06, 5.8, 5.45, 4.89, 5.01],
    ['IGARATINGA', 5.35, 5.77, 5.21, 5.42, 5.12, 5.22, 5.43, 6.1, 5.78, 5.42, 4.93, 5.08],
    ['ILICINEA', 5.01, 5.59, 5.05, 5.28, 5.03, 5.01, 5.25, 5.98, 5.51, 5.35, 4.85, 5.06],
    ['INHAUMA', 5.43, 5.84, 5.3, 5.47, 5.25, 5.23, 5.56, 6.17, 5.96, 5.51, 4.99, 5.13],
    ['ITAGUARA', 5.11, 5.54, 5.08, 5.22, 5.02, 5.07, 5.29, 6.0, 5.68, 5.3, 4.75, 4.97],
    ['ITAPECERICA', 5.27, 5.73, 5.17, 5.46, 5.12, 5.13, 5.39, 6.03, 5.74, 5.46, 4.84, 5.08],
    ['ITATIAIUCU', 5.22, 5.62, 5.1, 5.25, 5.05, 5.11, 5.34, 6.04, 5.76, 5.37, 4.82, 4.97],
    ['ITAU DE MINAS', 5.24, 5.7, 5.21, 5.43, 5.16, 5.16, 5.34, 6.04, 5.47, 5.48, 5.16, 5.21],
    ['ITAUNA', 5.24, 5.69, 5.14, 5.37, 5.05, 5.14, 5.38, 6.04, 5.76, 5.41, 4.87, 5.04],
    ['JABOTICATUBAS', 5.39, 5.8, 5.4, 5.42, 5.27, 5.19, 5.5, 6.11, 6.0, 5.6, 5.05, 5.18],
    ['JUATUBA', 5.38, 5.79, 5.29, 5.43, 5.14, 5.2, 5.39, 6.08, 5.81, 5.45, 4.91, 5.1],
    ['LAGOA DA PRATA', 5.36, 5.78, 5.27, 5.56, 5.29, 5.24, 5.49, 6.2, 5.83, 5.47, 4.91, 5.13],
    ['LAGOA SANTA', 5.35, 5.81, 5.39, 5.45, 5.22, 5.17, 5.45, 6.02, 5.91, 5.49, 5.03, 5.15],
    ['LAVRAS', 5.0, 5.5, 4.98, 5.14, 4.77, 4.8, 5.02, 5.79, 5.48, 5.21, 4.76, 5.02],
    ['MARAVILHAS', 5.41, 5.87, 5.34, 5.58, 5.38, 5.28, 5.64, 6.24, 5.97, 5.51, 4.98, 5.2],
    ['MARIO CAMPOS', 5.33, 5.65, 5.23, 5.31, 5.05, 5.08, 5.29, 6.03, 5.81, 5.45, 4.89, 5.12],
    ['MARTINHO CAMPOS', 5.42, 5.82, 5.31, 5.58, 5.42, 5.41, 5.64, 6.27, 5.92, 5.52, 4.95, 5.17],
    ['MATEUS LEME', 5.3, 5.74, 5.17, 5.36, 5.06, 5.15, 5.41, 6.07, 5.76, 5.41, 4.86, 4.99],
    ['MATOZINHOS', 5.36, 5.75, 5.32, 5.43, 5.2, 5.13, 5.46, 6.04, 5.92, 5.5, 5.0, 5.1],
    ['MOEMA', 5.37, 5.87, 5.26, 5.6, 5.35, 5.32, 5.47, 6.2, 5.84, 5.48, 4.98, 5.1],
    ['MORADA NOVA DE MINAS', 5.58, 6.04, 5.57, 5.78, 5.58, 5.42, 5.85, 6.26, 6.12, 5.77, 5.18, 5.33],
    ['MUZAMBINHO', 4.93, 5.35, 4.89, 5.16, 4.83, 4.77, 5.1, 5.88, 5.37, 5.25, 4.87, 4.94],
    ['NAZARENO', 5.1, 5.52, 5.07, 5.15, 4.73, 4.69, 4.88, 5.73, 5.43, 5.19, 4.74, 5.02],
    ['NEPOMUCENO', 5.16, 5.57, 5.1, 5.31, 4.91, 4.84, 5.1, 5.86, 5.48, 5.34, 4.9, 5.12],
    ['NOVA LIMA', 5.28, 5.7, 5.23, 5.29, 4.95, 5.08, 5.28, 5.91, 5.78, 5.45, 4.89, 5.08],
    ['NOVA SERRANA', 5.28, 5.75, 5.26, 5.43, 5.18, 5.17, 5.39, 6.09, 5.79, 5.46, 4.93, 5.08],
    ['NOVA UNIAO', 5.19, 5.71, 5.19, 5.14, 4.93, 4.98, 5.2, 5.85, 5.63, 5.35, 4.73, 4.98],
    ['OLIVEIRA', 5.13, 5.57, 5.08, 5.27, 4.98, 5.03, 5.27, 5.93, 5.61, 5.32, 4.78, 5.04],
    ['ONCA DE PITANGUI', 5.33, 5.8, 5.26, 5.48, 5.21, 5.23, 5.51, 6.15, 5.85, 5.46, 4.94, 5.08],
    ['PAINEIRAS', 5.35, 5.87, 5.34, 5.68, 5.59, 5.46, 5.84, 6.44, 6.03, 5.57, 4.94, 5.13],
    ['PAPAGAIOS', 5.41, 5.87, 5.34, 5.58, 5.38, 5.28, 5.64, 6.24, 5.97, 5.51, 4.98, 5.2],
    ['PARA DE MINAS', 5.27, 5.77, 5.19, 5.46, 5.14, 5.2, 5.43, 6.04, 5.82, 5.41, 4.93, 5.05],
    ['PARAOPEBA', 5.39, 5.88, 5.35, 5.58, 5.33, 5.3, 5.61, 6.16, 6.03, 5.54, 5.01, 5.2],
    ['PASSA TEMPO', 5.13, 5.59, 5.09, 5.21, 4.91, 5.0, 5.18, 5.92, 5.58, 5.33, 4.72, 5.06],
    ['PASSOS', 5.25, 5.69, 5.24, 5.42, 5.15, 5.14, 5.32, 5.93, 5.51, 5.48, 5.17, 5.22],
    ['PATOS DE MINAS', 5.16, 5.67, 5.2, 5.56, 5.59, 5.53, 5.85, 6.61, 6.01, 5.5, 4.88, 5.02],
    ['PEDRO LEOPOLDO', 5.36, 5.75, 5.32, 5.43, 5.2, 5.14, 5.46, 6.04, 5.92, 5.5, 5.0, 5.1],
    ['PEQUI', 5.4, 5.86, 5.3, 5.47, 5.21, 5.19, 5.52, 6.18, 5.91, 5.47, 4.97, 5.12],
    ['PIEDADE DOS GERAIS', 5.21, 5.64, 5.07, 5.22, 4.96, 4.96, 5.2, 5.87, 5.62, 5.31, 4.78, 5.05],
    ['PIRACEMA', 5.13, 5.62, 5.18, 5.34, 5.07, 5.11, 5.32, 5.98, 5.65, 5.35, 4.79, 5.02],
    ['PIUMHI', 5.14, 5.64, 5.06, 5.37, 5.11, 5.11, 5.34, 6.09, 5.63, 5.42, 4.81, 5.03],
    ['POMPEU', 5.45, 5.89, 5.37, 5.65, 5.46, 5.4, 5.75, 6.29, 6.01, 5.56, 5.03, 5.22],
    ['RAPOSOS', 5.15, 5.64, 5.15, 5.2, 4.89, 5.04, 5.23, 5.89, 5.66, 5.33, 4.74, 4.94],
    ['RIBEIRAO DAS NEVES', 5.3, 5.76, 5.28, 5.37, 5.09, 5.08, 5.34, 6.0, 5.85, 5.48, 4.94, 5.0],
    ['RIO ACIMA', 5.09, 5.65, 5.18, 5.16, 4.94, 5.04, 5.16, 5.88, 5.65, 5.3, 4.72, 4.94],
    ['RIO MANSO', 5.18, 5.61, 5.1, 5.22, 5.03, 5.06, 5.28, 6.01, 5.7, 5.33, 4.78, 4.98],
    ['SABARA', 5.28, 5.7, 5.22, 5.28, 4.95, 5.08, 5.27, 5.9, 5.78, 5.44, 4.89, 5.07],
    ['SANTA LUZIA', 5.33, 5.79, 5.38, 5.39, 5.06, 5.08, 5.34, 5.95, 5.84, 5.51, 4.99, 5.11],
    ['SANTA MARIA DO SUACUI', 5.38, 5.91, 5.32, 5.01, 4.65, 4.56, 4.63, 5.21, 5.33, 5.15, 4.54, 5.12],
    ['SANTANA DE PIRAPAMA', 5.66, 6.16, 5.61, 5.59, 5.34, 5.23, 5.55, 6.05, 6.13, 5.85, 5.21, 5.46],
    ['SANTANA DO RIACHO', 5.34, 5.86, 5.4, 5.44, 5.26, 5.3, 5.55, 6.09, 6.01, 5.64, 5.03, 5.18],
    ['SANTO ANTONIO DO AMPARO', 5.04, 5.47, 4.94, 5.22, 4.9, 4.89, 5.17, 5.88, 5.5, 5.21, 4.69, 4.96],
    ['SANTO ANTONIO DO MONTE', 5.29, 5.71, 5.15, 5.46, 5.23, 5.26, 5.43, 6.14, 5.8, 5.42, 4.87, 5.0],
    ['SAO GONCALO DO ABAETE', 5.38, 5.84, 5.24, 5.61, 5.64, 5.55, 5.99, 6.58, 6.16, 5.51, 4.88, 5.1],
    ['SAO GONCALO DO PARA', 5.38, 5.77, 5.25, 5.43, 5.14, 5.24, 5.43, 6.14, 5.79, 5.45, 4.94, 5.1],
    ['SAO GONCALO DO RIO ABAIXO', 5.05, 5.54, 4.98, 4.94, 4.58, 4.6, 4.83, 5.44, 5.27, 4.98, 4.47, 4.89],
    ['SAO JOAQUIM DE BICAS', 5.34, 5.76, 5.29, 5.4, 5.09, 5.17, 5.4, 6.05, 5.82, 5.47, 4.92, 5.07],
    ['SAO JOSE DA BARRA', 5.11, 5.54, 5.13, 5.4, 5.17, 5.13, 5.35, 6.0, 5.52, 5.43, 4.98, 5.05],
    ['SAO JOSE DA LAPA', 5.32, 5.79, 5.4, 5.42, 5.16, 5.13, 5.4, 6.03, 5.88, 5.48, 5.02, 5.1],
    ['SAO PEDRO DA UNIAO', 4.92, 5.43, 4.94, 5.15, 4.92, 4.93, 5.17, 5.93, 5.42, 5.3, 4.9, 4.95],
    ['SAO SEBASTIAO DO OESTE', 5.21, 5.7, 5.1, 5.41, 5.13, 5.16, 5.38, 6.08, 5.75, 5.41, 4.82, 5.03],
    ['SARZEDO', 5.28, 5.73, 5.27, 5.36, 5.09, 5.13, 5.38, 6.04, 5.84, 5.48, 4.89, 5.06],
    ['SETE LAGOAS', 5.41, 5.86, 5.41, 5.5, 5.23, 5.21, 5.57, 6.14, 6.0, 5.55, 5.04, 5.16],
    ['TAQUARACU DE MINAS', 5.31, 5.85, 5.36, 5.34, 5.11, 5.15, 5.36, 5.97, 5.84, 5.53, 4.96, 5.12],
    ['VESPASIANO', 5.32, 5.79, 5.4, 5.43, 5.16, 5.13, 5.41, 6.03, 5.88, 5.48, 5.02, 5.13]
]

lista_disjuntores = [
    ['Monopolar', 40, 5],
    ['Monopolar', 50, 6.55],
    ['Monopolar', 63, 10],
    ['Monopolar', 70, 10],
    ['Bipolar', 40, 10],
    ['Bipolar', 50, 12],
    ['Bipolar', 60, 15],
    ['Bipolar', 63, 15.1],
    ['Bipolar', 70, 16.8],
    ['Bipolar', 80, 20],
    ['Bipolar', 90, 20],
    ['Bipolar', 100, 24],
    ['Bipolar', 120, 30],
    ['Bipolar', 125, 30],
    ['Bipolar', 150, 36],
    ['Bipolar', 200, 50],
    ['Tripolar', 40, 15],
    ['Tripolar', 60, 23],
    ['Tripolar', 63, 23],
    ['Tripolar', 70, 27],
    ['Tripolar', 80, 27],
    ['Tripolar', 100, 38],
    ['Tripolar', 120, 47],
    ['Tripolar', 125, 47],
    ['Tripolar', 150, 57],
    ['Tripolar', 175, 66],
    ['Tripolar', 200, 75],
    ['Tripolar', 225, 86],
    ['Tripolar', 250, 95],
    ['Tripolar', 300, 114],
    ['Tripolar', 315, 114],
    ['Tripolar', 320, 114],
    ['Tripolar', 400, 152],
    ['Tripolar', 450, 171],
    ['Tripolar', 500, 188],
    ['Tripolar', 600, 228],
    ['Tripolar', 630, 228],
    ['Tripolar', 700, 266],
    ['Tripolar', 800, 304]
]

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para determinar a carga de acordo com o disjuntor da instalação
def carga_instalacao(aumento_carga: bool, polaridade_atual: str, disjuntor_atual: int, nova_polaridade: str, novo_disjuntor: int):
    if aumento_carga == False:
        polaridade = polaridade_atual
        corrente = disjuntor_atual
    else:
        polaridade = nova_polaridade
        corrente = novo_disjuntor

    carga: int = 0

    for disjuntor in lista_disjuntores:
        if polaridade == disjuntor[0]:
            if corrente == disjuntor[1]:
                carga = disjuntor[2]

    return carga

# Função para determinar a potência de pico total dos módulos anteriores
def potencia_total_modulos_anterior(ant_1: bool, quantidade_1: int, potencia_1: int, ant_2: bool, quantidade_2: int, potencia_2: int):
    quantidade: int = 0
    potencia: int = 0

    if ant_1 == True:
        quantidade = quantidade_1
        potencia = potencia_1

    if ant_2 == True:
        quantidade = quantidade_2
        potencia = potencia_2

    potencia_total = (quantidade * potencia) / 1000

    return potencia_total

# Função para determinar a potência de pico total dos módulos
def potencia_total_modulos(quantidade_1: int, potencia_1: int, quantidade_2: int, potencia_2: int):
    potencia_total = (quantidade_1 * potencia_1 + quantidade_2 * potencia_2) / 1000

    return potencia_total

# Função para determinar a área ocupada pelos módulos
def area_modulos(quantidade_1: int, comprimento_1: float, largura_1: float, quantidade_2: int, comprimento_2: float, largura_2: float):
    area_total = quantidade_1 * (comprimento_1 / 1000) * (largura_1 / 1000) + quantidade_2 * (comprimento_2 / 1000) * (largura_2 / 1000)

    return round(area_total, 1)

# Função para determinar a potência total dos inversores anteriores
def potencia_total_inversores_anterior(ant_1: bool, quantidade_1: int, potencia_1: int, ant_2: bool, quantidade_2: int, potencia_2: int, ant_3: bool, quantidade_3: int, potencia_3: int, ant_4: bool, quantidade_4: int, potencia_4: int):
    if ant_1 == False:
        quantidade_1 = 0
        potencia_1 = 0

    if ant_2 == False:
        quantidade_2 = 0
        potencia_2 = 0

    if ant_3 == False:
        quantidade_3 = 0
        potencia_3 = 0

    if ant_4 == False:
        quantidade_4 = 0
        potencia_4 = 0

    potencia_total = (quantidade_1 * potencia_1 + quantidade_2 * potencia_2 + quantidade_3 * potencia_3 + quantidade_4 * potencia_4) / 1000

    return potencia_total

# Função para determinar a potência total dos inversores
def potencia_total_inversores(quantidade_1: int, potencia_1: int, quantidade_2: int, potencia_2: int, quantidade_3: int, potencia_3: int, quantidade_4: int, potencia_4: int):
    potencia_total = (quantidade_1 * potencia_1 + quantidade_2 * potencia_2 + quantidade_3 * potencia_3 + quantidade_4 * potencia_4) / 1000

    return potencia_total

# Função para determinar as horas de sol pleno de uma determinada cidade
def horas_sol_pleno(cidade_desejada: str):
    cidade_desejada
    
    lista_horas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for cidade in lista_cidades:
        cidade[0]
        if cidade_desejada == cidade[0]:
            lista_horas = cidade[1:13]
            
    return lista_horas

# Função para determinar a geração mensal em uma determinada cidade
def geracao(potencia_total: int, cidade: str, mes: int):
    horas_mes = horas_sol_pleno(cidade)
    
    geracao_mensal = (0.8 * potencia_total * horas_mes[mes - 1] * 30)

    return round(geracao_mensal, 2)