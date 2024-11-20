# -*- coding: utf-8 -*-
"""
Versão: [v1.0 - 22/10/2024]
Descrição: Este script usa a biblioteca Pyrogram para automatizar o download de mídias de canais e grupos restritos do Telegram.

"""

import os
import configparser
import json
from pyrogram import Client, errors
from pyrogram.types import Chat
from pyrogram.enums import ChatType

import asyncio

# Função que exibe informações sobre o autor e o código
def exibir_informacoes_autor():
    print("="*50)
    print("Autor: [@Just4D3v]")
    print("Descrição: Este script usa a biblioteca Pyrogram para automatizar o download de mídias de canais restritos no Telegram.")
    print("="*50)

# Exibe as informações quando o script é executado
exibir_informacoes_autor()

# Função para solicitar API_ID e API_HASH ao usuário e salvar no config.ini
def get_api_credentials():
    api_id = input("Digite o seu API_ID: ")
    api_hash = input("Digite o seu API_HASH: ")
    config = configparser.ConfigParser()
    config['pyrogram'] = {
        'api_id': api_id,
        'api_hash': api_hash
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return api_id, api_hash

# Verificar se o arquivo config.ini existe
if not os.path.exists('config.ini'):
    print("Arquivo config.ini não encontrado.")
    api_id, api_hash = get_api_credentials()
else:
    # Ler API_ID e API_HASH do config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = config.get("pyrogram", "api_id")
    api_hash = config.get("pyrogram", "api_hash")

# Criar um cliente Pyrogram
app = Client("my_session", api_id=api_id, api_hash=api_hash)

async def list_channels():
    channels = []
    print("Buscando canais...")
    async with app:
        async for dialog in app.get_dialogs():
            chat = dialog.chat
            if chat.type in (ChatType.CHANNEL, ChatType.SUPERGROUP):
                channels.append(chat)
        if not channels:
            print("Você não é membro de nenhum canal.")
            return []
        print("Canais:")
        for idx, channel in enumerate(channels, start=1):
            print(f"{idx} - {channel.title}")
    return channels

async def get_last_message_id(chat_id):
    async with app:
        while True:
            try:
                last_message = None
                async for message in app.get_chat_history(chat_id, limit=1):
                    last_message = message
                if last_message:
                    return last_message.id
                else:
                    return None
            except errors.FloodWait as e:
                print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
                await asyncio.sleep(e.value)

def load_control_file(channel_id):
    control_filename = f"control_{channel_id}.json"
    if os.path.exists(control_filename):
        with open(control_filename, 'r') as f:
            data = json.load(f)
        return data
    else:
        return None

def save_control_file(channel_id, data):
    control_filename = f"control_{channel_id}.json"
    with open(control_filename, 'w') as f:
        json.dump(data, f)

def get_media_extension(message):
    if message.photo:
        return '.jpg'
    elif message.video:
        return '.mp4'
    elif message.audio:
        return '.mp3'
    elif message.document:
        # Tentar obter a extensão do nome do arquivo original
        if message.document.file_name:
            return os.path.splitext(message.document.file_name)[1]
        else:
            return ''
    elif message.voice:
        return '.ogg'
    elif message.animation:
        return '.mp4'
    else:
        return ''

async def download_media(message, folder):
    extension = get_media_extension(message)
    file_name = f"{message.id}{extension}"
    path = os.path.join(folder, file_name)

    # Verificar se o arquivo já existe
    if os.path.exists(path):
        print(f"Mídia da mensagem {message.id} já existe. Pulando download.")
        return True

    while True:
        try:
            await message.download(file_name=path)
            print(f"Baixou mídia da mensagem {message.id}")
            await asyncio.sleep(15)
            return True
        except errors.FloodWait as e:
            print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Erro ao baixar mídia da mensagem {message.id}: {e}")
            return False

async def download_media_from_channel(channel: Chat):
    channel_id = channel.id
    channel_name = channel.title.replace("/", "_").replace("\\", "_")
    if not os.path.exists(channel_name):
        os.makedirs(channel_name)
    # Carregar arquivo de controle
    control_data = load_control_file(channel_id)
    if control_data:
        start_id = control_data.get("start_id")
        last_message_id = control_data.get("last_message_id")
        processed_media_groups = set(control_data.get("processed_media_groups", []))
        print(f"Retomando download. Última mensagem baixada: ID {last_message_id}")
        # Obter o ID da última mensagem atual
        current_last_message_id = await get_last_message_id(channel_id)
        if current_last_message_id > start_id:
            print(f"Novas mensagens encontradas. Atualizando start_id de {start_id} para {current_last_message_id}")
            old_start_id = start_id
            start_id = current_last_message_id
            control_data["start_id"] = start_id
            # Salvar o controle atualizado
            save_control_file(channel_id, control_data)
            # Baixar novas mensagens de current_last_message_id até old_start_id + 1
            message_id = current_last_message_id
            while message_id > old_start_id:
                if message_id <= last_message_id:
                    break  # Evitar rebaixar mensagens já processadas
                try:
                    message = await app.get_messages(channel_id, message_ids=message_id)
                except errors.FloodWait as e:
                    print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
                    await asyncio.sleep(e.value)
                    continue
                except Exception as e:
                    print(f"Erro ao buscar mensagem {message_id}: {e}")
                    message_id -= 1
                    continue

                if message.empty:
                    message_id -= 1
                    continue

                # Processar a mensagem (código similar ao existente)
                if message.media:
                    if message.media_group_id:
                        if message.media_group_id in processed_media_groups:
                            print(f"Grupo de mídia {message.media_group_id} já processado.")
                        else:
                            # Criar pasta para o grupo de mídia usando o media_group_id
                            folder = os.path.join(channel_name, f"media_group_{message.media_group_id}")
                            if not os.path.exists(folder):
                                os.makedirs(folder)

                            # Baixar todas as mídias do grupo
                            while True:
                                try:
                                    media_group_messages = await app.get_media_group(channel_id, message.id)
                                    download_success = True
                                    for msg in media_group_messages:
                                        success = await download_media(msg, folder)
                                        if not success:
                                            download_success = False
                                            break
                                    if download_success:
                                        # Atualizar grupos de mídia processados
                                        processed_media_groups.add(message.media_group_id)
                                        control_data['processed_media_groups'] = list(processed_media_groups)
                                        save_control_file(channel_id, control_data)
                                    break
                                except errors.FloodWait as e:
                                    print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
                                    await asyncio.sleep(e.value)
                                except Exception as e:
                                    print(f"Erro ao buscar grupo de mídia {message.media_group_id}: {e}")
                                    break
                    else:
                        # Mensagem de mídia única
                        success = await download_media(message, channel_name)
                else:
                    print(f"Nenhuma mídia na mensagem {message_id}")

                message_id -= 1

            # Após baixar novas mensagens, atualizar o control_data e definir message_id para last_message_id - 1
            save_control_file(channel_id, control_data)
            message_id = last_message_id - 1
        else:
            print("Não há novas mensagens para baixar.")
            # Continuar a partir de last_message_id - 1
            message_id = last_message_id - 1
    else:
        # Primeira execução
        current_last_message_id = await get_last_message_id(channel_id)
        start_id = current_last_message_id
        last_message_id = current_last_message_id
        processed_media_groups = set()
        print(f"Iniciando download a partir da mensagem ID {start_id}")
        control_data = {
            "name": channel_name,
            "channel_id": channel_id,
            "start_id": start_id,
            "last_message_id": last_message_id,
            "processed_media_groups": []
        }
        # Salvar o controle
        save_control_file(channel_id, control_data)
        message_id = current_last_message_id

    # Continuar o download das mensagens anteriores a partir de message_id
    async with app:
        while message_id > 0:
            try:
                message = await app.get_messages(channel_id, message_ids=message_id)
            except errors.FloodWait as e:
                print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
                await asyncio.sleep(e.value)
                continue
            except Exception as e:
                print(f"Erro ao buscar mensagem {message_id}: {e}")
                message_id -= 1
                continue

            if message.empty:
                message_id -= 1
                continue

            if message.media:
                if message.media_group_id:
                    if message.media_group_id in processed_media_groups:
                        print(f"Grupo de mídia {message.media_group_id} já processado.")
                    else:
                        # Criar pasta para o grupo de mídia usando o media_group_id
                        folder = os.path.join(channel_name, f"media_group_{message.media_group_id}")
                        if not os.path.exists(folder):
                            os.makedirs(folder)

                        # Baixar todas as mídias do grupo
                        while True:
                            try:
                                media_group_messages = await app.get_media_group(channel_id, message.id)
                                download_success = True
                                for msg in media_group_messages:
                                    success = await download_media(msg, folder)
                                    if not success:
                                        download_success = False
                                        break
                                if download_success:
                                    # Atualizar grupos de mídia processados
                                    processed_media_groups.add(message.media_group_id)
                                    control_data['processed_media_groups'] = list(processed_media_groups)
                                    # Atualizar last_message_id
                                    control_data["last_message_id"] = message_id
                                    save_control_file(channel_id, control_data)
                                break
                            except errors.FloodWait as e:
                                print(f"Aguardando {e.value} segundos devido ao limite de requisições.")
                                await asyncio.sleep(e.value)
                            except Exception as e:
                                print(f"Erro ao buscar grupo de mídia {message.media_group_id}: {e}")
                                break
                else:
                    # Mensagem de mídia única
                    success = await download_media(message, channel_name)
                    if success:
                        # Atualizar last_message_id
                        control_data["last_message_id"] = message_id
                        save_control_file(channel_id, control_data)
            else:
                print(f"Nenhuma mídia na mensagem {message_id}")

            message_id -= 1

    print("Download concluído.")

async def main():
    channels = await list_channels()
    if not channels:
        return
    channel_number = int(input("Selecione um canal digitando seu número: "))
    if 1 <= channel_number <= len(channels):
        channel = channels[channel_number - 1]
        await download_media_from_channel(channel)
    else:
        print("Número de canal inválido.")

if __name__ == "__main__":
    app.run(main())
