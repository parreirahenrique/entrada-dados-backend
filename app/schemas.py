from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

# Esquemas para os usuários
class UserCreate(BaseModel): # Classe para os dados necessários para criação de um usuário
    nome: str                # Nome do usuário
    senha: str               # Senha do usuário
    
class UserOut(BaseModel): # Classe para os dados de saída quando um usuário é criado
    id: int               # ID do usuário
    nome: str             # Nome do usuário
    cargo: str            # Cargo do usuário
    criado_em: datetime   # Data de criação do usuário
    
    class Config:
        orm_mode = True

class UserUpdate(BaseModel): # Classe para os dados necessários para a atualização de um usuário
    nome: Optional[str]      # Nome do usuário
    senha: Optional[str]     # Senha do usuário

class UserLogin(BaseModel): # Classe para dados de login de usuário
    username: str           # Nome do usário para login
    password: str           # Senha do usuário para login

# Esquemas para os clientes
class ClientInsert(BaseModel):       # Classe para os dados necessário para a inserção de um novo cliente
    nome: str                        # Nome do cliente
    cpf: str                         # CPF do cliente
    numero_cliente: int              # Número do cliente na CEMIG
    nome_pais: Optional[str] = None  # Nome do pai/mãe
    rg: Optional[str] = None         # Número do RG
    nascimento: Optional[str] = None # Data de nascimento

class ClientUpdate(BaseModel):       # Classe para os dados necessários para a atualização de um cliente
    nome: Optional[str]              # Nome do cliente
    cpf: Optional[str]               # CPF do cliente
    numero_cliente: Optional[int]    # Número do cliente
    nome_pais: Optional[str] = None  # Nome do pai/mãe
    rg: Optional[str] = None         # Número do RG
    nascimento: Optional[str] = None # Data de nascimento
    
class ClientOut(ClientInsert): # Classe para os dados de saída quando um novo cliente for inserido
    criado_em: datetime        # Além dos dados necessários na inserção de um cliente, retorna a data se inserção
    criado_por: int            # Além dos dados necessários na inserção de um cliente, retorna quem inseriu
    
    class Config:
        orm_mode = True

# Esquemas para os clientes
class InstalationInsert(BaseModel):      # Classe para os dados necessário para a inserção de um novo cliente
    logradouro: str                      # Logradouro da instalação
    numero_predial: int                  # Número predial da instalação
    complemento: str                     # Complemento da instalação
    bairro: str                          # Bairro da instalação
    cidade: str                          # Cidade da instalação
    cep: str                             # CEP da instalação
    numero_instalacao: Optional[int] = 0 # Número da instalação na CEMIG
    numero_cliente: int                  # Número do cliente
    classificacao: str                   # Classificação da residência na CEMIG
    latitude: int                        # Latitude da instalação em UTM
    longitude: int                       # Longitude da instalação em UTM
    coordenadas_decimais: str            # Coordenadas decimais da instalação
    
class InstalationUpdate(BaseModel):     # Classe para os dados necessário para a inserção de um novo cliente
    logradouro: Optional[str]           # Logradouro da instalação
    numero_predial: Optional[int]       # Número predial da instalação
    complemento: Optional[str]          # Complemento da instalação
    bairro: Optional[str]               # Bairro da instalação
    cidade: Optional[str]               # Cidade da instalação
    cep: Optional[str]                  # CEP da instalação
    numero_instalacao: Optional[int]    # Número da instalação na CEMIG
    numero_cliente: Optional[int]       # Número do cliente
    classificacao: Optional[str]        # Classificação da residência na CEMIG
    latitude: Optional[int]             # Latitude da instalação em UTM
    longitude: Optional[int]            # Longitude da instalação em UTM
    coordenadas_decimais: Optional[str] # Coordenadas decimais da instalação

class InstalationOut(InstalationInsert): # Classe para os dados de saída quando uma nova instalação for inserida
    criado_em: datetime                  # Além dos dados necessários na inserção da instalação, retorna a data se inserção
    criado_por: int                      # Além dos dados necessários na inserção da instalação, retorna quem inseriu

    class Config:
        orm_mode = True

# Esquemas para os módulos
class ModuleInsert(BaseModel):     # Classe para os dados necessários para a inserção de um novo módulo
    modelo: str                    # Modelo
    fabricante: str                # Fabricante
    potencia: int                  # Potência de pico
    imp: float                     # Corrente no ponto de máxima potência
    isc: float                     # Corrente de curto circuito
    vmp: float                     # Tensão no ponto de máxima potência
    voc: float                     # Tensão de circuito aberto
    comprimento: float             # Comprimento
    largura: float                 # Largura
    espessura: float               # Espessura
    eficiencia: float              # Eficiência
    temperatura_nominal: str       # Temperatura nominal de operação
    tipo: str                      # Tipo cristalino
    coeficiente_temperatura: float # Coeficiente de temperatura de circuito aberto

class ModuleUpdate(BaseModel):               # Classe para os dados necessários para a inserção de um novo módulo
    modelo: Optional[str]                    # Modelo
    fabricante: Optional[str]                # Fabricante
    potencia: Optional[int]                  # Potência de pico
    imp: Optional[float]                     # Corrente no ponto de máxima potência
    isc: Optional[float]                     # Corrente de curto circuito
    vmp: Optional[float]                     # Tensão no ponto de máxima potência
    voc: Optional[float]                     # Tensão de circuito aberto
    comprimento: Optional[float]             # Comprimento
    largura: Optional[float]                 # Largura
    espessura: Optional[float]               # Espessura
    eficiencia: Optional[float]              # Eficiência
    temperatura_nominal: Optional[str]       # Temperatura nominal de operação
    tipo: Optional[str]                      # Tipo cristalino
    coeficiente_temperatura: Optional[float] # Coeficiente de temperatura de circuito aberto
    
class ModuleOut(ModuleInsert): # Classe para os dados de saída quando um novo módulo for inserido
    id: str                    # Além dos dados necessários na inserção do módulo, retorna a ID
    criado_em: datetime        # Além dos dados necessários na inserção do módulo, retorna a data e hora de criação
    criado_por: int            # Além dos dados necessários na inserção da instalação, retorna quem inseriu

    class Config:
        orm_mode = True

# Esquemas para os inversores
class InverterInsert(BaseModel):   # Classe para os dados necessários para a inserção de um novo inversor
    modelo: str                    # Modelo
    fabricante: str                # Fabricante
    potencia: int                  # Potência de pico
    overload: int                  # Overload
    imp: float                     # Corrente no ponto de máxima potência
    isc: float                     # Corrente de curto circuito
    v_min_mppt: int                # Tensão mínima do range da MPPT
    v_max_mppt: int                # Tensão máxima do range da MPPT
    v_max: int                     # Tensão máxima de entrada
    n_mppt: int                    # Número de MPPTs
    n_entrada: int                 # Número de entradas
    v_saida: int                   # Tensão de saída
    i_saida: float                 # Corrente de saída
    comprimento: float             # Comprimento
    largura: float                 # Largura
    espessura: float               # Espessura
    eficiencia: float              # Eficiência

class InverterUpdate(BaseModel): # Classe para os dados necessários para a inserção de um novo inversor
    modelo: Optional[str]        # Modelo
    fabricante: Optional[str]    # Fabricante
    potencia: Optional[int]      # Potência de pico
    overload: Optional[int]      # Potência máxima de entrada
    imp: Optional[float]         # Corrente no ponto de máxima potência
    isc: Optional[float]         # Corrente de curto circuito
    v_min_mppt: Optional[int]    # Tensão mínima do range da MPPT
    v_max_mppt: Optional[int]    # Tensão máxima do range da MPPT
    v_max: Optional[int]         # Tensão máxima de entrada
    n_mppt: Optional[int]        # Número de MPPTs
    n_entrada: Optional[int]     # Número de entradas
    v_saida: Optional[int]       # Tensão de saída
    i_saida: Optional[float]     # Corrente de saída
    comprimento: Optional[float] # Comprimento
    largura: Optional[float]     # Largura
    espessura: Optional[float]   # Espessura
    eficiencia: Optional[float]  # Eficiência
    
class InverterOut(InverterInsert): # Classe para os dados de saída quando um novo inversor for inserido
    id: str                        # Além dos dados necessários na inserção do inversor, retorna a ID
    criado_em: datetime            # Além dos dados necessários na inserção do inversor, retorna a data e hora de criação
    criado_por: int                # Além dos dados necessários na inserção da instalação, retorna quem inseriu

    class Config:
        orm_mode = True
    
# Esquemas para os projetos
class ProjectInsert(BaseModel):                 # Classe para os dados necessários para a inserção de um novo projeto
    numero_instalacao: int                      # Número da instalação
    numero_cliente: int                         # Número do cliente
    ligacao_nova: bool                          # Identificação se o projeto será ligação nova
    aumento_carga: bool                         # Identificação se o projeto terá aumento de carga
    aumento_usina: bool                         # Identificação se o projeto terá aumento de usina
    agrupamento: bool                           # Identificação se a unidade consumidora pertence a um agrupamento
    n_fases: str                                # Número de fases da unidade consumidora
    disjuntor: int                              # Disjuntor da unidade consumidora
    novo_n_fases: Optional[str]                 # Novo número de fases da unidade consumidora
    novo_disjuntor: Optional[int] = 0           # Novo disjuntor da unidade consumidora
    n_fases_agrupamento: Optional[str]          # Número de fases do agrupamento
    disjuntor_agrupamento: Optional[int] = 0    # Disjuntor do agrupamento
    tensao: int                                 # Tensão de atendimento
    
    modulo_anterior_1: bool                     # Determinar se o primeiro módulo é da usina anterior
    quantidade_modulo_1: int                    # Quantidade do primeiro módulo
    modelo_modulo_1: str                        # Modelo do primeiro módulo
    
    modulo_anterior_2: Optional[bool] = False   # Determinar se o segundo módulo é da usina anterior
    quantidade_modulo_2: Optional[int] = 0      # Quantidade do segundo módulo
    modelo_modulo_2: Optional[str] = None       # Potência do segundo módulo

    inversor_anterior_1: bool                   # Determinar se o primeiro inversor é da usina anterior
    quantidade_inversor_1: int                  # Quantidade do primeiro inversor
    modelo_inversor_1: str                      # Modelo do primeiro inversor
    
    inversor_anterior_2: Optional[bool] = False # Determinar se o segundo inversor é da usina anterior
    quantidade_inversor_2: Optional[int] = 0    # Quantidade do segundo inversor
    modelo_inversor_2: Optional[str] = None     # Modelo do segundo inversor
    
    inversor_anterior_3: Optional[bool] = False # Determinar se o terceiro inversor é da usina anterior
    quantidade_inversor_3: Optional[int] = 0    # Quantidade do terceiro inversor
    modelo_inversor_3: Optional[str] = None     # Modelo do terceiro inversor
    
    inversor_anterior_4: Optional[bool] = False # Determinar se o quarto inversor é da usina anterior
    quantidade_inversor_4: Optional[int] = 0    # Quantidade do quarto inversor
    modelo_inversor_4: Optional[str] = None     # Modelo do quarto inversor
    
class ProjectOut(ProjectInsert):                # Classe para os dados de saída quando um novo projeto for inserido
    id: int                                     # ID do projeto
    carga: int                                  # Carga instalada
    quantidade_modulos: int                     # Quantidade total de módulos
    potencia_modulos_anterior: float            # Potência total dos módulos anteriores
    potencia_modulos: float                     # Potência total dos módulos
    area: float                                 # Área ocupada pelos módulos
    quantidade_inversores: int                  # Número total de inversores
    potencia_inversores_anterior: float         # Potência total dos inversores anteriores
    potencia_inversores: float                  # Potência total dos inversores
    geracao_1: float                            # Geração média mensal de janeiro
    geracao_2: float                            # Geração média mensal de fevereiro
    geracao_3: float                            # Geração média mensal de março
    geracao_4: float                            # Geração média mensal de abril
    geracao_5: float                            # Geração média mensal de maio
    geracao_6: float                            # Geração média mensal de junho
    geracao_7: float                            # Geração média mensal de julho
    geracao_8: float                            # Geração média mensal de agosto
    geracao_9: float                            # Geração média mensal de setembro
    geracao_10: float                           # Geração média mensal de outubro
    geracao_11: float                           # Geração média mensal de novembro
    geracao_12: float                           # Geração média mensal de dezembro
    criado_em: datetime                         # Data de criação do projeto

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    numero_instalacao: Optional[int]     # Número da instalação
    numero_cliente: Optional[int]        # Número do cliente
    ligacao_nova: Optional[bool]         # Identificação se o projeto será ligação nova
    aumento_carga: Optional[bool]        # Identificação se o projeto terá aumento de carga
    aumento_usina: Optional[bool]        # Identificação se o projeto terá aumento de usina
    agrupamento: Optional[bool]          # Identificação se a unidade consumidora pertence a um agrupamento
    n_fases: Optional[str]               # Número de fases da unidade consumidora
    disjuntor: Optional[int]             # Disjuntor da unidade consumidora
    novo_n_fases: Optional[str]          # Novo número de fases da unidade consumidora
    novo_disjuntor: Optional[int]        # Novo disjuntor da unidade consumidora
    n_fases_agrupamento: Optional[str]   # Número de fases do agrupamento
    disjuntor_agrupamento: Optional[int] # Disjuntor do agrupamento
    tensao: Optional[int]                # Tensão de atendimento
    
    modulo_anterior_1: Optional[bool]    # Determinar se o primeiro módulo é da usina anterior
    quantidade_modulo_1: Optional[int]   # Quantidade do primeiro módulo
    modelo_modulo_1: Optional[str]       # Modelo do primeiro módulo
    
    modulo_anterior_2: Optional[bool]    # Determinar se o segundo módulo é da usina anterior
    quantidade_modulo_2: Optional[int]   # Quantidade do segundo módulo
    modelo_modulo_2: Optional[str]       # Potência do segundo módulo

    inversor_anterior_1: Optional[bool]  # Determinar se o primeiro inversor é da usina anterior
    quantidade_inversor_1: Optional[int] # Quantidade do primeiro inversor
    modelo_inversor_1: Optional[str]     # Modelo do primeiro inversor
    
    inversor_anterior_2: Optional[bool]  # Determinar se o segundo inversor é da usina anterior
    quantidade_inversor_2: Optional[int] # Quantidade do segundo inversor
    modelo_inversor_2: Optional[str]     # Modelo do segundo inversor
    
    inversor_anterior_3: Optional[bool]  # Determinar se o terceiro inversor é da usina anterior
    quantidade_inversor_3: Optional[int] # Quantidade do terceiro inversor
    modelo_inversor_3: Optional[str]     # Modelo do terceiro inversor
    
    inversor_anterior_4: Optional[bool]  # Determinar se o quarto inversor é da usina anterior
    quantidade_inversor_4: Optional[int] # Quantidade do quarto inversor
    modelo_inversor_4: Optional[str]     # Modelo do quarto inversor


# Esquemas para os tokens de autenticação
class Token(BaseModel): # Classe para os dados necessário para o token de autenticação
    access_token: str   # Token de acesso
    token_type: str     # Tipo do token

class TokenData(BaseModel):        # Classe para os dados necessário para a criação de um token de autenticação
    nome: Optional[str] = None     # Nome do cliente
    id: Optional[int] = 0          # ID co cliente