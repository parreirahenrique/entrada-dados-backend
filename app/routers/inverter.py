from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Inverters']
)

# Função para inserir um novo inversor
@router.post('/inverters', status_code=status.HTTP_201_CREATED, response_model=schemas.InverterOut)
def create_inverter(inversor_inserido: schemas.InverterInsert, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Adicionando novo inversor ao banco de dados
        inversores = db.query(models.Inversor).all()

        # Determinando a maior ID dentro dos inversores
        id_max: int = 0
        for inversor in inversores:
            if inversor.id > id_max:
                id_max = inversor.id

        novo_inversor = models.Inversor(**inversor_inserido.dict())
        novo_inversor.criado_por = usuario_atual.id
        novo_inversor.id = id_max + 1
        db.add(novo_inversor)
        db.commit()
        db.refresh(novo_inversor)
        return novo_inversor
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de inserir um novo inversor')
    
# Função para adquirir os dados de um inversor
@router.get('/inverters/{id}', response_model=schemas.InverterOut)
def get_one_inverter(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando o inversor do banco de dados de acordo com a ID informada
        inversor = db.query(models.Inversor).filter(models.Inversor.id == id).first()
        
        # Caso a ID informada esteja presente no banco de dados
        if inversor != None:
            return inversor

        # Caso a ID informada não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Inversor com a ID {id} não foi encontrado')
        
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir as informações de um inversor')
    
# Função para adquirir os dados de todos inversores
@router.get('/inverters', response_model=List[schemas.InverterOut])
def get_inverters(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual), limite: int = 10, pular: int = 0, buscar: Optional[str] = ''):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os inversores do banco de dados de acordo com os parâmetros passados
        inversores = db.query(models.Inversor).filter(models.Inversor.modelo.contains(buscar) == True).limit(limite).offset(pular).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if inversores != []:
            return inversores
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir os dados dos inversores')
    
# Função para adquirir os dados de todos inversores
@router.get('/all-inverters', response_model=List[schemas.InverterOut])
def get_inverters(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os inversores do banco de dados de acordo com os parâmetros passados
        inversores = db.query(models.Inversor).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if inversores != []:
            return inversores
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir os dados dos inversores')
        
# Função para adquirir os dados de todos inversores de um fabricante
@router.get('/inverters-{fabricante}', response_model=List[schemas.InverterOut])
def get_inverters(fabricante: str, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando os inversores do banco de dados de acordo com os parâmetros passados
        inversores = db.query(models.Inversor).filter(models.Inversor.fabricante.contains(fabricante) == True).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if inversores != []:
            return inversores
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir os dados dos inversores')
    
# Função para atualizar os campos de um inversor
@router.patch('/inverters/{id}', response_model=schemas.InverterOut)
def update_inverter(id: int, inversor_atualizado: schemas.InverterUpdate, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        inversor = db.query(models.Inversor).filter(models.Inversor.id == id).first()

        # Caso a ID informada esteja presente no banco de dados
        if inversor != None:
            # Caso seja desejado atualizar o modelo
            if inversor_atualizado.modelo != None:
                inversor.modelo = inversor_atualizado.modelo
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o fabricante
            if inversor_atualizado.fabricante != None:
                inversor.fabricante = inversor_atualizado.fabricante
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a potência
            if inversor_atualizado.potencia != None:
                inversor.potencia = inversor_atualizado.potencia
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a potência
            if inversor_atualizado.overload != None:
                inversor.overload = inversor_atualizado.overload
                inversor.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar a corrente no ponto de máxima potência
            if inversor_atualizado.imp != None:
                inversor.imp = inversor_atualizado.imp
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a corrente de curto circuito
            if inversor_atualizado.isc != None:
                inversor.isc = inversor_atualizado.isc
                inversor.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar a tensão no ponto de máxima potência
            if inversor_atualizado.v_min_mppt != None:
                inversor.v_min_mppt = inversor_atualizado.v_min_mppt
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a tensão no ponto de máxima potência
            if inversor_atualizado.v_max_mppt != None:
                inversor.v_max_mppt = inversor_atualizado.v_max_mppt
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a tensão de circuito aberto
            if inversor_atualizado.v_max != None:
                inversor.v_max = inversor_atualizado.v_max
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número de MPPTs
            if inversor_atualizado.n_mppt != None:
                inversor.n_mppt = inversor_atualizado.n_mppt
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número de entradas
            if inversor_atualizado.n_entrada != None:
                inversor.n_entrada = inversor_atualizado.n_entrada
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a tensão de saída
            if inversor_atualizado.v_saida != None:
                inversor.v_saida = inversor_atualizado.v_saida
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a corrente de saída
            if inversor_atualizado.i_saida != None:
                inversor.i_saida = inversor_atualizado.i_saida
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o comprimento
            if inversor_atualizado.comprimento != None:
                inversor.comprimento = inversor_atualizado.comprimento
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a largura
            if inversor_atualizado.largura != None:
                inversor.largura = inversor_atualizado.largura
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a espessura
            if inversor_atualizado.espessura != None:
                inversor.espessura = inversor_atualizado.espessura
                inversor.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a eficiência
            if inversor_atualizado.eficiencia != None:
                inversor.eficiencia = inversor_atualizado.eficiencia
                inversor.criado_por = usuario_atual.id
            
            db.commit() # Atualizando as informações no banco de dados
            return inversor
        
        # Caso a ID informada não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Inversor com a ID {id} não existe')

    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de atualizar um inversor')
    
# Função para deletar um inversor
@router.delete('/inverters/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_inverter(id: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        inversor = db.query(models.Inversor).filter(models.Inversor.id == id)
        
        # Caso a ID informada esteja presente no banco de dados
        try:
            if inversor.first().id != None:
                inversor.delete(synchronize_session=False)
                db.commit()

        # Caso a ID informada não esteja presente no banco de dados
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Inversor com a ID {id} não existe')
    
    # Caso o usuário atual esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de deletar um inversor')