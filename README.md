# mpyq

mpyq is a Python library for reading MPQ (MoPaQ) archives used in many of
Blizzard's games. It was originally developed for data mining Starcraft II
replay files.

In addition to being a library, mpyq also has a command line interface that
exposes some of the library's core functionality such as extracting archives.

At this early stage in development only files compressed with DEFLATE are
uncompressed. More compression formats will be supported in the future. Also,
as mpyq is so far pure Python code, it might be unfeasible to try to extract
very large MPQ archives.

## Installation

For now, mpyq is not installable as an egg or anything. This will change
in the future.

## Usage

### As a library

    >>> import mpyq
    >>> archive = mpyq.MPQArchive('game.SC2Replay')

Now you have a MPQArchive object of the file you opened. One common thing
to do now is to extract the files from the archive.

    >>> files = archive.extract()

This will extract and return the archive's contents in memory. Be advised
that you might not want to do this with multi-gigabyte MPQ files from
World of Warcraft, for example.

If you want to write the extracted files to disk, you can simply do the
following.

    >>> archive.extract_to_disk()

For more information, consult `help(mpyq)` in your Python console.

### From the command line

    Usage: mpyq.py [options] -f FILE

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -I, --headers         print header information from archive
      -t, --list-files      list files inside archive
      -x, --extract         extract files from archive
      -f FILE, --file=FILE  path to archive

You can extract all the files inside the archive from the command line.

    ./mpyq.py -xf game.SC2Replay

This will create a directory called 'game' with the files inside.

You can also print the header information from a given file.

    ./mpyq.py -If game.SC2Replay
    {'block_table_offset_high': 0,
     'extended_block_table_offset': 0,
     'block_table_offset': 65647,
     'magic': 'MPQ\x1a',
     'arhive_size': 65791,
     'format_version': 1,
     'sector_size_shift': 3,
     'header_size': 44,
     'hash_table_offset': 65391,
     'offset': 1024,
     'block_table_entries': 9,
     'user_data_header': {
       'mpq_header_offset': 1024,
       'magic': 'MPQ\x1b',
       'starcraft2_replay_header': SC2ReplayHeader(
         identifier='StarCraft II replay',
         release_flag=1,
         major_version=0,
         minor_version=11,
         maintenance_version=0,
         build_number=15133,
         duration=1304
        ),
        'content': '\x15StarCraft II replay\x1b6\x01\x00\x0b\x00\x00\x00;\x1d\x00\x00;\x1d\x02\x00\x05\x18\x03',
        'user_data_size': 512,
        'user_data_header_size': 39
      },
      'hash_table_entries': 16,
      'hash_table_offset_high': 0}

## References

The following two documents were used as references for the MPQ format:

 * [http://www.zezula.net/en/mpq/mpqformat.html](http://www.zezula.net/en/mpq/mpqformat.html)
 * [http://wiki.devklog.net/index.php?title=The_MoPaQ_Archive_Format](http://wiki.devklog.net/index.php?title=The_MoPaQ_Archive_Format)


## Copyright

Copyright 2010, Aku Kotkavuo. See LICENSE for details.
