# ⚙️ Organização e Tarefas — Equipe Servidor
**Repositório:** `tftp-server-python`  
**Objetivo:** Construir um servidor TFTP isolado, aderente à RFC 1350, capaz de atender clientes externos/nativos, com divisão de trabalho fiel aos diagramas C4 do Servidor.

---

# Diretriz Arquitetural
Este repositório representa **somente o lado Servidor** do projeto.

A organização da equipe seguirá fielmente os **3 níveis de diagramas C4** do servidor:

- **Nível 1 — Contexto:** mostra o sistema `TFTP Server Python` e suas entidades externas.
- **Nível 2 — Container:** mostra a aplicação Python do servidor e suas dependências externas.
- **Nível 3 — Componentes:** mostra as caixinhas internas do servidor, que serão implementadas separadamente pela equipe.

## Regra principal
Cada integrante será responsável por **componentes C4 específicos**.  
O código de cada pessoa deve ficar restrito à sua própria “caixinha” no diagrama de Componentes (Nível 3).

---

# Como o C4 do Servidor deve ser interpretado

## Nível 1 — Contexto
O diagrama de Contexto do Servidor deve representar:

- **Sistema principal:** `TFTP Server Python`
- **Entidade externa principal:** `Cliente TFTP Externo/Nativo`
- **Dependência externa:** `Sistema de Arquivos Local`
- **Relação principal:** troca de arquivos via protocolo TFTP

Esse nível serve para mostrar **quem interage com o servidor**.

---

## Nível 2 — Container
O diagrama de Container do Servidor deve representar:

- **Container principal:** `Aplicação Python do Servidor`
- **Dependências externas:**
  - Rede UDP
  - Sistema de Arquivos Local

Como o projeto é pequeno, o servidor pode ser representado por **um único container de aplicação**, mas ele ainda deve aparecer separado das entidades externas.

Esse nível serve para mostrar **onde o servidor roda e com o que ele se conecta**.

---

## Nível 3 — Componentes
O diagrama de Componentes do Servidor deve representar exatamente estas caixinhas internas:

- `CLI / Argument Parser`
- `Transfer Manager`
- `TFTP Packet API`
- `UDP Socket Adapter`
- `File Access`

Esse nível serve para mostrar **como o servidor foi dividido internamente**.

## Relações esperadas entre os componentes
- `CLI / Argument Parser` chama o `Transfer Manager`
- `Transfer Manager` usa `TFTP Packet API`
- `Transfer Manager` usa `UDP Socket Adapter`
- `Transfer Manager` usa `File Access`

## Relações proibidas
- `UDP Socket Adapter` não deve conter lógica de protocolo
- `File Access` não deve conter lógica de protocolo
- `TFTP Packet API` não deve acessar rede
- `TFTP Packet API` não deve acessar disco
- `CLI / Argument Parser` não deve montar pacotes nem ler/gravar arquivos diretamente

---

# Papéis e Responsabilidades da Equipe Servidor

## 1. FERNANDO — Arquiteto e Revisor (Dono do Repositório)
### Responsabilidade C4
Responsável por modelar e defender a arquitetura do Servidor nos 3 níveis do C4:

- **Nível 1 — Contexto**
- **Nível 2 — Container**
- **Nível 3 — Componentes**

### Componentes sob sua responsabilidade
- `CLI / Argument Parser`
- `Bootstrap / Inicialização do Servidor`

### Entregáveis
- Criar e subir o repositório `tftp-server-python`
- Criar a pasta `docs/c4/`
- Desenhar os diagramas:
  - `nivel-1-contexto.drawio`
  - `nivel-2-container.drawio`
  - `nivel-3-componentes.drawio`
- Subir a estrutura base de pastas e arquivos
- Criar o `INTERFACE.md`
- Criar o `README.md`
- Criar o `server.py` como entry point
- Criar o `cli.py` para leitura de argumentos e inicialização
- Subir os arquivos dos colegas como stubs vazios ou com assinatura inicial

### Responsabilidade de revisão
Você aprova exclusivamente os Pull Requests do:

- **Colega 2**
- **Colega 3**

### Critérios de revisão
Ao revisar os PRs, você deve verificar se:

- cada pessoa implementou apenas sua própria caixinha;
- o código continua fiel ao diagrama C4 Nível 3;
- `server.py` continua sendo apenas bootstrap;
- ninguém misturou lógica de rede, protocolo e disco no mesmo componente.

### Não deve implementar
- parsing binário de pacotes;
- máquina de estados da transferência;
- lógica bruta de socket;
- leitura e gravação direta de arquivos fora do bootstrap.

---

## 2. [Nome] — Desenvolvedor Core
### Componentes C4 sob responsabilidade
- `TFTP Packet API`
- `Transfer Manager`

### Entregáveis
- Implementar a montagem e desmontagem dos pacotes TFTP
- Validar opcodes
- Implementar a máquina de estados do servidor
- Orquestrar o fluxo de:
  - `RRQ`
  - `WRQ`
  - `DATA`
  - `ACK`
  - `ERROR`
- Integrar o fluxo com rede e disco **sem implementar rede e disco diretamente**

### Responsabilidade do componente `TFTP Packet API`
Esse componente deve conter apenas:
- builders de pacotes;
- parsers de pacotes;
- validação de formato;
- serialização/deserialização com `struct`.

### O que `TFTP Packet API` não deve fazer
- abrir socket;
- enviar pacote pela rede;
- abrir arquivo;
- decidir fluxo da aplicação;
- conter lógica de CLI.

### Responsabilidade do componente `Transfer Manager`
Esse componente deve conter apenas:
- máquina de estados do servidor;
- decisão de fluxo da transferência;
- coordenação entre protocolo, rede e disco;
- controle da ordem dos pacotes;
- decisão de quando enviar `ACK`, `DATA` ou `ERROR`.

### O que `Transfer Manager` não deve fazer
- usar `open()` diretamente;
- implementar `bind`, `recvfrom` ou `sendto`;
- usar `struct` espalhado no fluxo principal;
- assumir responsabilidade de CLI.

---

## 3. [Nome] — Engenheiro de Redes e Testes
### Componentes C4 sob responsabilidade
- `UDP Socket Adapter`
- `File Access`

### Entregáveis
- Implementar a camada de socket UDP
- Implementar:
  - `bind`
  - `recvfrom`
  - `sendto`
  - timeout
- Implementar leitura de arquivo para envio
- Implementar gravação de arquivo recebido
- Garantir acesso restrito à pasta local do servidor
- Fazer testes com cliente externo/nativo
- Gerar evidências visuais para o README

### Responsabilidade do componente `UDP Socket Adapter`
Esse componente deve conter apenas:
- abertura e fechamento do socket;
- envio bruto de bytes;
- recebimento bruto de bytes;
- configuração de timeout.

### O que `UDP Socket Adapter` não deve fazer
- interpretar opcode;
- decidir quando enviar `ACK`, `DATA` ou `ERROR`;
- abrir arquivo;
- conhecer a máquina de estados.

### Responsabilidade do componente `File Access`
Esse componente deve conter apenas:
- leitura de arquivo em modo binário;
- gravação de arquivo em modo binário;
- validação de caminho;
- isolamento da pasta base do servidor.

### O que `File Access` não deve fazer
- montar pacote TFTP;
- acessar socket;
- decidir fluxo do protocolo.

### Prova de interoperabilidade
Esse integrante é responsável por:
- testar o servidor com cliente TFTP externo/nativo;
- gerar prints para o README;
- comprovar que a borda do sistema está funcional.

---

# Regras (Limites dos Componentes)

## CLI / Argument Parser
Pode:
- usar `argparse`
- validar parâmetros de entrada
- iniciar o fluxo da aplicação

NÃO PODE:
- abrir socket
- ler ou gravar arquivo
- montar ou interpretar pacotes TFTP

## Transfer Manager
Pode:
- ditar a ordem dos pacotes
- controlar a máquina de estados
- decidir quando chamar rede, disco e Packet API
- coordenar o fluxo de RRQ, WRQ, DATA, ACK e ERROR

NÃO PODE:
- fazer chamada de rede direta (`sendto`, `recvfrom`, `bind`)
- abrir arquivo diretamente
- manipular bytes com `struct` por conta própria

## TFTP Packet API
Pode:
- usar `struct` para montar e desmontar pacotes
- validar opcode e formato dos pacotes
- transformar bytes em estruturas de protocolo e vice-versa

NÃO PODE:
- tomar decisões de negócio
- controlar o fluxo da transferência
- acessar disco
- acessar socket

## UDP Socket Adapter
Pode:
- abrir/configurar socket
- fazer `bind`, `recvfrom`, `sendto`
- controlar timeout

NÃO PODE:
- interpretar opcode
- conhecer regras de TFTP
- decidir quando enviar ACK, DATA ou ERROR
- acessar disco

## File Access
Pode:
- ler e gravar arquivos em disco
- validar caminhos
- restringir acesso à pasta base

NÃO PODE:
- saber o que é ACK, DATA, RRQ ou WRQ
- interpretar pacote
- acessar socket
- decidir fluxo do protocolo

---

# Estrutura de Pastas do Repositório
> O Arquiteto/Revisor sobe essa estrutura inicialmente com arquivos vazios ou com stubs.

```text
tftp-server-python/
├─ docs/
│  └─ c4/
│     ├─ nivel-1-contexto.drawio
│     ├─ nivel-2-container.drawio
│     └─ nivel-3-componentes.drawio
├─ INTERFACE.md
├─ README.md
├─ src/
│  └─ tftp_server/
│     ├─ __init__.py
│     ├─ server.py
│     ├─ cli.py
│     ├─ transfer_manager.py
│     ├─ packet_api.py
│     ├─ udp_adapter.py
│     ├─ file_access.py
│     └─ errors.py
└─ tests/
   ├─ unit/
   └─ integration/
