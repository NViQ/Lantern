import unittest
from unittest.mock import patch, AsyncMock

from lantern import Lantern, main, handle_message
import tracemalloc


tracemalloc.start()

class TestLantern(unittest.TestCase):
    def setUp(self):
        self.lantern = Lantern()

    # тесты конструктора класса Lantern
    def test_init_with_defaults(self):
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'белый')

    def test_init_with_status_and_color(self):
        f = Lantern(status=1, color=2)
        self.assertEqual(f.status, 1)
        self.assertEqual(f.color, 'синий')

    def test_init_with_invalid_color(self):
        with self.assertRaises(KeyError):
            Lantern(color=4)



    async def test_run_command(self):
        # тесты включения
        await self.lantern.run_command('on')
        self.assertEqual(self.lantern.status, 1)
        self.assertEqual(self.lantern.color, 'белый')
        await self.assertRaises(ValueError, self.lantern.run_command, 'on')

        # тесты выключения
        await self.lantern.run_command('off')
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'белый')
        await self.assertRaises(ValueError, self.lantern.run_command, 'off')

        # тесты установки цвета
        await self.lantern.run_command('color', 3)
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'красный')
        await self.assertRaises(ValueError, self.lantern.run_command, 'color', 4)

        async with self.assertRaises(ValueError):
            await self.lantern.run_command('color', 4)


class TestHandleMessage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.lantern = AsyncMock()

    # тесты обработки полученных сообщений
    async def test_handle_message_on(self):
        await handle_message({'command': 'on'}, self.lantern)
        self.lantern.run_command.assert_called_once_with('on', None)

    async def test_handle_message_off(self):
        await handle_message({'command': 'off'}, self.lantern)
        self.lantern.run_command.assert_called_once_with('off', None)

    async def test_handle_message_color(self):
        await handle_message({'command': 'color', 'metadata': 2}, self.lantern)
        self.lantern.run_command.assert_called_once_with('color', 2)


class TestMain(unittest.IsolatedAsyncioTestCase):

    @patch('aiohttp.ClientSession.ws_connect')
    @patch('lantern.handle_message')
    async def test_main(self, handle_mock, ws_connect_mock):

        ws_mock = AsyncMock()
        mssg_mock = AsyncMock()
        ws_mock.__aiter__.return_value = [mssg_mock]


        ws_connect_mock.return_value.__aenter__.return_value = ws_mock
        mssg_mock.type = 'text'
        mssg_mock.json.return_value = {'message': 'test'}

        await main()

        ws_connect_mock.assert_called_once_with('http://127.0.0.1:9999')


if __name__ == '__main__':
    unittest.main()