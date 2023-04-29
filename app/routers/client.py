from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    tags=['Clientes']
)

# Função para inserir um novo cliente
@router.post('/clients', status_code=status.HTTP_201_CREATED, response_model=schemas.ClientOut)
def create_client(cliente: schemas.ClientInsert, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Adicionando novo cliente ao banco de dados
        novo_cliente = models.Cliente(**cliente.dict())
        novo_cliente.criado_por = usuario_atual.id
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de inserir um novo cliente')

# Função para adquirir os dados de um cliente
@router.get('/clients/{numero_cliente}', response_model=schemas.ClientOut)
def get_one_client(numero_cliente: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando o cliente do banco de dados de acordo com o número do cliente informado
        cliente = db.query(models.Cliente).filter(models.Cliente.numero_cliente == numero_cliente).first()
        
        # Caso o número do cliente informado esteja presente no banco de dados
        if cliente != None:
            return cliente

        # Caso o número do cliente informado não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Cliente com o Número do Cliente {numero_cliente} não foi encontrado')
        
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados de um cliente')

# Função para adquirir os dados de todos cliente
@router.get('/clients', response_model=List[schemas.ClientOut])
def get_clients(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual), limite: int = 10, pular: int = 0, buscar: Optional[str] = ''):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os clientes do banco de dados de acordo com os parâmetros passados
        clientes = db.query(models.Cliente).filter(models.Cliente.nome.contains(buscar) == True).limit(limite).offset(pular).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if clientes != []:
            return clientes
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados de um cliente')
    
# Função para adquirir os dados de todos cliente
@router.get('/all-clients', response_model=List[schemas.ClientOut])
def get_all_clients(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os clientes do banco de dados de acordo com os parâmetros passados
        clientes = db.query(models.Cliente).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if clientes != []:
            return clientes
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados de um cliente')

# Função para atualizar os campos de um cliente
@router.patch('/clients/{numero_cliente}', response_model=schemas.ClientOut)
def update_client(numero_cliente: int, cliente_atualizado: schemas.ClientUpdate, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        cliente = db.query(models.Cliente).filter(models.Cliente.numero_cliente == numero_cliente).first()

        # Caso o número do cliente informado esteja presente no banco de dados
        if cliente != None:
            # Caso seja desejado atualizar o nome do cliente
            if cliente_atualizado.nome != None:
                cliente.nome = cliente_atualizado.nome
                cliente.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o cpf do cliente
            if cliente_atualizado.cpf != None:
                cliente.cpf = cliente_atualizado.cpf
                cliente.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número do cliente
            if cliente_atualizado.numero_cliente != None:
                cliente.numero_cliente = cliente_atualizado.numero_cliente
                cliente.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o nome do pai/mãe
            if cliente_atualizado.nome_pais != None:
                cliente.nome_pais = cliente_atualizado.nome_pais
                cliente.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número do RG
            if cliente_atualizado.rg != None:
                cliente.rg = cliente_atualizado.rg
                cliente.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a data de nascimento
            if cliente_atualizado.nascimento != None:
                cliente.nascimento = cliente_atualizado.nascimento
                cliente.criado_por = usuario_atual.id

            db.commit() # Atualizando as informações no banco de dados
            return cliente
        
        # Caso o número do cliente informado não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Cliente com o Número do Cliente {numero_cliente} não existe')

    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de atualizar um cliente')
    
# Função para deletar um cliente
@router.delete('/clients/{numero_cliente}', status_code=status.HTTP_204_NO_CONTENT)
def delete_client(numero_cliente: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        cliente = db.query(models.Cliente).filter(models.Cliente.numero_cliente == numero_cliente)

        # Caso o número do cliente informado esteja presente no banco de dados
        try:
            if cliente.first().nome != None:
                cliente.delete(synchronize_session=False)
                db.commit()

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Cliente com o Número do Cliente {numero_cliente} não existe')
    
    # Caso o usuário atual esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de deletar um cliente')