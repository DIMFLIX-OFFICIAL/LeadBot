#!/usr/bin/env python3

import asyncio

import uvloop

from .core import LeadBot
from .loader import db
from .config import cfg
from .utils.json_proxy import JSONProxy

from loguru import logger


def add_account() -> None:
    import easygui

    session_pyro = easygui.fileopenbox(filetypes=["*.session"])

    if not session_pyro:
        logger.error("Не выбрана сессия Pyrogram. Завершение скрипта...")
        return

    api_id = int(input("Введите api_id: "))
    api_hash = input("Введите api_hash: ")
    proxy_str = input("Введите прокси (Если он не нужен, просто нажми Enter): ")

    if proxy_str.strip() == "":
        proxy = None
    else:
        proxy = JSONProxy.convert_proxy_to_dict(proxy_str)

    async def add():
        from pyrogram import Client

        async with Client(
            api_id=api_id,
            api_hash=api_hash,
            name=session_pyro.replace(".session", ""),
            proxy=proxy,
        ) as client:
            me = await client.get_me()
            account_id = me.id
            phone_number = me.phone_number
            session_str = await client.export_session_string()

        await db.accounts.add_account(
            account_id=account_id,
            phone_number=phone_number,
            api_id=api_id,
            api_hash=api_hash,
            proxy=proxy,
            session_string=session_str,
        )

    asyncio.run(add())


async def _main():
    bot = LeadBot(
        managers_chat=cfg.bot.manager_chat_id,
        trigger_words=cfg.bot.trigger_words,
        folder_name=cfg.bot.folder_name,
        blacklist_chats=cfg.bot.blacklist_chats,
        log_chat_id=cfg.bot.log_chat_id,
    )
    await bot.start()


def main():
    uvloop.install()
    asyncio.run(_main())


if __name__ == "__main__":
    main()
