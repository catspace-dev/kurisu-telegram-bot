from aiogram.types import Message
from mcstatus import MinecraftServer
import socket

async def querymc_cmd(msg: Message):
    try:
        _, addr = msg.parse_entities().split(' ', 1)
    except ValueError:
        await msg.answer("Использование: "
                         "<code>/querymc "
                         "&lt;IP_Сервера&gt;[:&lt;Порт_Query&gt;]"
                         "</code>", "HTML")
    else:
        msg = await msg.answer("⌛️ Пингую...")
        server = MinecraftServer.lookup(addr)
        try:
            query = server.query()
        except socket.timeout:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Таймаут)</i>", "HTML")
        except ConnectionResetError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Удаленный хост принудительно "
                                "разорвал существующее подключение)"
                                "</i>", "HTML")
        except ConnectionRefusedError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Подключение не установлено, т.к. "
                                "конечный хост отверг запрос на подключение)"
                                "</i>", "HTML")
        except ConnectionAbortedError:
            await msg.edit_text("🏐 <b>Сервер выключен.</b> "
                                "<i>(Установленное соединение было прервано "
                                "программным обеспечением на вашем "
                                "хост-компьютере)"
                                "</i>", "HTML")
        else:
            online = str(query.players.online)
            maxonline = str(query.players.max)
            if not query.players.names:
                await msg.edit_text("🎾 <b>Сервер включен.</b>"
                                    f"\n * Онлайн: <i>{online}"
                                    f" из {maxonline}</i>", "HTML")
            else:
                playerlist = ""
                for playername in query.players.names:
                    playerlist += f"<code>{playername}</code> "
                await msg.edit_text("🎾 <b>Сервер включен.</b>"
                                    f"\n * Онлайн: <i>{online}"
                                    f" из {maxonline}</i>"
                                    f"\n * Игроки: {playerlist}", "HTML")
