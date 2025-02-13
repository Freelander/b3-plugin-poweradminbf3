# -*- encoding: utf-8 -*-
import unittest
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
from tests import extends_mock
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf3 import Poweradminbf3Plugin

extends_mock()

class Test_load_server_config(unittest.TestCase):

    def setUp(self):
        self.console = Mock()
        self.p = Poweradminbf3Plugin(self.console)

    def test_empty_file(self):
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName")
        self.p.load_server_config(client, "theConfName", None)
        self.p.load_server_config(client, "theConfName", [])
        self.p.load_server_config(client, "theConfName", tuple())

    def test_kind_of_empty_file(self):
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", (
            "",
            "",
            "",
            "       ",
            "           ",
            "         ",
            "\n",
            "\n\r",
            "\r ",
            ""
        ))
        self.assertFalse(self.console.write.called)

    def test_comments(self):
        self.console.reset_mock()
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", (
            "#vars.autoBalance true",
            "  #vars.autoBalance true",
            "#  vars.autoBalance true",
            "  #  vars.autoBalance true",
            "//vars.autoBalance true",
            " //vars.autoBalance true",
            "//  vars.autoBalance true",
            "  //  vars.autoBalance true",
            " +-----------------------------------+",
            " |                                   |",
            " |      maps below                   |",
            " |                                   |",
            " +-----------------------------------+",
        ))
        self.assertFalse(self.console.write.called)

    def test_read_cvars_no_result(self):
        self.console.write.return_value = []
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", (
            "vars.withnoarg",
            "   vars.withnoarg",
            "   vars.withnoarg    ",
            "vars.withnoarg    ",
        ))
        self.assertEqual(4,self.console.write.call_count)
        self.console.write.assert_called_with(('vars.withnoarg',))

    def test_read_cvars_with_result(self):
        self.console.write.return_value = ['theResult']
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("vars.withnoarg",))
        self.assertTrue(self.console.write.called)
        self.console.write.assert_called_with(('vars.withnoarg',))
        self.assertTrue(client.message.called)
        client.message.assert_was_called_with('vars.withnoarg is "theResult"')

    def test_read_cvars_with_error(self):
        self.console.write.side_effect = CommandFailedError('theError')
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("vars.withnoarg",))
        self.assertTrue(self.console.write.called)
        self.console.write.assert_called_with(('vars.withnoarg',))
        client.message.assert_was_called_with('Error "theError" received at line 1 when sending "vars.withnoarg" to server')

    def test_write_cvars_no_result(self):
        self.console.write.return_value = []
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", (
            "vars.theCvar theValue",
            "   vars.theCvar theValue1 theValue2 theValue3",
            "   vars.theCvar   theValue   ",
            "vars.theCvar      theValue",
            "vars.theCvar 5",
        ))
        self.assertEqual(5,self.console.write.call_count)
        self.console.write.assert_was_called_with(('vars.theCvar', 'theValue'))
        self.console.write.assert_was_called_with(('vars.theCvar', 'theValue1 theValue2 theValue3'))
        self.console.write.assert_was_called_with(('vars.theCvar', '5'))

    def test_write_cvars_with_result(self):
        self.console.write.return_value = ['theResult']
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("vars.theCvar theValue",))
        self.assertTrue(self.console.write.called)
        self.console.write.assert_called_with(('vars.theCvar', 'theValue'))
        self.assertEqual(1, client.message.call_count)
        client.message.assert_was_called_with('New config "theConfName" loaded')

    def test_write_cvars_with_error(self):
        self.console.write.side_effect = CommandFailedError('theError')
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("vars.theCvar   theValue",))
        self.assertTrue(self.console.write.called)
        self.console.write.assert_called_with(('vars.theCvar', 'theValue'))
        client.message.assert_was_called_with('Error "theError" received at line 1 when sending "vars.theCvar   theValue" to server')


    def test_map_item(self):
        self.console.write.return_value = []
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("MAP_001 gamemode1 3",))
        self.assertEqual(3,self.console.write.call_count)
        self.console.write.assert_was_called_with(('mapList.clear',))
        self.console.write.assert_was_called_with(('mapList.add', 'MAP_001', 'gamemode1', '3'))
        self.console.write.assert_was_called_with(('mapList.save',))

    def test_map_item_with_error(self):
        def my_write(*args):
            if len(args) and len(args[0]) and 'mapList.add' == args[0][0]:
                raise CommandFailedError('theError')
            return []
        self.console.write.side_effect = my_write
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", ("MAP_001 gamemode1 3",))
        self.assertEqual(3,self.console.write.call_count)
        self.console.write.assert_was_called_with(('mapList.clear',))
        self.console.write.assert_was_called_with(('mapList.add', 'MAP_001', 'gamemode1', '3'))
        self.console.write.assert_was_called_with(('mapList.save',))
        client.message.assert_was_called_with('Error adding map "MAP_001 gamemode1 3" on line 1 : theError')



if __name__ == '__main__':
    unittest.main(verbosity=2)