#!/usr/bin/env python
# coding: utf-8

import os
import unittest
from mpyq import MPQArchive

TEST_DIR = os.path.realpath(os.path.dirname(__file__)) + '/'

class TestMPQArchive(unittest.TestCase):

    def setUp(self):
        self.archive = MPQArchive(TEST_DIR + 'test.SC2Replay')

    def test_header(self):
        self.assertEqual(self.archive.header['magic'], 'MPQ\x1a')
        self.assertEqual(self.archive.header['header_size'], 44)
        self.assertEqual(self.archive.header['arhive_size'], 205044)
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
        self.assertEqual(self.archive.files, ['replay.attributes.events',
                                              'replay.details',
                                              'replay.game.events',
                                              'replay.initData',
                                              'replay.load.info',
                                              'replay.message.events',
                                              'replay.smartcam.events',
                                              'replay.sync.events'])
