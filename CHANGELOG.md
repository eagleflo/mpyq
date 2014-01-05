# CHANGE LOG

### 0.2.4 - Released 2014-01-05

 * Fixed bug in multi-sector block decompression

### 0.2.3 - Released 2013-07-31

 * Fixed division bug with Python3 compatibility

### 0.2.2 - Released 2013-04-08

 * Added Python3 support

### 0.2.1 - Released 2013-02-25

 * Now properly writes empty archive files to disk
 * Improved handling of invalid archive files, now raises ValueError

### 0.2.0 - Released 2011-09-26

 * Allow for MPQ file extraction to current directory
 * Returns None when reading empty files from the archive

### 0.1.11 - Released 2011-09-20

 * Automatically install argparse dependency during install

### 0.1.10 - Released 2011-09-20

 * Fixes bug when using force_decompress option on a multi-sector block

### 0.1.9 - Released 2011-09-18

 * Introduces force_decompress option. This flexibility allows for reading
   files from some otherwise corrupted MPQ files.
 * Fixes print_headers for archives without user_data_header
 * Improves formatting of print_file command

### 0.1.8 - Released 2011-03-28

 * Adds support for opening any file-like object (objects implementing .read())
 * Returns None when attempting to read missing or non-existant file from
   archive

### 0.1.7 - Released 2011-03-08

 * Adds support for opening archives from opened file objects
 
### 0.1.6 - Released 2011-03-03

 * Fixes decompression bug for multi-sector blocks

### 0.1.5 - Released 2011-03-01

 * Adds option to skip/ignore the list file. Allows reading when listfile has
   been encrypted or tampered with when you already know what you are looking
   for.

### 0.1.4 - Released 2011-02-28

 * Raises NotImplementedError when attempting to read encrypted files from
   archives

### 0.1.3 - Released 2011-02-26

 * Adds print_hash_table and print_block_table commands

### 0.1.2 - Released 2011-02-24

 * Fixed UnboundLocalError in read_file

### 0.1.1 - Released 2011-01-05

 * Fixed installation layout
 * Added minimal regression test

### 0.1.0 - Released 2010-09-05

 * Released on PyPI for the first time

### Initial Release - 2010-05-15

