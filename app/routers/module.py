from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Modules']
)

# Função para inserir um novo módulo
@router.post('/modules', status_code=status.HTTP_201_CREATED, response_model=schemas.ModuleOut)
def create_module(modulo_inserido: schemas.ModuleInsert, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Adicionando novo módulo ao banco de dados
        modulos = db.query(models.Modulo).all()

        # Determinando a maior ID dentro dos módulos
        id_max = 0
        for modulo in modulos:
            if modulo.id > id_max:
                id_max = modulo.id

        novo_modulo = models.Modulo(**modulo_inserido.dict())
        novo_modulo.criado_por = usuario_atual.id
        novo_modulo.id = id_max + 1
        db.add(novo_modulo)
        db.commit()
        db.refresh(novo_modulo)
        return novo_modulo
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de inserir um novo módulo')
    
# Função para adquirir os dados de um cliente
@router.get('/modules/{id}', response_model=schemas.ModuleOut)
def get_one_module(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando o módulo do banco de dados de acordo com a ID informada
        modulo = db.query(models.Modulo).filter(models.Modulo.id == id).first()
        
        # Caso a ID informada esteja presente no banco de dados
        if modulo != None:
            return modulo

        # Caso a ID informada não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Módulo com a ID {id} não foi encontrado')
        
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir as informações de um módulo')
    
# Função para adquirir os dados de todos módulos
@router.get('/modules', response_model=List[schemas.ModuleOut])
def get_modules(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual), limite: int = 10, pular: int = 0, buscar: Optional[str] = ''):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os módulos do banco de dados de acordo com os parâmetros passados
        modules = db.query(models.Modulo).filter(models.Modulo.modelo.contains(buscar) == True).limit(limite).offset(pular).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if modules != []:
            return modules
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados dos módulos')

# Função para adquirir os dados dos módulos de um fabricante
@router.get('/modules-{fabricante}', response_model=List[schemas.ModuleOut])
def get_modules(fabricante: str, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os módulos do banco de dados de acordo com os parâmetros passados
        modules = db.query(models.Modulo).filter(models.Modulo.fabricante.contains(fabricante) == True).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if modules != []:
            return modules
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados dos módulos')

# Função para adquirir os dados de todos módulos
@router.get('/all-modules', response_model=List[schemas.ModuleOut])
def get_all_modules(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os módulos do banco de dados de acordo com os parâmetros passados
        modules = db.query(models.Modulo).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if modules != []:
            return modules
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de adquirir os dados dos módulos')
    
# Função para atualizar os campos de uma instalação
@router.patch('/modules/{id}', response_model=schemas.ModuleOut)
def update_instalation(id: int, modulo_atualizado: schemas.ModuleUpdate, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        modulo = db.query(models.Modulo).filter(models.Modulo.id == id).first()

        # Caso a ID informada esteja presente no banco de dados
        if modulo != None:
            # Caso seja desejado atualizar o modelo
            if modulo_atualizado.modelo != None:
                modulo.modelo = modulo_atualizado.modelo
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o fabricante
            if modulo_atualizado.fabricante != None:
                modulo.fabricante = modulo_atualizado.fabricante
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a potência
            if modulo_atualizado.potencia != None:
                modulo.potencia = modulo_atualizado.potencia
                modulo.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar a corrente no ponto de máxima potência
            if modulo_atualizado.imp != None:
                modulo.imp = modulo_atualizado.imp
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a corrente de curto circuito
            if modulo_atualizado.isc != None:
                modulo.isc = modulo_atualizado.isc
                modulo.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar a tensão no ponto de máxima potência
            if modulo_atualizado.vmp != None:
                modulo.vmp = modulo_atualizado.vmp
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a tensão de circuito aberto
            if modulo_atualizado.voc != None:
                modulo.voc = modulo_atualizado.voc
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o comprimento
            if modulo_atualizado.comprimento != None:
                modulo.comprimento = modulo_atualizado.comprimento
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a largura
            if modulo_atualizado.largura != None:
                modulo.largura = modulo_atualizado.largura
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a espessura
            if modulo_atualizado.espessura != None:
                modulo.espessura = modulo_atualizado.espessura
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a eficiência
            if modulo_atualizado.eficiencia != None:
                modulo.eficiencia = modulo_atualizado.eficiencia
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a temperatura nominal
            if modulo_atualizado.temperatura_nominal != None:
                modulo.temperatura_nominal = modulo_atualizado.temperatura_nominal
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o tipo
            if modulo_atualizado.tipo != None:
                modulo.tipo = modulo_atualizado.tipo
                modulo.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o coeficiente de temperatura
            if modulo_atualizado.coeficiente_temperatura != None:
                modulo.coeficiente_temperatura = modulo_atualizado.coeficiente_temperatura
                modulo.criado_por = usuario_atual.id

            db.commit() # Atualizando as informações no banco de dados
            return modulo
        
        # Caso a ID informada não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Módulo com a ID {id} não existe')

    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de atualizar um módulo')
    
# Função para deletar uma instalação
@router.delete('/modules/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_instalation(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        modulo = db.query(models.Modulo).filter(models.Modulo.id == id)
        
        # Caso a ID informada esteja presente no banco de dados
        try:
            if modulo.first().id != None:
                modulo.delete(synchronize_session=False)
                db.commit()

        # Caso a ID informada não esteja presente no banco de dados
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Módulo com a ID {id} não existe')
    
    # Caso o usuário atual esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Por favor, faça login antes de deletar um módulo')