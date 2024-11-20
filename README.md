### **README.md**

# Telegram Media Downloader

Este projeto é uma ferramenta para automatizar o **download de mídias** de canais e grupos do Telegram, incluindo aqueles com restrições. Ele utiliza a biblioteca **Pyrogram** para se comunicar com a API do Telegram e gerenciar o download de arquivos de maneira eficiente.

---

## **Descrição**
Este script permite ao usuário baixar automaticamente todas as mídias de canais ou grupos específicos no Telegram, organizando os arquivos localmente. Ele é capaz de gerenciar limites da API, retomar downloads interrompidos e evitar downloads duplicados. 

---

## **Funcionalidades**
- Listagem de canais e grupos dos quais o usuário faz parte.
- Download automático de mídias (fotos, vídeos, áudios, documentos e animações).
- Organização de mídias em pastas com o nome do canal ou grupo.
- Retomada automática de downloads interrompidos.
- Controle de mensagens já processadas para evitar duplicação.
- Suporte a álbuns de mídia (grupos de arquivos).

---

## Funcionamento Geral
1. Credenciais e Configuração:

- O script solicita ao usuário o `API_ID` e o `API_HASH`, necessários para autenticação na API do Telegram. Essas credenciais são salvas em um arquivo `config.ini` para uso futuro.

2. Listagem de Canais:

- O código exibe todos os canais e grupos dos quais o usuário é membro. Ele permite que o usuário selecione um canal para iniciar o download das mídias.

3. Controle de Downloads:

- Para evitar downloads duplicados, o script mantém um registro (`control_<channel_id>.json`) que armazena:
  - O último `message_id` processado.
  - Grupos de mídia já processados (para mensagens agrupadas, como álbuns).

4. Tipos de Mídias Suportadas:

- O script verifica os tipos de mídia (fotos, vídeos, áudios, documentos, animações) e define a extensão apropriada ao salvar os arquivos.

5. Baixar Mídias:

- As mídias são salvas em pastas com o nome do canal. Mensagens agrupadas (álbuns) têm suas próprias subpastas.
- Verifica se uma mídia já foi baixada, evitando redundâncias.

6. Mecanismos de Controle:

- Gerencia limites impostos pela API do Telegram (usando o erro `FloodWait`) e aguarda o tempo necessário antes de fazer novas requisições.

7. Retomada de Downloads:

- Caso o processo seja interrompido, o script pode retomar o download do ponto onde parou, usando o arquivo de controle.

8. Interface Simples:

   - O usuário interage com o script via terminal para:
       - Inserir credenciais.
        - Escolher um canal.
        - Acompanhar o progresso do download.



## **Requisitos**
- **Python 3.7+**
- Biblioteca **Pyrogram**
- Credenciais do Telegram (`API_ID` e `API_HASH`).

---

## **Instalação**
1. Clone este repositório:
   ```bash
   git clone https://github.com/viniciusnxar/Telegram-Media-Downloader
   cd telegram-media-downloader
   ```

2. Instale as dependências:
   ```bash
   pip install pyrogram
   ```

3. Crie uma conta de desenvolvedor no Telegram para obter o `API_ID` e o `API_HASH`:
   - Acesse o [Telegram Apps](https://my.telegram.org/apps).
   - Crie um novo aplicativo e copie as credenciais fornecidas.

4. Execute o script para configurar o ambiente:
   ```bash
   python downloader.py
   ```
   - Caso seja sua primeira execução, insira o `API_ID` e o `API_HASH` quando solicitado.

---

## **Uso**
1. Execute o script:
   ```bash
   python downloader.py
   ```

2. O script exibirá a lista de canais e grupos disponíveis na sua conta Telegram.

3. Escolha o número correspondente ao canal ou grupo que deseja processar.

4. As mídias serão baixadas automaticamente para uma pasta local com o nome do canal/grupo.

---

## **Como Funciona**
1. **Configuração**:
   - O script solicita o `API_ID` e o `API_HASH` para se autenticar na API do Telegram.
   - Estas credenciais são salvas no arquivo `config.ini` para uso posterior.

2. **Listagem de Canais**:
   - Exibe todos os canais e grupos dos quais o usuário é membro.
   - O usuário seleciona o canal para iniciar o download.

3. **Download**:
   - As mídias são organizadas em pastas com o nome do canal/grupo.
   - Arquivos de controle (`control_<channel_id>.json`) rastreiam o progresso do download, evitando duplicações.

4. **Tipos de Arquivo Suportados**:
   - Fotos (`.jpg`), vídeos (`.mp4`), áudios (`.mp3`, `.ogg`), documentos (extensão original) e animações (`.mp4`).

5. **Resiliência**:
   - Se o processo for interrompido, ele pode ser retomado do ponto onde parou.
   - Lida com os limites de requisição da API do Telegram (`FloodWait`) pausando automaticamente quando necessário.

---

## **Estrutura do Projeto**
```
telegram-media-downloader/
├── downloader.py       # Script principal
├── config.ini          # Arquivo de configuração com credenciais (gerado automaticamente)
├── control_<id>.json   # Arquivo de controle para canais (gerado automaticamente)
├── media/              # Pasta contendo as mídias baixadas (gerada automaticamente)
└── README.md           # Documentação do projeto
```

---

## **Exemplo de Execução**
1. Execute o script:
   ```bash
   python downloader.py
   ```

2. Insira as credenciais se solicitado:
   ```
   Digite o seu API_ID: 123456
   Digite o seu API_HASH: abcdef1234567890abcdef1234567890
   ```

3. Escolha um canal/grupo:
   ```
   Buscando canais...
   1 - Canal Público 1
   2 - Grupo Restrito 2
   3 - Canal Restrito 3
   Selecione um canal digitando seu número: 2
   ```

4. O download iniciará automaticamente:
   ```
   Iniciando download a partir da mensagem ID 1000.
   Baixou mídia da mensagem 1000.
   Aguardando 15 segundos devido ao limite de requisições.
   Download concluído.
   ```

---

## **Aviso de Uso**
Este script foi projetado para fins pessoais, como backup de dados de canais ou grupos dos quais você é membro. **O uso indevido para infringir direitos autorais ou acessar mídias sem permissão pode violar os Termos de Serviço do Telegram.**

---

## **Contribuição**
Sinta-se à vontade para enviar PRs ou relatar problemas. Sugestões são sempre bem-vindas!

---

## **Licença**
Este projeto está licenciado sob a [MIT License](LICENSE).