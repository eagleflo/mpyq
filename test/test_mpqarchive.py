#!/usr/bin/env python
# coding: utf-8

import os
import unittest
from tempfile import mkdtemp
from shutil import rmtree

try:
    from unittest import mock  # Python 3+
except ImportError:
    import mock  # Python 2.7

from mpyq import MPQArchive
import six

TEST_DIR = os.path.realpath(os.path.dirname(__file__)) + '/'

class TestMPQArchive(unittest.TestCase):

    def setUp(self):
        self.archive = MPQArchive(TEST_DIR + 'test.SC2Replay')

    def tearDown(self):
        self.archive.close()
        self.archive = None

    def test_init_with_file(self):
        self.archive = MPQArchive(open(TEST_DIR + 'test.SC2Replay', 'rb'))

    def test_header(self):
        self.assertEqual(self.archive.header['magic'], b'MPQ\x1a')
        self.assertEqual(self.archive.header['header_size'], 44)
        self.assertEqual(self.archive.header['archive_size'], 205044)
        self.assertEqual(self.archive.header['format_version'], 1)
        self.assertEqual(self.archive.header['sector_size_shift'], 3)
        self.assertEqual(self.archive.header['hash_table_offset'], 204628)
        self.assertEqual(self.archive.header['block_table_offset'], 204884)
        self.assertEqual(self.archive.header['hash_table_entries'], 16)
        self.assertEqual(self.archive.header['block_table_entries'], 10)
        self.assertEqual(self.archive.header['extended_block_table_offset'], 0)
        self.assertEqual(self.archive.header['hash_table_offset_high'], 0)
        self.assertEqual(self.archive.header['block_table_offset_high'], 0)
        self.assertEqual(self.archive.header['offset'], 1024)

    def test_files(self):
        self.assertEqual(self.archive.files, [b'replay.attributes.events',
                                              b'replay.details',
                                              b'replay.game.events',
                                              b'replay.initData',
                                              b'replay.load.info',
                                              b'replay.message.events',
                                              b'replay.smartcam.events',
                                              b'replay.sync.events'])

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def test_print_hash_table(self, mock_stdout):
        self.archive.print_hash_table()
        self.assertEqual(mock_stdout.getvalue(),
                         "MPQ archive hash table\n"
                         "----------------------\n"
                         " Hash A   Hash B  Locl Plat BlockIdx\n"
                         "D38437CB 07DFEAEC 0000 0000 00000009\n"
                         "AAC2A54B F4762B95 0000 0000 00000002\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "C9E5B770 3B18F6B6 0000 0000 00000005\n"
                         "343C087B 278E3682 0000 0000 00000004\n"
                         "3B2B1EA0 B72EF057 0000 0000 00000006\n"
                         "5A7E8BDC FF253F5C 0000 0000 00000001\n"
                         "FD657910 4E9B98A7 0000 0000 00000008\n"
                         "D383C29C EF402E92 0000 0000 00000000\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "FFFFFFFF FFFFFFFF FFFF FFFF FFFFFFFF\n"
                         "1DA8B0CF A2CEFF28 0000 0000 00000007\n"
                         "31952289 6A5FFAA3 0000 0000 00000003\n"
                         "\n")

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def test_print_block_table(self, mock_stdout):
        self.archive.print_block_table()
        self.assertEqual(mock_stdout.getvalue(),
                         "MPQ archive block table\n"
                         "-----------------------\n"
                         " Offset  ArchSize RealSize  Flags\n"
                         "0000002C      727      890 81000200\n"
                         "00000303      801     1257 81000200\n"
                         "00000624   194096   479869 81000200\n"
                         "0002FC54      226      334 81000200\n"
                         "0002FD36       97       97 81000200\n"
                         "0002FD97     1323     1970 81000200\n"
                         "000302C2     6407    12431 81000200\n"
                         "00031BC9      533     2400 81000200\n"
                         "00031DDE      120      164 81000200\n"
                         "00031E56      254      288 81000200\n"
                         "\n")

class TestSC2Map(unittest.TestCase):

    def setUp(self):
        self.archive = MPQArchive(TEST_DIR + 'CollectMineralShards.SC2Map')

    def tearDown(self):
        self.archive.close()
        self.archive = None

    def test_init_with_file(self):
        self.archive = MPQArchive(open(TEST_DIR + 'CollectMineralShards.SC2Map', 'rb'))

    def test_extract_all(self):
        temp_dir = mkdtemp()
        self.archive.extract_to_disk(target_dir=temp_dir)
        rmtree(temp_dir)

    def test_extract_some_to_disk(self):
        temp_dir = mkdtemp()
        self.archive.extract_to_disk(b'DocumentInfo', b'Regions', target_dir=temp_dir)
        rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
