#!/usr/bin/env python
# coding: utf-8

"""
mpyq is a Python library for reading MPQ (MoPaQ) archives.
"""

import argparse
import bz2
import cStringIO
import os
import struct
import zlib
from collections import namedtuple


__author__ = "Aku Kotkavuo"
__version__ = "0.1.2"


MPQ_FILE_IMPLODE        = 0x00000100
MPQ_FILE_COMPRESS       = 0x00000200
MPQ_FILE_ENCRYPTED      = 0x00010000
MPQ_FILE_FIX_KEY        = 0x00020000
MPQ_FILE_SINGLE_UNIT    = 0x01000000
MPQ_FILE_DELETE_MARKER  = 0x02000000
MPQ_FILE_SECTOR_CRC     = 0x04000000
MPQ_FILE_EXISTS         = 0x80000000

MPQFileHeader = namedtuple('MPQFileHeader',
    '''
    magic
    header_size
    arhive_size
    format_version
    sector_size_shift
    hash_table_offset
    block_table_offset
    hash_table_entries
    block_table_entries
    '''
)
MPQFileHeader.struct_format = '<4s2I2H4I'

MPQFileHeaderExt = namedtuple('MPQFileHeaderExt',
    '''
    extended_block_table_offset
    hash_table_offset_high
    block_table_offset_high
    '''
)
MPQFileHeaderExt.struct_format = 'q2h'

MPQUserDataHeader = namedtuple('MPQUserDataHeader',
    '''
    magic
    user_data_size
    mpq_header_offset
    user_data_header_size
    '''
)
MPQUserDataHeader.struct_format = '<4s3I'

MPQHashTableEntry = namedtuple('MPQHashTableEntry',
    '''
    hash_a
    hash_b
    locale
    platform
    block_table_index
    '''
)
MPQHashTableEntry.struct_format = '2I2HI'

MPQBlockTableEntry = namedtuple('MPQBlockTableEntry',
    '''
    offset
    archived_size
    size
    flags
    '''
)
MPQBlockTableEntry.struct_format = '4I'


class MPQArchive(object):

    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.header = self.read_header()
        self.hash_table =  self.read_table('hash')
        self.block_table = self.read_table('block')
        self.files = self.read_file('(listfile)').splitlines()

    def read_header(self):
        """Read the header of a MPQ archive."""

        def read_mpq_header(offset=None):
            if offset:
                self.file.seek(offset)
            data = self.file.read(32)
            header = MPQFileHeader._make(
                struct.unpack(MPQFileHeader.struct_format, data))
            header = header._asdict()
            if header['format_version'] == 1:
                data = self.file.read(12)
                extended_header = MPQFileHeaderExt._make(
                    struct.unpack(MPQFileHeaderExt.struct_format, data))
                header.update(extended_header._asdict())
            return header

        def read_mpq_user_data_header():
            data = self.file.read(16)
            header = MPQUserDataHeader._make(
                struct.unpack(MPQUserDataHeader.struct_format, data))
            header = header._asdict()
            header['content'] = self.file.read(header['user_data_header_size'])
            return header

        magic = self.file.read(4)
        self.file.seek(0)

        if magic == 'MPQ\x1a':
            header = read_mpq_header()
            header['offset'] = 0
        elif magic == 'MPQ\x1b':
            user_data_header = read_mpq_user_data_header()
            header = read_mpq_header(user_data_header['mpq_header_offset'])
            header['offset'] = user_data_header['mpq_header_offset']
            header['user_data_header'] = user_data_header

        return header

    def read_table(self, table_type):
        """Read either hash or block table of a MPQ archive."""

        if table_type == 'hash':
            entry_class = MPQHashTableEntry
        elif table_type == 'block':
            entry_class = MPQBlockTableEntry
        else:
            raise ValueError("Invalid table type.")

        table_offset = self.header['%s_table_offset' % table_type]
        table_entries = self.header['%s_table_entries' % table_type]
        key = self._hash('(%s table)' % table_type, 'TABLE')

        self.file.seek(table_offset + self.header['offset'])
        data = self.file.read(table_entries * 16)
        data = self._decrypt(data, key)

        def unpack_entry(position):
            entry_data = data[position*16:position*16+16]
            return entry_class._make(
                struct.unpack(entry_class.struct_format, entry_data))

        return [unpack_entry(i) for i in range(table_entries)]

    def get_hash_table_entry(self, filename):
        """Get the hash table entry corresponding to filename."""
        hash_a = self._hash(filename, 'HASH_A')
        hash_b = self._hash(filename, 'HASH_B')
        for entry in self.hash_table:
            if (entry.hash_a == hash_a and entry.hash_b == hash_b):
                return entry

    def read_file(self, filename):
        """Read a file from the MPQ archive."""

        def decompress(data):
            """Read the compression type and decompress file data."""
            compression_type = ord(data[0])
            if compression_type == 0:
                return data
            elif compression_type == 2:
                return zlib.decompress(data[1:], 15)
            elif compression_type == 16:
                return bz2.decompress(data[1:])
            else:
                raise RuntimeError("Unsupported compression type.")

        hash_entry = self.get_hash_table_entry(filename)
        block_entry = self.block_table[hash_entry.block_table_index]

        # Read the block.
        if block_entry.flags & MPQ_FILE_EXISTS:
            offset = block_entry.offset + self.header['offset']
            self.file.seek(offset)
            file_data = self.file.read(block_entry.archived_size)

            if not block_entry.flags & MPQ_FILE_SINGLE_UNIT:
                # File consist of many sectors. They all need to be
                # decompressed separately and united.
                sector_size = 512 << self.header['sector_size_shift']
                sectors = block_entry.size / sector_size + 1
                if block_entry.flags & MPQ_FILE_SECTOR_CRC:
                    crc = True
                    sectors += 1
                else:
                    crc = False
                positions = struct.unpack('<%dI' % (sectors + 1),
                                          file_data[:4*(sectors+1)])
                result = cStringIO.StringIO()
                for i in range(len(positions) - (2 if crc else 1)):
                    sector = file_data[positions[i]:positions[i+1]]
                    sector = decompress(sector)
                    result.write(sector)
                file_data = result.getvalue()
            else:
                # Single unit files only need to be decompressed, but
                # compression only happens when at least one byte is gained.
                if (block_entry.flags & MPQ_FILE_COMPRESS and
                    block_entry.size > block_entry.archived_size):
                    file_data = decompress(file_data)

            return file_data

    def extract(self):
        """Extract all the files inside the MPQ archive in memory."""
        return dict((f, self.read_file(f)) for f in self.files)

    def extract_to_disk(self):
        """Extract all files and write them to disk."""
        archive_name, extension = os.path.splitext(self.file.name)
        if not os.path.isdir(os.path.join(os.getcwd(), archive_name)):
            os.mkdir(archive_name)
        os.chdir(archive_name)
        for filename, data in self.extract().items():
            f = open(filename, 'wb')
            f.write(data)
            f.close()

    def print_headers(self):
        print "MPQ archive header"
        print "------------------"
        for key, value in self.header.iteritems():
            if key == "user_data_header":
                continue
            print "{0:30} {1!r}".format(key, value)
        if self.header['user_data_header']:
            print
            print "MPQ user data header"
            print "--------------------"
            for key, value in self.header['user_data_header'].iteritems():
                print "{0:30} {1!r}".format(key, value)

    def print_files(self):
        for filename in self.files:
            hash_entry = self.get_hash_table_entry(filename)
            block_entry = self.block_table[hash_entry.block_table_index]
            print "{0:30} {1:>8} bytes".format(filename, block_entry.size)

    def _hash(self, string, hash_type):
        """Hash a string using MPQ's hash function."""
        hash_types = {
            'TABLE_OFFSET': 0,
            'HASH_A': 1,
            'HASH_B': 2,
            'TABLE': 3
        }
        seed1 = 0x7FED7FED
        seed2 = 0xEEEEEEEE

        for ch in string:
            ch = ord(ch.upper())
            value = self.encryption_table[(hash_types[hash_type] << 8) + ch]
            seed1 = (value ^ (seed1 + seed2)) & 0xFFFFFFFF
            seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3 & 0xFFFFFFFF

        return seed1

    def _decrypt(self, data, key):
        """Decrypt hash or block table or a sector."""
        seed1 = key
        seed2 = 0xEEEEEEEE
        result = cStringIO.StringIO()

        for i in range(len(data) // 4):
            seed2 += self.encryption_table[0x400 + (seed1 & 0xFF)]
            seed2 &= 0xFFFFFFFF
            value = struct.unpack("<I", data[i*4:i*4+4])[0]
            value = (value ^ (seed1 + seed2)) & 0xFFFFFFFF

            seed1 = ((~seed1 << 0x15) + 0x11111111) | (seed1 >> 0x0B)
            seed1 &= 0xFFFFFFFF
            seed2 = value + seed2 + (seed2 << 5) + 3 & 0xFFFFFFFF

            result.write(struct.pack("<I", value))

        return result.getvalue()

    def _prepare_encryption_table():
        """Prepare encryption table for MPQ hash function."""
        seed = 0x00100001
        crypt_table = {}

        for i in range(256):
            index = i
            for j in range(5):
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp1 = (seed & 0xFFFF) << 0x10;

                seed = (seed * 125 + 3) % 0x2AAAAB
                temp2 = (seed & 0xFFFF)

                crypt_table[index] = (temp1 | temp2)

                index += 0x100

        return crypt_table

    encryption_table = _prepare_encryption_table()


def main():
    description = "mpyq reads and extracts MPQ archives."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", action="store", help="path to the archive")
    parser.add_argument("-I", "--headers", action="store_true", dest="headers",
                        help="print header information from the archive")
    parser.add_argument("-t", "--list-files", action="store_true", dest="list",
                        help="list files inside the archive")
    parser.add_argument("-x", "--extract", action="store_true", dest="extract",
                        help="extract files from the archive")
    args = parser.parse_args()
    if args.file:
        archive = MPQArchive(args.file)
        if args.headers:
            archive.print_headers()
        if args.list:
            archive.print_files()
        if args.extract:
            archive.extract_to_disk()


if __name__ == '__main__':
    main()
