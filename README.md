# Trabalho Final - Sistemas Distribuidos e Mobile

Esta página apresenta uma simples aplicação Flask, que deve ser conteinerizada,e esta possui o banco de dados (relacional) desacoplado do serviço web.

O Objetivo dela é você criar suas tarefas, organizar e marcar como concluidas, alem de que se você criou alguma errada você pode excluir sem nenhum problema.

Alunos envolvidos Arthur Marcio Brasil - RA .... e Vitor Alexandrino de Melo - RA 320140534


## Organização do projeto

* static: contém arquivos estáticos, por exemplo, arquivos de estilos .css.
* templates: contém todos os templates usando a engine Jinja. Veja *https://flask.palletsprojects.com/en/2.2.x/templating/* para mais detalhes.
* app: A aplicação Flask, arquivo .sql: contém o esquema para criar o banco (Postgres)


**Atenção**, prepare o projeto para compilação/execução. No diretório do projeto:

1. crie um ambiente virtual: `python3 -m venv env`. Esse comando cria um ambiente chamado *env*. Pesquise sobre ambientes virtuais no python.
2. crie um arquivo .env contendo as variáveis de ambiente: **SESSION_SECRET_KEY_DEV** e uma string hexadecimal como valor (use o *python secrets*), **DB_USERNAME=postgres** e **DB_PASSWORD=admin123**. As duas últimas variáveis de ambiente, usaremos na definição no banco. Este arquivo terá somente três linhas, da seguinte maneira: *SESSION_SECRET_KEY_DEV='string-gerada-pelo-python-secrets'*
*DB_USERNAME=postgres*
*DB_PASSWORD=admin123*
3. crie o arquivo *.config.py* e carregue o *.env*. Este arquivo conterá a linha de import `from dotenv import load_dotenv` e a linha `load_dotenv()`.

## (2) Interagindo com a aplicação localmente

Para executar a aplicação, temos que colocar o Flask para execução, e configurar o Banco.

- No diretório do projeto, digite para:
   1. Carregar o ambiente desta aplicação: `source env/bin/activate`
   2. Instalar os pacotes necessários: `pip install -r requirements.txt`

- Para desativar o ambiente, digite `deactivate`.

Recomendamos fortemente a utilização do github codespaces para essa atividade porque por algum motivo o vscode não reconheceu o flask na maquina de um dos integrantes, e o requirements.txt vai garantir isso

## (3) Docker

- Instale o docker em sua máquina local (virtual). 

- Os comandos Docker que mais usaremos são:
   - sudo docker image build -t image-name .
   - sudo docker image ls
   - sudo docker container ls -a
   - sudo docker container ps
   - sudo docker run [OPTIONS] image-name (ou image-id)
   - sudo docker stop (ou start) image-name (ou image-id)
   - sudo docker rm image-name (ou image-id)
   - sudo docker image rm image-name (ou image-id)

A Partir daqui, se estiver usando o github codespace você pode executar os comandos...

- Para esta prática, iremos construir três imagens: Blog (Flask), Postgres e PgAdmin (gerenciador do banco).

   1. `docker pull postgres`
   2. `docker pull dpage/pgadmin4`

Após a execução desses dois comandos, as duas imagens *postgres* e *pgadmin* estão disponíveis. 

   3. Criar uma rede própria para os conteineres: `docker network create --driver bridge postgres-network`
   4. Certifique de que a rede foi criada: `docker network ls`

Agora, iremos construir os conteineres, um para cada imagem criada.

   5. `docker run --name postgresql --network=postgres-network -e "POSTGRES_PASSWORD=admin123" -p 5432:5432 -d postgres`

Criamos um conteiner chamado *postgresql*, o colocamos na rede criada, configuramos a porta local 5432 na máquina local, que será mapeada para a porta 5432 do conteiner, além de configurar a senha *admin123* para o usuário padrão *postgres*.

O próximo comando precisa de um e-mail válido, apenas para criar o usuário para o gerenciador do banco.

   6. `docker run --name pgadmin4 --network=postgres-network -p 15432:80 -e "PGADMIN_DEFAULT_EMAIL=teste@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=admin123" -e PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1 -e PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1 -d dpage/pgadmin4`

Criamos um conteiner chamado *pgadmin4*, o colocamos na mesma rede criada do postgres, configuramos a porta local 15432 na máquina local, que será mapeada para a porta 80 do conteiner, já que o acesso é via http, além de configurar a senha *admin123* para o usuário criado, cujo *login* é o email informado.

A partir desse momento, o banco pode ser acessado. Vamos fazer um pequeno teste de acesso ao banco (conteiner postgresql).

   7. `docker exec -it id-do-container-postgres bash`

O acesso ao container foi concedido.

   8. `psql -U postgres`

O acesso ao banco foi concedido, por meio do usuário *postgres*. Acesse o link *https://dbschema.com/2020/04/14/postgresql-show-tables/* para alguns comandos de manipulação do postgres via terminal. Dê atenção aos comandos *\l*, *\c database-name*, *\dt*. Utilize esses comandos apenas para conferir o banco. Não iremos gerenciá-lo via terminal, mas pelo pgadmin. 

   9. Acesse *localhost:15432* na máquina local, via browser.
   10. Faça o *login* com o usuário e a senha criada para o pgadmin. Efetuada a autenticação, teremos então o painel principal, com as funcionalidades que permitirão o gerenciamento de servidores e bases de dados.
   11. Não há servidor cadastrado. Registre um servidor e informe os seguintes parâmetros de conexão: 
      a. Na aba *General* informar a identificação (*Name*) da conexão.
      b. Na aba *Connection*, informe o *hostname: postgresql*, *Port: 5432*, *Username: postgres* e *Password: admin123*. Marque para deixar a senha salva.

Assim o gerenciador já está conectado ao postgres, isto é, dois conteineres estão se comunicando. Agora vamos criar um banco para a aplicação.

   12. No menu clique em *Object -> Create -> Database*. Dê um nome ao banco tasks, com o usuário *postgres* como o dono.
   13. Na lateral, clique sobre o nome do banco criado, e em seguida, no menu, clique em *Tools -> Query Tool*. Isso abre o gerenciador de queries.
   14. Acesse o arquivo *schema_posgres.sql* do projeto. Execute cada comando, *DROP* e *CREATE* juntos (copie, cole e execute), em seguida os comandos *INSERT*. Isso cria a tabela e registros. Você pode conferir fazendo o *SELECT* no banco. Se quiser, confira via conteiner, conforme o **passo 8**.

Antes de executar nossa aplicação, no terminal, execute o comando `pip install psycopg2`, pois ele é um adaptador necessário para essa aplicação para fazer a comunicação entre o python e o postgreSQL

Agora, basta executar nossa aplicação Flask, que já está configurada para acessar o banco. 

   15. Execute o arquivo *app.py*
   16. Acesse o endereço localhost na porta 5000 (localhost:5000) para visualizar a aplicação.

Realize todas as operações CRUD normalmente como um usuário normal!!

Fimmmmmmmm
