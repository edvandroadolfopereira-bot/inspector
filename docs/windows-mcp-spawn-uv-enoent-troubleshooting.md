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

    "C:\Users\SEU_USUARIO\.local\bin\uv.exe" --version

Certo:

    & "C:\Users\SEU_USUARIO\.local\bin\uv.exe" --version

Se você colocar crase antes do &, o PowerShell tentará executar o texto & como comando e vai falhar. Portanto, o primeiro caractere da linha deve ser exatamente &.

## Passo 4 — editar o arquivo MCP correto

JSON não é comando de PowerShell. JSON deve ser salvo em arquivo.

Abra o arquivo de configuração do Claude Desktop com um dos comandos abaixo:

Para instalação empacotada (Microsoft Store):

COMANDO:

    notepad "$env:LocalAppData\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json"

Para instalação comum fora do pacote Windows:

COMANDO:

    notepad "$env:AppData\Claude\claude_desktop_config.json"

## Passo 4.1 — corrigir o conteúdo do JSON

O arquivo não pode ter dois blocos JSON seguidos. Apague tudo e deixe somente um objeto JSON.

Também não deixe a versão escapada com \n dentro do arquivo. Se o arquivo tiver algo parecido com `{\n"mcpServers"...`, apague essa parte.

**IMPORTANTE:** Antes de editar o JSON, execute este comando para obter o caminho correto do uv.exe no seu computador:

COMANDO:

    (Get-Command uv).Source

Use exatamente o caminho retornado no campo `command` do JSON, substituindo cada `\` por `\\`.

**IMPORTANTE:** O argumento `--directory` diz ao uv em qual pasta do servidor procurar o `pyproject.toml` e instalar as dependências. Sem ele, o servidor pode falhar com erros de módulo ausente.

Exemplo de JSON (substitua os caminhos pelos valores reais do seu computador):

    {
      "mcpServers": {
        "windows-mcp": {
          "command": "CAMINHO_RETORNADO_POR_Get-Command_uv_com_barras_duplicadas",
          "args": [
            "--directory",
            "C:\\caminho\\absoluto\\do\\servidor",
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

Por exemplo, se `(Get-Command uv).Source` retornou `C:\Users\seunome\.local\bin\uv.exe` e o servidor está em `C:\projetos\meu-servidor`, o JSON fica:

    {
      "mcpServers": {
        "windows-mcp": {
          "command": "C:\\Users\\seunome\\.local\\bin\\uv.exe",
          "args": [
            "--directory",
            "C:\\projetos\\meu-servidor",
            "run",
            "python",
            "C:\\projetos\\meu-servidor\\main.py"
          ],
          "env": {
            "PYTHONUTF8": "1"
          }
        }
      }
    }

## Passo 5 — validar se o JSON salvo está correto

No PowerShell, copie somente esta linha.

Para o seu caminho do pacote Windows:

COMANDO:

    Get-Content "$env:LocalAppData\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json | Out-Null; "JSON OK"

Para a instalação comum fora do pacote Windows:

COMANDO:

    Get-Content "$env:AppData\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json | Out-Null; "JSON OK"

Se aparecer JSON OK, o arquivo está válido.

Se aparecer erro, volte no Notepad e corrija aspas, vírgulas ou chaves.

## Passo 6 — testar o servidor MCP fora do Claude

Troque os caminhos pelos caminhos reais do seu computador.

COMANDO:

    & (Get-Command uv).Source --directory "C:\caminho\absoluto\do\servidor" run python "C:\caminho\absoluto\do\servidor\main.py"

Se preferir usar o caminho completo do uv.exe:

COMANDO:

    & "CAMINHO_DO_UV_AQUI" --directory "C:\caminho\absoluto\do\servidor" run python "C:\caminho\absoluto\do\servidor\main.py"

Se esse comando falhar, o problema ainda é no ambiente local, no uv, no Python ou no caminho do servidor.

Se esse comando funcionar, feche totalmente o Claude Desktop e abra de novo.

## Passo 7 — olhar logs

No PowerShell, copie somente esta linha.

Para o seu caminho do pacote Windows:

COMANDO:

    Get-Content "$env:LocalAppData\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\logs\mcp*.log" -Tail 80

Para a instalação comum fora do pacote Windows:

COMANDO:

    Get-Content "$env:AppData\Claude\logs\mcp*.log" -Tail 80

## Tabela de erros e correções

| Erro visto                   | Causa                               | Correção                                                        |
| ---------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| O termo uv não é reconhecido | uv não instalado ou fora do PATH    | Instale uv e reabra o PowerShell                                |
| O termo & não é reconhecido  | Você colou crase antes do &         | Digite a linha começando diretamente por &                      |
| Token ':' inesperado         | Você colou JSON no PowerShell       | Abra o JSON no Notepad e salve no arquivo de configuração       |
| Token run inesperado         | Você executou EXE entre aspas sem & | Use & antes do caminho entre aspas                              |
| spawn uv ENOENT              | O cliente MCP não achou uv          | Use o caminho absoluto retornado por (Get-Command uv).Source    |
| Erro de módulo ausente       | uv não encontrou o pyproject.toml   | Adicione --directory com o caminho da pasta do servidor no args |
| Dois blocos JSON no arquivo  | Conteúdo duplicado                  | Apague tudo e deixe somente um objeto JSON principal            |
| Texto com \n dentro do JSON  | JSON escapado foi colado como texto | Apague esse bloco e cole JSON normal no Notepad                 |
| Caminho errado no JSON       | Placeholder não foi substituído     | Use o caminho exato retornado por (Get-Command uv).Source       |

## Checklist final

- uv --version funciona sem crases.
- where.exe uv mostra o caminho do uv.exe.
- (Get-Command uv).Source retorna o caminho usado no JSON.
- O comando com & e --directory antes de run funciona no PowerShell.
- O arquivo claude_desktop_config.json contém mcpServers.
- O campo args inclui --directory com o caminho da pasta do servidor antes de run.
- O arquivo tem apenas um objeto JSON principal.
- O arquivo não contém texto literal com \n.
- O campo command usa o caminho exato retornado por (Get-Command uv).Source com barras duplicadas.
- O JSON valida com ConvertFrom-Json.
- O Claude Desktop foi fechado por completo e aberto novamente.
