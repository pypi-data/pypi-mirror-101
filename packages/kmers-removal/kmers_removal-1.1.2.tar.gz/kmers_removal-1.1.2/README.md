# kmers_removal

Small example of how a list of kmers (specified in a .txt file) can be removed from a genome assembly

# Requirements

- python 3
- pip

# Installation 

```console
git clone https://github.com/GDelevoye/kmers_removal.git
pip install -e ./kmers_removal
```

# Run tests

Only a terminal test is implemented by now. It is implemented with pytest

```console 

guillaume@A320MA:~/GitHub/kmers_removal$ pytest .
===================== test session starts =====================
platform linux -- Python 3.8.5, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/guillaume/GitHub/kmers_removal
collected 1 item                                              

test/test_kmers_removal_launcher.py .                   [100%]

====================== 1 passed in 0.33s ======================

```

# Usage 

```console 
guillaume@A320MA:~$ kmers_removal --help
usage: kmers_removal [-h] --fastaFile FASTAFILE --kmerFile KMERFILE --output
                     OUTPUT
                     [--verbosity {NONE,DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [--report REPORT]

Allows to remove a given list of kmers in a genome assembly

optional arguments:
  -h, --help            show this help message and exit
  --fastaFile FASTAFILE, -f FASTAFILE
                        Input .fasta file where kmers must be removed
  --kmerFile KMERFILE, -k KMERFILE
                        Path to a file with 1 kmer to remove per line (can be
                        list of files). Must contain onlyupper A, T, C or G
                        and \n
  --output OUTPUT, -o OUTPUT
                        output .fa file
  --verbosity {NONE,DEBUG,INFO,WARNING,ERROR,CRITICAL}, -v {NONE,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Choose your verbosity on stdout. Default: INFO. If
                        verbosity < INFO, no progress_bar is displayed.
  --report REPORT, -r REPORT
                        [FACULTATIVE - DEFAULT is None] Path to a report of
                        the kmers encountered
```

# Credits

Guillaume Delevoye 2021
