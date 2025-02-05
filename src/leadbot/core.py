import asyncio
import re
import traceback
from dataclasses import dataclass, field
from typing import Dict, List

from loguru import logger
from pyrogram import Client, idle
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .config import cfg
from .database.models import Account
from .loader import bot, db


@dataclass
class Worker:
    account: Account
    session: Client
    suitable_chats: List[int] = field(init=False, default_factory=list)


class LeadBot:
    def __init__(
        self,
        managers_chat: int,
        trigger_words: List[str],
        folder_name: str,
        blacklist_chats: List[int],
        log_chat_id: int
    ):
        self.managers_chat: int = managers_chat
        self.blacklist_chats: List[int] = blacklist_chats
        self.folder_name: str = folder_name
        self.trigger_words: List[str] = trigger_words
        self.log_chat_id = log_chat_id
        self.workers: Dict[int, Worker] = dict()

    async def start(self):
        await self.init_clients()
        logger.info("Начинаю мониторинг сообщений!")
        asyncio.create_task(self.while_update_accounts_chats())
        await idle()

    async def init_clients(self):
        accounts = await db.accounts.get_accounts()
        error_accounts = []
        connected_accounts = 0

        for account in accounts:
            try:
                if account.proxy:
                    client = Client(
                        name="my_account",
                        api_id=account.api_id,
                        api_hash=account.api_hash,
                        session_string=account.session_string,
                        proxy=account.proxy,
                    )
                else:
                    client = Client(
                        name="my_account",
                        api_id=account.api_id,
                        api_hash=account.api_hash,
                        session_string=account.session_string,
                    )

                client.add_handler(MessageHandler(self.handle_message))
                await client.start()
                self.workers[account.id] = Worker(
                    account=account,
                    session=client,
                )
                connected_accounts += 1
            except Exception:
                logger.error(
                    f"Ошибка при подключении аккаунта: {traceback.format_exc()}"
                )
                await db.accounts.set_account_valid(
                    account_id=accounts.id,
                    status=False
                )
                error_accounts.append(account.id)

            await self.log(f"Подключено аккаунтов: {connected_accounts}/{len(accounts)}")
            if len(error_accounts) > 0:
                await self.log_error(f"Возникла ошибка при подключении к аккаунтам: {','.join(error_accounts)}")

            await self.update_accounts_chats()

    async def while_update_accounts_chats(self):
        while True:
            await asyncio.sleep(cfg.bot.delay_for_update_accounts_chats)
            await self.update_accounts_chats()

    async def update_accounts_chats(self):
        for worker in self.workers.values():
            logger.info(f"Обновляю список чатов у: {worker.account.id}")
            client = worker.session

            try:
                folders = await client.get_folders()
                new_chats = []

                for f in folders:
                    if f.title.text == self.folder_name:
                        if f.included_chats:
                            for chat in f.included_chats:
                                new_chats.append(chat.id)
                        if f.pinned_chats:
                            for chat in f.pinned_chats:
                                new_chats.append(chat.id)

                worker.suitable_chats.clear()
                worker.suitable_chats.extend(new_chats)
            except AttributeError:
                logger.error(f"На аккаунте {worker.account.id} нет папок!")
                await self.log_error(
                    f"Ошибка обновлении списка чатов аккаунта {worker.account.id}"
                )
            except Exception:
                logger.error(
                    f"Ошибка при обновлении списка чатов аккаунта {worker.account.id}: {traceback.format_exc()}"
                )
                await self.log_error(
                    f"Ошибка обновлении списка чатов аккаунта {worker.account.id}"
                )

        await self.log("Обновил список чатов на всех аккаунтах!")

    async def handle_message(self, client: Client, message: Message):
        logger.info(f"Получено сообщение от @{message.chat.username}: {message.link}")

        try:
            text = message.text
            user = message.from_user
            message_link = message.link

            if not text:
                logger.info("Сообщение пустое")
                return

            if message.chat.id in cfg.bot.blacklist_chats:
                logger.info("Чат в блэк листе")
                return

            for w in self.workers.values():
                if client is w.session:
                    if message.chat.id in w.suitable_chats:
                        break
            else:
                logger.info("Чат не находится в папке.")
                return

            text_lower = message.text.lower()
            if not any(
                re.search(rf"\b{word}\b", text_lower) for word in self.trigger_words
            ):
                logger.info("В сообщении нет триггерных слов")
                return

            report = (
                f"⚠️ **Новый лид!**\n\n"
                f"📄 Сообщение: `{message.text[:200]}...`\n"
                f"💬 Чат: {message.chat.title} (ID: `{message.chat.id}`; @{message.chat.username})\n"
                f"👤 Автор: @{user.username} (ID: `{user.id}`)\n"
                f"🕒 Время: {message.date.strftime('%d.%m.%Y %H:%M')}\n"
                f"🔢 Длина: {len(message.text)} символов\n"
                f"🔗 {message_link}"
            )

            await bot.send_message(
                chat_id=self.managers_chat,
                text=report,
                parse_mode=ParseMode.MARKDOWN,
            )
            await self.log(f"📩 Переслано сообщение из чата {message.chat.title}")
        except Exception as e:
            await self.log_error(f"Ошибка обработки сообщения: {str(e)}")

    async def log(self, text: str):
        await self.send_to_log_chat(f"ℹ️ {text}")

    async def log_error(self, text: str):
        await self.send_to_log_chat(f"🚨 {text}")

    async def send_to_log_chat(self, text: str):
        try:
            await bot.send_message(self.log_chat_id, text)
        except Exception:
            print(f"Ошибка логирования: {traceback.format_exc()}")
