from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# Classe para a tabela de usuários
class Usuario(Base):
    __tablename__ = 'usuarios' # Nome da tabela

    # Colunas da tabela
    id = Column(Integer, unique=True, primary_key=True, nullable=False)                        # Coluna para identificação do número do usuário
    nome = Column(String, nullable=False, unique=True)                                         # Coluna para o nome
    senha = Column(String, nullable=False)                                                     # Coluna para o hash da senha
    cargo = Column(String, nullable=False, server_default='Usuário')                           # Coluna para o cargo do usuário
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False) # Coluna para identificar a data e hora de criação

# Classe para a tabela de clientes
class Cliente(Base):
    __tablename__ = 'clientes' # Nome da tabela

    # Colunas da tabela
    numero_cliente = Column(BigInteger, unique=True, primary_key=True, nullable=False)          # Coluna para o número do cliente
    nome = Column(String, nullable=False)                                                       # Coluna para o nome
    cpf = Column(String, nullable=False)                                                        # Coluna para o CPF
    rg = Column(String, nullable=True)                                                          # Coluna para o RG
    nome_pais = Column(String, nullable=True)                                                   # Coluna para o nome do pai/mãe
    nascimento = Column(String, nullable=True)                                                  # Coluna para a data de nascimento
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # Coluna para identificar a data e hora de inserção
    criado_por = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False) # Coluna para identificar quem inseriu o cliente
    
# Classe para a tabela de instalações
class Instalacao(Base):
    __tablename__ = 'instalacoes' # Nome da tabela

    # Colunas da tabela
    numero_instalacao = Column(BigInteger, unique=True, primary_key=True, nullable=False)                          # Coluna para o número da instalação
    numero_cliente = Column(BigInteger, ForeignKey('clientes.numero_cliente', ondelete='CASCADE'), nullable=False) # Coluna para o número do cliente titular da instalação
    logradouro = Column(String, nullable=False)                                                                    # Coluna para o logradouro
    numero_predial = Column(Integer, nullable=False)                                                               # Coluna para o número predial
    complemento = Column(String, nullable=False)                                                                   # Coluna para o complemento
    bairro = Column(String, nullable=False)                                                                        # Coluna para o bairro
    cidade = Column(String, nullable=False)                                                                        # Coluna para a cidade
    cep = Column(String, nullable=False)                                                                           # Coluna para o CEP
    classificacao = Column(String, nullable=False)                                                                 # Coluna para a classificação da unidade consumidora
    latitude = Column(Integer, nullable=False)                                                                     # Coluna para a latitude
    longitude = Column(Integer, nullable=False)                                                                    # Coluna para a longitude
    coordenadas_decimais = Column(String, nullable=False)                                                          # Coluna para as coordenadas decimais
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)                     # Coluna para identificar a data e hora de inserção
    criado_por = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)                    # Coluna para identificar quem inseriu a instalação

# Classe para a tabela de módulos
class Modulo(Base):
    __tablename__ = 'modulos' # Nome da tabela

    # Colunas da tabela
    id = Column(Integer, nullable=False)                                                        # Coluna para identificação do número do módulo
    modelo = Column(String, primary_key=True, unique=True, nullable=False)                      # Coluna para o modelo
    fabricante = Column(String, nullable=False)                                                 # Coluna para o fabricante
    potencia = Column(Integer, nullable=False)                                                  # Coluna para a potência de pico
    imp = Column(Float, nullable=False)                                                         # Coluna para a corrente no ponto de máxima potência
    isc = Column(Float, nullable=False)                                                         # Coluna para a corrente de curto circuito
    vmp = Column(Float, nullable=False)                                                         # Coluna para a tensão no ponto de máxima potência
    voc = Column(Float, nullable=False)                                                         # Coluna para a tensão de circuito aberto
    comprimento = Column(Float, nullable=False)                                                 # Coluna para o comprimento
    largura = Column(Float, nullable=False)                                                     # Coluna para a largura
    espessura = Column(Float, nullable=False)                                                   # Coluna para a espessura
    eficiencia = Column(Float, nullable=False)                                                  # Coluna para a eficiência
    temperatura_nominal = Column(String, nullable=False)                                        # Coluna para a temperatura nominal de operação
    tipo = Column(String, nullable=False)                                                       # Coluna para o tipo cristalino
    coeficiente_temperatura = Column(Float, nullable=False)                                     # Coluna para o coeficiente de temperatura de circuito aberto
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # Coluna para identificar a data e hora de inserção
    criado_por = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False) # Coluna para identificar quem inseriu o módulo

# Classe para a tabela de inversores
class Inversor(Base):
    __tablename__ = 'inversores' # Nome da tabela

    # Colunas da tabela
    id = Column(Integer, nullable=False)                                                        # Coluna para identificação do número do módulo
    modelo = Column(String, primary_key=True, unique=True, nullable=False)                      # Coluna para o modelo
    fabricante = Column(String, nullable=False)                                                 # Coluna para o fabricante
    potencia = Column(Integer, nullable=False)                                                  # Coluna para a potência nominal
    overload = Column(Integer, nullable=False)                                                  # Coluna para a potência máxima de entrada
    imp = Column(Float, nullable=False)                                                         # Coluna para a corrente máxima de entrada
    isc = Column(Float, nullable=False)                                                         # Coluna para a corrente máxima de curto circuito
    v_min_mppt = Column(Integer, nullable=False)                                                # Coluna para a tensão mínima do range da MPPT
    v_max_mppt = Column(Integer, nullable=False)                                                # Coluna para a tensão máxima do range da MPPT
    v_max = Column(Integer, nullable=False)                                                     # Coluna para a tensão máxima de entrada
    n_mppt = Column(Integer, nullable=False)                                                    # Coluna para o número de MPPTs
    n_entrada = Column(Integer, nullable=False)                                                 # Coluna para o número de entradas
    v_saida = Column(Integer, nullable=False)                                                   # Coluna para a tensão de saída
    i_saida = Column(Float, nullable=False)                                                     # Coluna para a corrente de saída
    eficiencia = Column(Float, nullable=False)                                                  # Coluna para a eficiência
    comprimento = Column(Float, nullable=False)                                                 # Coluna para o comprimento
    largura = Column(Float, nullable=False)                                                     # Coluna para a largura
    espessura = Column(Float, nullable=False)                                                   # Coluna para a espessura
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # Coluna para identificar a data e hora de inserção
    criado_por = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False) # Coluna para identificar quem inseriu o inversor

# Classe para a tabela de projetos
class Projeto(Base):

    __tablename__ = 'projetos' # Nome da tabela

    # Colunas da tabela para as informações da instalação
    id = Column(Integer, unique=True, primary_key=True, nullable=False)                                                     # Coluna para identificação do número do projeto
    criado_em = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)                              # Coluna para identificar a data e hora de inserção
    criado_por = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)                             # Coluna para identificar quem criou o projeto
    numero_instalacao = Column(BigInteger, ForeignKey('instalacoes.numero_instalacao', ondelete='CASCADE'), nullable=False) # Coluna para o número da instalação
    numero_cliente = Column(BigInteger, ForeignKey('clientes.numero_cliente', ondelete='CASCADE'), nullable=False)          # Coluna para o número do cliente
    ligacao_nova = Column(Boolean, nullable=False)                                                                          # Coluna para identificação se o projeto será ligação nova
    aumento_carga = Column(Boolean, nullable=False)                                                                         # Coluna para identificação se o projeto terá aumento de carga
    aumento_usina = Column(Boolean, nullable=False)                                                                         # Coluna para identificação se o projeto terá aumento de usina
    agrupamento = Column(Boolean, nullable=False)                                                                           # Coluna para identificação se a unidade consumidora pertence a um agrupamento
    n_fases = Column(String, nullable=False)                                                                                # Coluna para o número de fases da unidade consumidora
    disjuntor = Column(Integer, nullable=False)                                                                             # Coluna para o disjuntor da unidade consumidora
    novo_n_fases = Column(String, nullable=True)                                                                            # Coluna para o novo número de fases da unidade consumidora
    novo_disjuntor = Column(Integer, nullable=True)                                                                         # Coluna para o novo disjuntor da unidade consumidora
    n_fases_agrupamento = Column(String, nullable=True)                                                                     # Coluna para o número de fases do agrupamento
    disjuntor_agrupamento = Column(Integer, nullable=True)                                                                  # Coluna para o disjuntor do agrupamento
    tensao = Column(Integer, nullable=False)                                                                                # Coluna para a tensão de atendimento
    carga = Column(Float, nullable=False)                                                                                   # Coluna para a carga instalada
    
    # Colunas da tabela para as informações dos módulos
    modulo_anterior_1 = Column(Boolean, nullable=False, server_default='FALSE')                                             # Coluna para determinar se o primeiro módulo é da usina anterior
    quantidade_modulo_1 = Column(Integer, nullable=False)                                                                   # Coluna para a quantidade do primeiro módulo
    modelo_modulo_1 = Column(String, nullable=False)                                                                        # Coluna para o modelo do primeiro módulo
    potencia_modulo_1 = Column(Integer, nullable=False)                                                                     # Coluna para a potência de pico do primeiro módulo
    
    modulo_anterior_2 = Column(Boolean, nullable=True, server_default='FALSE')                                              # Coluna para determinar se o segundo módulo é da usina anterior
    quantidade_modulo_2 = Column(Integer, nullable=True, server_default='0')                                                # Coluna para a quantidade do segundo módulo
    modelo_modulo_2 = Column(String, server_default='')                                                                     # Coluna para o modelo do segundo módulo
    potencia_modulo_2 = Column(Integer, nullable=False, server_default='0')                                                 # Coluna para a potência de pico do segundo módulo
    
    quantidade_modulos = Column(Integer, nullable=False)                                                                    # Coluna para o número total de módulos
    potencia_modulos_anterior = Column(Float, nullable=True)                                                                # Coluna para a potência total dos módulos anteriores
    potencia_modulos = Column(Float, nullable=False)                                                                        # Coluna para a potência total dos módulos
    area = Column(Float, nullable=False)                                                                                    # Coluna para a área ocupada pelos módulos

    # Colunas da tabela para as informações dos inversores
    inversor_anterior_1 = Column(Boolean, nullable=False)                                                                   # Coluna para determinar se o primeiro inversor é da usina anterior
    quantidade_inversor_1 = Column(Integer, nullable=False)                                                                 # Coluna para a quantidade do primeiro inversor
    modelo_inversor_1 = Column(String, nullable=False)                                                                      # Coluna para o modelo do primeiro inversor
    potencia_inversor_1 = Column(Integer, nullable=False)                                                                   # Coluna para a potência nominal do primeiro inversor
    
    inversor_anterior_2 = Column(Boolean, nullable=True, server_default='FALSE')                                            # Coluna para determinar se o segundo inversor é da usina anterior
    quantidade_inversor_2 = Column(Integer, nullable=True, server_default='0')                                              # Coluna para a quantidade do segundo inversor
    modelo_inversor_2 = Column(String, server_default='', nullable=True)                                                    # Coluna para o modelo do segundo inversor
    potencia_inversor_2 = Column(Integer, nullable=False, server_default='0')                                               # Coluna para a potência nominal do segundo inversor

    inversor_anterior_3 = Column(Boolean, nullable=True, server_default='FALSE')                                            # Coluna para determinar se o terceiro inversor é da usina anterior
    quantidade_inversor_3 = Column(Integer, nullable=True, server_default='0')                                              # Coluna para a quantidade do terceiro inversor
    modelo_inversor_3 = Column(String, server_default='', nullable=True)                                                    # Coluna para o modelo do terceiro inversor
    potencia_inversor_3 = Column(Integer, nullable=False, server_default='0')                                               # Coluna para a potência nominal do terceiro inversor

    inversor_anterior_4 = Column(Boolean, nullable=True, server_default='FALSE')                                            # Coluna para determinar se o quarto inversor é da usina anterior
    quantidade_inversor_4 = Column(Integer, nullable=True, server_default='0')                                              # Coluna para a quantidade do quarto inversor
    modelo_inversor_4 = Column(String, server_default='', nullable=True)                                                    # Coluna para o modelo do quarto inversor
    potencia_inversor_4 = Column(Integer, nullable=False, server_default='0')                                               # Coluna para a potência nominal do quarto inversor

    quantidade_inversores = Column(Integer, nullable=False)                                                                 # Coluna para o número total de inversores
    potencia_inversores_anterior = Column(Float, nullable=True)                                                             # Coluna para a potência total dos inversores anteriores
    potencia_inversores = Column(Float, nullable=False)                                                                     # Coluna para a potência total dos inversores
    
    # Colunas da tabela para as informações das gerações mensais 
    geracao_1 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de janeiro
    geracao_2 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de fevereiro
    geracao_3 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de março
    geracao_4 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de abril
    geracao_5 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de maio
    geracao_6 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de junho
    geracao_7 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de julho
    geracao_8 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de agosto
    geracao_9 = Column(Float, nullable=False)                                                                               # Coluna para a geração média mensal de setembro
    geracao_10 = Column(Float, nullable=False)                                                                              # Coluna para a geração média mensal de outubro
    geracao_11 = Column(Float, nullable=False)                                                                              # Coluna para a geração média mensal de novembro
    geracao_12 = Column(Float, nullable=False)                                                                              # Coluna para a geração média mensal de dezembro