from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Users']
)

# Função para criar um novo usuário, sem permissões de admnistrador
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(usuario: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Criptografando a senha
    hashed_password = utils.hash(usuario.senha)
    usuario.senha = hashed_password
    
    # Adicionando novo usuário ao banco de dados
    novo_usuario = models.Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# Função para adquirir os dados de um usuário
@router.get('/users/{nome}', response_model=schemas.UserOut)
def get_one_user(nome: str, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
    
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Caso o nome do usuário informado esteja cadastrado no banco de dados
        if usuario != None:
            # Caso o usuário atual seja um administrador
            if usuario_atual.cargo == 'Administrador':
                return usuario

            # Caso o usuário atual não seja um administrador
            else: 
                # Caso o usuário queira suas próprias informações
                if usuario.nome == usuario_atual.nome:
                    return usuario

                # Caso o usuário queira informações de outro usuário
                else:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Não é possível obter informações de outro usuário')

        # Caso o nome do usuário informado não esteja cadastrado no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário de nome {nome} não existe')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de requisitar as informações de um usuário')
    
# Função para adquirir os dados de todos os usuários
@router.get('/users', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Caso o usuário atual não seja um administrador
        if usuario_atual.cargo == 'Administrador':
            usuarios = db.query(models.Usuario).all()
            return usuarios
        
        # Caso o usuário atual não esteja validado
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login como um administrador antes de requisitar as informações dos usuários')
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de requisitar as informações dos usuário')
    
# Função para atualizar os dados de um usuário
@router.patch('/users/{nome}')
def update_user(nome: str, usuario_atualizado: schemas.UserUpdate, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
        
        # Caso o número do cliente informado esteja presente no banco de dados
        if usuario != None:
            # Caso o usuário logado seja um administrador
            if usuario_atual.cargo == 'Administrador':
                # Caso seja desejado atualizar o nome do usuário
                if usuario_atualizado.nome != None:
                    usuario.nome = usuario_atualizado.nome

                # Caso seja desejado atualizar a senha do usuário
                if usuario_atualizado.senha != None:
                    usuario.senha = utils.hash(usuario_atualizado.senha)

                db.commit() # Atualizando as informações no banco de dados
                return {'detail': f'Dados do usuário {nome} alteradas com sucesso'}
            
            else:
                # Caso o usuário queira atualizar seus próprios dados
                if usuario_atual.nome == usuario.nome:
                    # Caso seja desejado atualizar a senha do usuário
                    if usuario_atualizado.senha != None:
                        usuario.senha = utils.hash(usuario_atualizado.senha)
                        db.commit() # Atualizando as informações no banco de dados
                        return {'detail': f'Senha do usuário {nome} alterada com sucesso'}

                    else:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Apenas a senha do usuário pode ser atualizada')
                # Caso o usuário queira atualizar dados de outro usuário
                else:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Não é possível atualizar dados de outro usuário')

            
        # Caso o número do cliente informado não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário de nome {nome} não existe')

    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de atualizar um usuário')
    
# Função para deletar um usuário
@router.delete('/users/{nome}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(nome: str, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado e seja um administrador
    if usuario_atual.cargo == 'Administrador':
        usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome)

        # Caso o nome de usuário informado exista no bando de dados
        try:
            if usuario.first().nome != None:
                usuario.delete(synchronize_session=False)
                db.commit()
        
        # Caso o nome de usuário informado não exista no bando de dados
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Usuário de nome {nome} não existe')

    # Caso o usuário atual não esteja validado ou não seja um adminsitrador
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login como administrador antes de deletar um usuário')