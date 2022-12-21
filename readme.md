# FUNDAMENTOS DE SISTEMAS EMBARCADOS - PROJETO 1

## Configuração

### Conectando-se ao servidor central

Primeiro, deve-se configurar o servidor central. Para isso, basta executar: 

```
    ssh enzosaraiva@164.41.98.26 -p 13508
```

Senha para acesso: 160119006

Após o acesso, entre do diretório onde se encontra o código fonte do projeto para o servidor central através do comando:

```
    cd fse_trabalho_01/central_server
```
### Conectando-se aos servidores distribuídos

Para conectar os servidores distribuídos, é necessário a criação da instância de mais um terminal para cada servidor distribuído que irá acessar o servidor central. 
Com uma nova instância do terminal aberta (mantendo o terminal do servidor central em execução) acesse a placa que irá executar o servidor distribuído através do comando: 

```
    ssh enzosaraiva@164.41.98.15 -p 13508
```
Senha para acesso: 160119006


Após o acesso, entre do diretório onde se encontra o código fonte do projeto para o servidor distribuído através do comando:
​
```
    cd fse_trabalho_01/distributed_server
```
# Execução
​
### Servidor Central
​
Para rodar o projeto completo, primeiro deve-se executar o servidor central. Entre na aba do terminal onde foi configurado o servidor central, e execute o comando: 

```
    python3 main.py
```

Após isso, apareerá o seguinte menu no terminal do servidor central:

Enquanto isso, no terminal do servidor distribuído, execute o comando:

```
    python3 main.py
```

Com isso, a conexão tcp ip entre os servidores será feita automaticamente.

Em seguida, o usuário tem a liberdade para utilizar qualquer um dos comandos presentes no menu do servidor central