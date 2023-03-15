from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Função para criar um token de acesso
def criar_token_acesso(dados: dict):
    encriptar = dados.copy()                                                       # Criando cópia dos dados passados para o token

    expira_em = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Determinando o tempo que o token deve expirar
    encriptar.update({'exp': expira_em})                                           # Incluindo o tempo que o token deve expirar ao dicionário com os dados necessários para o token

    token_acesso = jwt.encode(encriptar, SECRET_KEY, algorithm=ALGORITHM)          # Criando token de acesso com os dados passados

    return token_acesso                                                            # Retornando token de acesso

# Função para verificar um token de acesso
def verificar_token_acesso(token_acesso: str, excecao_credenciais):
    try:
        payload = jwt.decode(token_acesso, SECRET_KEY, algorithms=[ALGORITHM]) # Decodificando o token de acesso
        nome: str = payload.get('nome')                                        # Variável para determinar o nome do usuário que havia sido encriptado no token de acesso
        id: int = payload.get('id')                                            # Variável para determinar a id do usuário que havia sido encriptada no token de acesso

        # Caso realmente houver dados encriptados no token de acesso
        if nome != None:
            dados_token = schemas.TokenData(nome=nome, id=id)                 # Cria objeto com os dados do usuário retirados do token de acesso
            return dados_token
        # Caso não haja dados encriptados no token de acesso
        else:
            raise excecao_credenciais

    # Caso ocorra algum erro JWT
    except JWTError:
        raise excecao_credenciais

# Função para determinar o usuário atual
def determinar_usuario_atual(token_acesso: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    excecao_credenciais = HTTPException(                                                       # Criando objeto contendo a exceção a ser levantada caso o usuário não esteja autorizado
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    dados_token = verificar_token_acesso(token_acesso, excecao_credenciais)                    # Variável para armazenar os dados contidos no token de acesso
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == dados_token.nome).first() # Criando objeto para conter o usuário atual
    return usuario                                                                             # Retornando o usuário atual