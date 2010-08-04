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

    usage: mpyq.py [-h] [-I] [-t] [-x] file

    mpyq reads and extracts MPQ archives.

    positional arguments:
      file              path to the archive

    optional arguments:
      -h, --help        show this help message and exit
      -I, --headers     print header information from the archive
      -t, --list-files  list files inside the archive
      -x, --extract     extract files from the archive

You can extract all the files inside the archive from the command line.

    ./mpyq.py -x game.SC2Replay

This will create a directory called 'game' with the files inside.

You can also print the header information from a given file.

    ./mpyq.py -I game.SC2Replay
    MPQ archive header
    ------------------
    magic                          'MPQ\x1a'
    header_size                    44
    arhive_size                    299391
    format_version                 1
    sector_size_shift              3
    hash_table_offset              298975
    block_table_offset             299231
    hash_table_entries             16
    block_table_entries            10
    extended_block_table_offset    0
    hash_table_offset_high         0
    block_table_offset_high        0
    offset                         1024

    MPQ user data header
    --------------------
    magic                          'MPQ\x1b'
    user_data_size                 512
    mpq_header_offset              1024
    user_data_header_size          60
    content                        '\x05\x08\x00\x02,StarCraft II replay\x1b11\x02\x05\x0c\x00\t\x02\x02\t\x02\x04\t\x00\x06\t\x00\x08\t\xea\xfb\x01\n\t\xda\xf0\x01\x04\t\x04\x06\t\xfe\x9e\x05'

## References

The following two documents were used as references for the MPQ format:

 * [http://www.zezula.net/en/mpq/mpqformat.html](http://www.zezula.net/en/mpq/mpqformat.html)
 * [http://wiki.devklog.net/index.php?title=The_MoPaQ_Archive_Format](http://wiki.devklog.net/index.php?title=The_MoPaQ_Archive_Format)


## Copyright

Copyright 2010, Aku Kotkavuo. See LICENSE for details.
