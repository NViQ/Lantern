import unittest
from .lantern import Lantern, handle_message


class TestLantern(unittest.TestCase):
    def setUp(self):
        self.lantern = Lantern()

    def test_init_with_defaults(self):
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'белый')

    def test_init_with_status_and_color(self):
        f = Lantern(status=1, color=3)
        self.assertEqual(f.status, 1)
        self.assertEqual(f.color, 'красный')

    def test_init_with_invalid_color(self):
        with self.assertRaises(KeyError):
            Lantern(color=4)


    async def test_run_command(self):

        await self.lantern.run_command('on')
        self.assertEqual(self.lantern.status, 1)
        self.assertEqual(self.lantern.color, 'белый')
        self.assertRaises(ValueError, self.lantern.run_command, 'on')


        await self.lantern.run_command('off')
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'белый')
        self.assertRaises(ValueError, self.lantern.run_command, 'off')

        await self.lantern.run_command('color', 2)
        self.assertEqual(self.lantern.status, 0)
        self.assertEqual(self.lantern.color, 'синий')
        self.assertRaises(ValueError, self.lantern.run_command, 'color', 4)

        async with self.assertRaises(ValueError):
            await self.lantern.run_command('color', 4)


class TestHandleMessage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.lantern = AsyncMock()

    async def test_handle_message_on(self):
        await handle_message({'command': 'on'}, self.lantern)
        self.lantern.run_command.assert_called_once_with('on', None)

    async def test_handle_message_off(self):
        await handle_message({'command': 'off'}, self.lantern)
        self.lantern.run_command.assert_called_once_with('off', None)

    async def test_handle_message_color(self):
        await handle_message({'command': 'color', 'metadata': 2}, self.lantern)
        self.lantern.run_command.assert_called_once_with('color', 2)



if __name__ == '__main__':
    unittest.main()