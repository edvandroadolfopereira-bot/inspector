# Windows MCP: spawn uv ENOENT (Server disconnected)

Este guia resolve o erro do MCP no Windows quando o cliente mostra:

- MCP Windows-MCP: spawn uv ENOENT
- MCP Windows-MCP: Server disconnected

Ele também evita os erros que acontecem quando comandos de documentação são colados no PowerShell com crases ou quando JSON é colado no terminal.

## O que aconteceu no seu PowerShell

Pelo log enviado, houve seis problemas diferentes:

1. O comando uv não está instalado ou não está no PATH.
2. Você digitou comandos com crases, por exemplo, colocando acento grave antes e depois de uv --version.
3. Você tentou executar JSON como se fosse comando de PowerShell.
4. Você tentou executar um caminho EXE entre aspas sem o operador de chamada do PowerShell.
5. O arquivo mostrou dois JSONs colados um depois do outro. Arquivo JSON válido precisa ter exatamente um objeto principal.
6. O segundo bloco apareceu com caracteres literais \n. Isso não deve existir no arquivo final.

## Regra principal: não copie crases

Quando este guia mostrar uma linha depois de COMANDO, copie somente o texto do comando.

Não copie estes caracteres:

- crase simples / acento grave antes ou depois do comando
- três crases antes ou depois do comando
- o prefixo COMANDO:
- o prompt PS C:\...>

Exemplo errado:

    `uv --version`

Exemplo certo:

    uv --version

## Passo 1 — instalar uv

No PowerShell, copie somente a linha abaixo.

COMANDO:

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Depois feche e abra o PowerShell de novo.

Se preferir instalar pelo winget, use esta alternativa.

COMANDO:

    winget install --id astral-sh.uv -e

## Passo 2 — confirmar que uv existe

No PowerShell, rode uma linha por vez.

COMANDO:

    uv --version

COMANDO:

    where.exe uv

COMANDO:

    (Get-Command uv).Source

Resultado esperado:

- uv --version deve mostrar a versão instalada.
- where.exe uv deve mostrar o caminho do uv.exe.
- (Get-Command uv).Source deve mostrar o caminho exato que deve ser usado no campo command do JSON.

Se where.exe uv não mostrar nada, o uv ainda não está no PATH. Feche e abra o PowerShell. Se continuar igual, reinicie o Windows.

## Passo 3 — se o caminho estiver entre aspas, use & antes

No PowerShell, uma string entre aspas sozinha apenas imprime o texto. Ela não executa o programa.

Errado:

    "C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Scripts\uv.exe" --version

Certo:

    & "C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Scripts\uv.exe" --version

Se você colocar crase antes do &, o PowerShell tentará executar o texto & como comando e vai falhar. Portanto, o primeiro caractere da linha deve ser exatamente &.

## Passo 4 — editar o arquivo MCP correto

JSON não é comando de PowerShell. JSON deve ser salvo em arquivo.

No seu caso, o Claude está no pacote do Windows e o caminho que você encontrou foi:

    C:\Users\edvan\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude

Então abra o arquivo correto com este comando:

COMANDO:

    notepad "C:\Users\edvan\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json"

Se você usa uma instalação não empacotada do Claude Desktop, o caminho comum é este:

COMANDO:

    notepad "$env:AppData\Claude\claude_desktop_config.json"

## Passo 4.1 — corrigir o conteúdo do JSON

O arquivo não pode ter dois blocos JSON seguidos. Apague tudo e deixe somente um objeto JSON.

Também não deixe a versão escapada com \n dentro do arquivo. Se o arquivo tiver algo parecido com `{\n"mcpServers"...`, apague essa parte.

ATENÇÃO: SEU_USUARIO é só exemplo. No seu computador, troque por edvan ou, melhor ainda, use exatamente o caminho retornado por `(Get-Command uv).Source`.

Exemplo para o seu usuário edvan se o uv estiver em `C:\Users\edvan\.local\bin\uv.exe`:

    {
      "mcpServers": {
        "windows-mcp": {
          "command": "C:\\Users\\edvan\\.local\\bin\\uv.exe",
          "args": [
            "run",
            "python",
            "C:\\caminho\\absoluto\\do\\servidor\\main.py"
          ],
          "env": {
            "PYTHONUTF8": "1"
          }
        }
      }
    }

Se `(Get-Command uv).Source` mostrar outro caminho, use esse outro caminho no campo command, sempre com barras duplicadas no JSON. Por exemplo, `C:\Users\edvan\.local\bin\uv.exe` vira `C:\\Users\\edvan\\.local\\bin\\uv.exe`.

## Passo 5 — validar se o JSON salvo está correto

No PowerShell, copie somente esta linha.

Para o seu caminho do pacote Windows:

COMANDO:

    Get-Content "C:\Users\edvan\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json | Out-Null; "JSON OK"

Para a instalação comum fora do pacote Windows:

COMANDO:

    Get-Content "$env:AppData\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json | Out-Null; "JSON OK"

Se aparecer JSON OK, o arquivo está válido.

Se aparecer erro, volte no Notepad e corrija aspas, vírgulas ou chaves.

## Passo 6 — testar o servidor MCP fora do Claude

Troque os caminhos pelos caminhos reais do seu computador.

COMANDO:

    & (Get-Command uv).Source run python "C:\caminho\absoluto\do\servidor\main.py"

Se preferir usar o caminho completo do uv.exe, o comando fica assim quando o uv estiver em `C:\Users\edvan\.local\bin\uv.exe`:

COMANDO:

    & "C:\Users\edvan\.local\bin\uv.exe" run python "C:\caminho\absoluto\do\servidor\main.py"

Se esse comando falhar, o problema ainda é no ambiente local, no uv, no Python ou no caminho do servidor.

Se esse comando funcionar, feche totalmente o Claude Desktop e abra de novo.

## Passo 7 — olhar logs

No PowerShell, copie somente esta linha.

Para o seu caminho do pacote Windows:

COMANDO:

    Get-Content "C:\Users\edvan\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\logs\mcp*.log" -Tail 80

Para a instalação comum fora do pacote Windows:

COMANDO:

    Get-Content "$env:AppData\Claude\logs\mcp*.log" -Tail 80

## Tabela de erros e correções

| Erro visto                   | Causa                               | Correção                                                   |
| ---------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| O termo uv não é reconhecido | uv não instalado ou fora do PATH    | Instale uv e reabra o PowerShell                           |
| O termo & não é reconhecido  | Você colou crase antes do &         | Digite a linha começando diretamente por &                 |
| Token ':' inesperado         | Você colou JSON no PowerShell       | Abra o JSON no Notepad e salve no arquivo de configuração  |
| Token run inesperado         | Você executou EXE entre aspas sem & | Use & antes do caminho entre aspas                         |
| spawn uv ENOENT              | O cliente MCP não achou uv          | Use caminho absoluto para uv.exe em command                |
| Dois blocos JSON no arquivo  | Conteúdo duplicado                  | Apague tudo e deixe somente um objeto JSON principal       |
| Texto com \n dentro do JSON  | JSON escapado foi colado como texto | Apague esse bloco e cole JSON normal no Notepad            |
| SEU_USUARIO no JSON          | Placeholder não foi substituído     | Troque por edvan ou pelo caminho retornado por Get-Command |

## Checklist final

- uv --version funciona sem crases.
- where.exe uv mostra o caminho do uv.exe.
- O comando com & antes do caminho do uv.exe funciona.
- O arquivo claude_desktop_config.json contém mcpServers.
- O arquivo tem apenas um objeto JSON principal.
- O arquivo não contém texto literal com \n.
- O arquivo não contém SEU_USUARIO nem caminho exemplo.
- O JSON valida com ConvertFrom-Json.
- O Claude Desktop foi fechado por completo e aberto novamente.
