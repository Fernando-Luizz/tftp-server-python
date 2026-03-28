# Interface entre módulos

Referência para implementação alinhada ao C4 nível 3 e às regras do `Tasks.md`.

## `server.py`

Chama `cli.main()`. Sem TFTP, rede ou disco.

## `cli.py`

Argumentos: `--host` (default `0.0.0.0`), `--port` (default `69`), `--root` (diretório existente). Resolve `root` e chama `transfer_manager.serve(bind_host, port, root_dir)`.

Não importa `packet_api`, `udp_adapter` nem `file_access`. Não abre socket nem arquivo.

## `transfer_manager.py`

`serve(bind_host: str, port: int, root_dir: Path) -> None`: máquina de estados e orquestração RRQ, WRQ, DATA, ACK, ERROR.

Usa `packet_api` para bytes de protocolo, `UdpSocketAdapter` para datagramas, `FileAccess` para disco. Não usa `struct` fora do packet API; não chama `bind`, `recvfrom`, `sendto`, `open` diretamente.

## `packet_api.py`

Montagem, parsing e validação de pacotes TFTP com `struct`. Sem socket e sem filesystem.

## `udp_adapter.py`

`UdpSocketAdapter`: `bind`, `recvfrom`, `sendto`, timeout e fecho. Só bytes UDP; sem opcode TFTP e sem arquivo.

## `file_access.py`

`FileAccess(root)`: leitura/gravação binária, validação de caminho sob `root`. Sem pacotes TFTP e sem socket.

## `errors.py`

Exceções e constantes de erro partilhadas quando o transfer manager e o packet API precisarem do mesmo contrato.
