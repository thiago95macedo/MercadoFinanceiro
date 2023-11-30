#!/bin/bash
# © 2023 Thiago Macêdo, WETH Systems

#--------------------------------------------------
# Definindo as variáveis de ambiente
#--------------------------------------------------

export DB_NAME='mercadofinanceiro'
export DB_USER='weth'
export DB_PASSWORD='weth1q2w3e4r'

#--------------------------------------------------
# Fazendo atualizações do sistema
#--------------------------------------------------

sudo apt-get update -y
sudo apt-get upgrade -y

#--------------------------------------------------
# Verificando e instalando o 'expect' se necessário
#--------------------------------------------------

if ! command -v expect &> /dev/null
then
    echo "O 'expect' não foi encontrado. Instalando..."
    sudo apt-get install expect -y
fi

#--------------------------------------------------
# Criando o banco de dados no PostgreSQL
#--------------------------------------------------

echo -e "\n---- Criando o banco de dados '$DB_NAME' ----"

psql -d postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

#--------------------------------------------------
# Iniciando ambiente virtual
#--------------------------------------------------
source .venv/bin/activate

#--------------------------------------------------
# Atualizando o pip e instalando as dependências
#--------------------------------------------------

pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
pip install ./dependencias/iqoptionapi
pip install ./dependencias/websocket_client
#--------------------------------------------------
# Executando as migrações do Django
#--------------------------------------------------

echo -e "\n---- Executando as migrações do Django ----"
python manage.py migrate

#--------------------------------------------------
# Iniciando o servidor Django
#--------------------------------------------------

echo -e "\n---- Iniciando o servidor Django ----"
python manage.py runserver