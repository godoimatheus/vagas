# Site de empregos

Este é um projeto de um site de empregos construído com Django. O objetivo do site é permitir que empresas cadastrem vagas de emprego e candidatos possam se candidatar a essas vagas.

## Funcionalidades

O site possui as seguintes funcionalidades:

### Para Empresas

- Cadastro e autenticação de empresas;
- Cadastro, edição e exclusão de vagas de emprego;
- Visualização das candidaturas recebidas para cada vaga;
- Detalhes das vagas cadastradas.

### Para Candidatos

- Cadastro e autenticação de candidatos;
- Visualização das vagas de emprego disponíveis;
- Candidatura a vagas;
- Detalhes das vagas em que o candidato se candidatou.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter os seguintes pré-requisitos instalados:

- Python (versão 3.x)
- Django (versão 4.x)
- Git

## Instalação e configuração

Clone o repositório para o seu computador:

`git clone https://github.com/godoimatheus/vagas.git`

Crie um ambiente virtual (opcional, mas recomendado):

`python -m venv venv`

Ative o ambiente virtual (opcional):

- Windows

  `venv\Scripts\activate`

- macOS/Linux

  `source venv/bin/activate`

Instale as dependências:

`pip install -r requirements.txt`

Configure o banco de dados:

>O projeto está configurado para usar o banco de dados SQLite por padrão. Se desejar usar outro banco de dados (por exemplo, MySQL ou PostgreSQL), modifique as configurações no arquivo **settings.py**.

Realize as migrações:

> Certifique-se que esteja na pasta que contenha o arquivo **manage.py** antes de realizar os seguintes comandos. Usando o comando `ls` no terminal podemos ver os arquivos do diretório atual, para acessar a pasta onde o arquivo **manage.py** se localiza, basta usar `cd projeto_vagas`, se quiser ter certeza de que está no diretório correto pode-se usar novamente o comando `ls`.

`python manage.py migrate`

Crie um superusuário (administrador):

`python manage.py createsuperuser`

Rode o servidor:

`python manage.py runserver`

O site estará disponível em http://localhost:8000/.
