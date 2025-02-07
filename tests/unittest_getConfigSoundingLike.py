# -*- encoding: utf-8 -*-
import unittest
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
from tests import extends_mock
from poweradminbf3 import Poweradminbf3Plugin

extends_mock()

class Test_getConfigSoundingLike(unittest.TestCase):

    def setUp(self):
        self.available_names = ["hardcore", "normal", "infantry", "tdm", "conquest", "rush", "quickmatch", "hardcore-tdm", "hardcore-conquest"]
        self.console = Mock()
        self.p = Poweradminbf3Plugin(self.console)
        self.p._list_available_server_config_files = lambda: self.available_names

    def test_no_available_config(self):
        self.p._list_available_server_config_files = lambda: []
        self.assertListEqual([], self.p._getConfigSoundingLike(""))
        self.assertListEqual([], self.p._getConfigSoundingLike("qsfqsdf q"))

    def test_no_match(self):
        self.assertEqual(9, len(self.p._getConfigSoundingLike("qsfqsdf qqsfdsdqfqsfd qsf qsfd q fsdf")))

    def test_exact_name(self):
        self.assertListEqual(["hardcore"], self.p._getConfigSoundingLike("hardcore"))

    def test_substring_one_match(self):
        self.assertListEqual(["infantry"], self.p._getConfigSoundingLike("infan"))

    def test_substring_many_matches(self):
        self.assertListEqual(['hardcore', 'hardcore-tdm', 'hardcore-conquest'], self.p._getConfigSoundingLike("hardco"))

    def test_soundex_one_match(self):
        self.assertListEqual(['quickmatch'], self.p._getConfigSoundingLike("quickmtch"))

    def test_soundex_many_matches(self):
        self.available_names = ["wasabi21", "wasabi2", "wasabi22", "tdm", "conquest"]
        self.assertListEqual(['wasabi2', 'wasabi21', 'wasabi22'], self.p._getConfigSoundingLike("wsbi2"))

    def test_levenshteinDistance(self):
        self.assertEqual(9, len(self.p._getConfigSoundingLike("")))