import aiohttp
import asyncio


class Lantern:

    COMMANDS = {
        'on': 'turn_on',
        'off': 'turn_off',
        'color': 'change_color',
    }
    COLORS = {1: 'белый', 2: 'синий', 3: 'красный'}


    def __init__(self, status: int = 0, color: int = 1) -> None:

        self.status = status
        self.color = self.COLORS[color]

    # Получаем комманду для фонаря асинхронным методом.
    async def run_command(self, command: str, metadata: int) -> None:

        command_name = self.COMMANDS[command]
        attr_name = getattr(self, command_name)
        attr_name(metadata)

    def turn_on(self):
        if not self.status:
            self.status = 1
            print('Фонарь включен.')
        else:
            raise ValueError('Фонарь уже включен.')


    def turn_off(self):
        if self.status:
            self.status = 0
            print('Фонарь выключен.')
        else:
            raise ValueError('Фонарь уже выключен.')


    def change_color(self, metadata):
        if metadata is None or metadata not in self.COLORS:
            raise ValueError('Нет такого цвета, проверьте атрибуты.')
        elif self.COLORS[metadata] == self.color:
            print(f'{self.color} цвет уже установлен.')
        else:
            self.color = self.COLORS[metadata]
            print(f'Установлен {self.color} цвет фонаря.')

# Обрабатываем сообщения от сервера асинхронным методом
async def handle_message(message: dict, lantern: Lantern) -> None:
    try:
        command = message['command'].lower()
        metadata = message.get('metadata')
        await lantern.run_command(command, metadata)
    except ValueError as err:
        print(err)


# Запускаем функцию асинхронным методом
async def main():
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 9999

    try:
        lantern = Lantern()
        # Создаем объект для работы с сокетом
        async with aiohttp.ClientSession() as session:
            socket = session.ws_connect(f'http://{SERVER_ADDRESS}:{SERVER_PORT}')
            # Цикл для чтения сообщений от веб-сокета.
            async for mssg in socket:
                if mssg.type == aiohttp.WSMsgType.TEXT:
                    message = mssg.json()
                    await handle_message(message, lantern)
    except Exception as err:
        print(f'Ошибка при подключении: {err}')


if __name__ == '__main__':
    asyncio.run(main())