from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(
    tags=['Usuários']
)

@router.post('/login', response_model=schemas.Token)
def login(credenciais_usuario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == credenciais_usuario.username).first()

    # Caso o usuário atual não esteja cadastrado no banco de dados
    if usuario != None:

        # Caso a senha informada esteja condizente com a senha armazenada no banco de dados
        if utils.verify(credenciais_usuario.password, usuario.senha) == True:
            token_acesso = oauth2.criar_token_acesso(dados={'nome': usuario.nome, 'id': usuario.id})
            return {'access_token': token_acesso, 'token_type': 'bearer'}

        # Caso a senha informada não esteja condizente com a senha armazenada no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credenciais inválidas')

    # Caso o usuário atual não esteja cadastrado no banco de dados
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credenciais inválidas')