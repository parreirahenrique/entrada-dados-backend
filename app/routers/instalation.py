from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Instalations']
)

# Função para inserir uma nova instalação
@router.post('/instalations', response_model=schemas.InstalationOut)
def create_instalation(instalacao: schemas.InstalationInsert, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Adicionando novo cliente ao banco de dados
        if instalacao.numero_instalacao == 0:
            # Determinando um número de instalação fictício para as ligações novas
            instalacoes = db.query(models.Instalacao).all()
            id_max: int = 0
            
            for i in instalacoes:
                if i.numero_instalacao > id_max and i.numero_instalacao < 3000000000:
                    id_max = i.numero_instalacao

            instalacao.numero_instalacao = id_max + 1

        nova_instalacao = models.Instalacao(**instalacao.dict())
        nova_instalacao.criado_por = usuario_atual.id
        db.add(nova_instalacao)
        db.commit()
        db.refresh(nova_instalacao)
        return nova_instalacao
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de inserir uma nova instalação')
    
# Função para adquirir os dados de um cliente
@router.get('/instalations/{numero_instalacao}', response_model=schemas.InstalationOut)
def get_one_instalation(numero_instalacao: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando a instalação do banco de dados de acordo com o número de instalação informado
        instalacao = db.query(models.Instalacao).filter(models.Instalacao.numero_instalacao == numero_instalacao).first()
        
        # Caso o número de instalação informado esteja presente no banco de dados
        if instalacao != None:
            return instalacao

        # Caso o número de instalação informado não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Instalação com o Número de Instalação {numero_instalacao} não foi encontrada')
        
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de inserir um novo cliente')
    
# Função para adquirir os dados de todas instalações
@router.get('/instalations', response_model=List[schemas.InstalationOut])
def get_instalations(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual), limite: int = 10, pular: int = 0, buscar: Optional[str] = ''):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando as instalações do banco de dados de acordo com os parâmetros passados
        instalacoes = db.query(models.Instalacao).filter(models.Instalacao.logradouro.contains(buscar) == True).limit(limite).offset(pular).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if instalacoes != []:
            return instalacoes
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir os dados das intalações')

# Função para adquirir os dados de todas instalações
@router.get('/all-instalations', response_model=List[schemas.InstalationOut])
def get_instalations(db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        # Filtrando as instalações do banco de dados de acordo com os parâmetros passados
        instalacoes = db.query(models.Instalacao).all()
        
        # Caso os parâmetros de busca tenham sido válidos
        if instalacoes != []:
            return instalacoes
        
        # Caso os parâmetros de busca não tenham sido válidos
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Parâmetros de busca passados não exibiram nenhum resultado')
    
    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de adquirir os dados das intalações')
    
# Função para atualizar os campos de uma instalação
@router.patch('/instalations/{numero_instalacao}', response_model=schemas.InstalationOut)
def update_instalation(numero_instalacao: int, instalacao_atualizada: schemas.InstalationUpdate, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        instalacao = db.query(models.Instalacao).filter(models.Instalacao.numero_instalacao == numero_instalacao).first()

        # Caso o número do cliente informado esteja presente no banco de dados
        if instalacao != None:
            # Caso seja desejado atualizar o logradouro
            if instalacao_atualizada.logradouro != None:
                instalacao.logradouro = instalacao_atualizada.logradouro
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número predial
            if instalacao_atualizada.numero_predial != None:
                instalacao.numero_predial = instalacao_atualizada.numero_predial
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o complemento
            if instalacao_atualizada.complemento != None:
                instalacao.complemento = instalacao_atualizada.complemento
                instalacao.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar o bairro
            if instalacao_atualizada.bairro != None:
                instalacao.bairro = instalacao_atualizada.bairro
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a cidade
            if instalacao_atualizada.cidade != None:
                instalacao.cidade = instalacao_atualizada.cidade
                instalacao.criado_por = usuario_atual.id
            
            # Caso seja desejado atualizar o CEP
            if instalacao_atualizada.cep != None:
                instalacao.cep = instalacao_atualizada.cep
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número da instalação
            if instalacao_atualizada.numero_instalacao != None:

                # Caso não tenha sido informado um número de instalação para os casos de ligação nova
                if instalacao_atualizada.numero_instalacao == 0:
                    # Determinando um número de instalação fictício para as ligações novas
                    instalacoes = db.query(models.Instalacao).all()
                    id_max: int = 0
            
                    for i in instalacoes:
                        if i.numero_instalacao > id_max and i.numero_instalacao < 3000000000:
                            id_max = i.numero_instalacao
                            
                    instalacao.numero_instalacao = id_max + 1
                
                # Caso tenha sido informado um número de instalação
                elif instalacao_atualizada.numero_instalacao != 0:
                    instalacao.numero_instalacao = instalacao_atualizada.numero_instalacao
                    instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar o número do cliente
            if instalacao_atualizada.numero_cliente != None:
                instalacao.numero_cliente = instalacao_atualizada.numero_cliente
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a classificação
            if instalacao_atualizada.classificacao != None:
                instalacao.classificacao = instalacao_atualizada.classificacao
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a latitude
            if instalacao_atualizada.latitude != None:
                instalacao.latitude = instalacao_atualizada.latitude
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar a longitude
            if instalacao_atualizada.longitude != None:
                instalacao.longitude = instalacao_atualizada.longitude
                instalacao.criado_por = usuario_atual.id

            # Caso seja desejado atualizar as coordenadas decimais
            if instalacao_atualizada.coordenadas_decimais != None:
                instalacao.coordenadas_decimais = instalacao_atualizada.coordenadas_decimais
                instalacao.criado_por = usuario_atual.id

            db.commit() # Atualizando as informações no banco de dados
            return instalacao
        
        # Caso o número do cliente informado não esteja presente no banco de dados
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Instalação com o Número de Instalação {numero_instalacao} não existe')

    # Caso o usuário atual não esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de atualizar uma instalação')
    
# Função para deletar uma instalação
@router.delete('/instalations/{numero_instalacao}', status_code=status.HTTP_204_NO_CONTENT)
def delete_instalation(numero_instalacao: int, db: Session = Depends(get_db), usuario_atual: models.Usuario = Depends(oauth2.determinar_usuario_atual)):
    # Caso o usuário atual esteja validado
    if usuario_atual != None:
        instalacao = db.query(models.Instalacao).filter(models.Instalacao.numero_instalacao == numero_instalacao)
        
        # Caso o número da instalação informado esteja presente no banco de dados
        try:
            if instalacao.first().numero_instalacao != None:
                instalacao.delete(synchronize_session=False)
                db.commit()

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Instalação com o Número de Instalação {numero_instalacao} não existe')
    
    # Caso o usuário atual esteja validado
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Por favor, faça login antes de deletar uma instalação')