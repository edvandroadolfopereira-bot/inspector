# Windows MCP: spawn uv ENOENT (Server disconnected)

Este guia resolve o erro do MCP no Windows quando o cliente mostra:

- MCP Windows-MCP: spawn uv ENOENT
- MCP Windows-MCP: Server disconnected

Ele também evita os erros que acontecem quando comandos de documentação são colados no PowerShell com crases ou quando JSON é colado no terminal.

## O que aconteceu no seu PowerShell

Pelo log enviado, houve quatro problemas diferentes:

1. O comando uv não está instalado ou não está no PATH.
2. Você digitou comandos com crases, por exemplo, colocando acento grave antes e depois de uv --version.
3. Você tentou executar JSON como se fosse comando de PowerShell.
4. Você tentou executar um caminho EXE entre aspas sem o operador de chamada do PowerShell.

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

Resultado esperado:

- uv --version deve mostrar a versão instalada.
- where.exe uv deve mostrar o caminho do uv.exe.

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

Para Claude Desktop no Windows, abra o arquivo de configuração com este comando:

COMANDO:

    notepad "$env:AppData\Claude\claude_desktop_config.json"

Cole o conteúdo abaixo dentro do Notepad, salve e feche.

ATENÇÃO: troque SEU_USUARIO e o caminho do servidor pelos caminhos reais do seu computador.

    {
      "mcpServers": {
        "windows-mcp": {
          "command": "C:\\Users\\SEU_USUARIO\\AppData\\Local\\Programs\\Python\\Scripts\\uv.exe",
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

## Passo 5 — validar se o JSON salvo está correto

No PowerShell, copie somente esta linha.

COMANDO:

    Get-Content "$env:AppData\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json | Out-Null; "JSON OK"

Se aparecer JSON OK, o arquivo está válido.

Se aparecer erro, volte no Notepad e corrija aspas, vírgulas ou chaves.

## Passo 6 — testar o servidor MCP fora do Claude

Troque os caminhos pelos caminhos reais do seu computador.

COMANDO:

    & "C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Scripts\uv.exe" run python "C:\caminho\absoluto\do\servidor\main.py"

Se esse comando falhar, o problema ainda é no ambiente local, no uv, no Python ou no caminho do servidor.

Se esse comando funcionar, feche totalmente o Claude Desktop e abra de novo.

## Passo 7 — olhar logs

No PowerShell, copie somente esta linha.

COMANDO:

    Get-Content "$env:AppData\Claude\logs\mcp*.log" -Tail 80

## Tabela de erros e correções

| Erro visto                   | Causa                               | Correção                                                  |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------- |
| O termo uv não é reconhecido | uv não instalado ou fora do PATH    | Instale uv e reabra o PowerShell                          |
| O termo & não é reconhecido  | Você colou crase antes do &         | Digite a linha começando diretamente por &                |
| Token ':' inesperado         | Você colou JSON no PowerShell       | Abra o JSON no Notepad e salve no arquivo de configuração |
| Token run inesperado         | Você executou EXE entre aspas sem & | Use & antes do caminho entre aspas                        |
| spawn uv ENOENT              | O cliente MCP não achou uv          | Use caminho absoluto para uv.exe em command               |

## Checklist final

- uv --version funciona sem crases.
- where.exe uv mostra o caminho do uv.exe.
- O comando com & antes do caminho do uv.exe funciona.
- O arquivo claude_desktop_config.json contém mcpServers.
- O JSON valida com ConvertFrom-Json.
- O Claude Desktop foi fechado por completo e aberto novamente.
