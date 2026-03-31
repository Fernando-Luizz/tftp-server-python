# Guia de Uso

## Requisitos

- Python 3.10 ou superior

## Instalação

Clone o repositório e instale em modo editável:

```bash
git clone <url-do-repositorio>
cd tftp-server-python
pip install -e .
```

## Iniciando o Servidor

```bash
python -m tftp_server.server --root <diretório>
```

`--root` é o diretório a partir do qual o servidor irá servir e receber arquivos. Deve ser um diretório existente.

### Opções

| Opção    | Padrão    | Descrição                                         |
|----------|-----------|---------------------------------------------------|
| `--root` | —         | **(obrigatório)** Diretório raiz para transferências |
| `--host` | `0.0.0.0` | Endereço para associar o socket UDP               |
| `--port` | `69`      | Porta UDP para escutar                            |

### Exemplos

Servir arquivos de uma pasta chamada `shared/`:

```bash
python -m tftp_server.server --root ./shared
```

Associar a uma interface específica e a uma porta não privilegiada:

```bash
python -m tftp_server.server --root ./shared --host 127.0.0.1 --port 6969
```

> **Nota:** A porta 69 (padrão do TFTP) normalmente requer privilégios de administrador/root. Use uma porta alta como `6969` para testes sem permissões elevadas.

## Testando com um Cliente TFTP

### Linux (tftp-hpa)

```bash
# instalar
sudo apt install tftp-hpa

# baixar um arquivo do servidor
tftp <ip-do-servidor> <porta>
tftp> get example.txt
tftp> quit

# enviar um arquivo para o servidor
tftp <ip-do-servidor> <porta>
tftp> put myfile.txt
tftp> quit
```

### Windows (cliente tftp nativo)

Ative o cliente TFTP em **Painel de Controle → Programas → Ativar ou desativar recursos do Windows → Cliente TFTP**, depois:

```powershell
# baixar
tftp -i <ip-do-servidor> GET example.txt

# enviar
tftp -i <ip-do-servidor> PUT myfile.txt
```

**Exemplo local (porta 69, requer prompt elevado):**

```powershell
tftp -i 127.0.0.1 GET example.txt
tftp -i 127.0.0.1 PUT myfile.txt
```

> **Nota:** O `tftp.exe` nativo não suporta portas personalizadas. Para usar a porta `6969`, utilize o [tftp64](https://sourceforge.net/projects/tftp-server/), que aceita um argumento de porta, ou inicie o servidor na porta 69 com um prompt elevado.
>
> ```powershell
> # exemplo com tftp64 na porta 6969
> tftp64 -i 127.0.0.1 -p 6969 GET example.txt
> tftp64 -i 127.0.0.1 -p 6969 PUT myfile.txt
> ```

## Estrutura do Projeto

```
src/tftp_server/
├── server.py            # Ponto de entrada
├── cli.py               # Análise de argumentos e inicialização
├── transfer_manager.py  # Máquina de estados e orquestração de transferências
├── packet_api.py        # Construção e análise de pacotes TFTP
├── udp_adapter.py       # Wrapper do socket UDP
├── file_access.py       # I/O binário de arquivos dentro do diretório raiz
└── errors.py            # Exceções compartilhadas
```

Consulte `INTERFACE.md` para os contratos entre os módulos.
