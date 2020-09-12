# GithubDorker
## Description
Dork for secrets in code, commits and repositories using wordlist. Just add access_token like this `export GITHUB_ACCESS_TOKEN='dorked'` and the tool is all set.

## Features
1. Search in all places such as code, commits and repositories
2. Threaded, nice colored display and easy to use

## Usage
```
usage: GithubDorker [-h] [-w WORDLIST] [-oD OUTPUT_DIRECTORY] [-d DOMAIN] [-t THREADS] [-r REPOSITORY | -u USER] [-f] [-b]

Automatic Github Dorker

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Absolute path of wordlist
  -oD OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -t THREADS, --threads THREADS
                        Number of threads
  -r REPOSITORY, --repository REPOSITORY
                        Repository name
  -u USER, --user USER  User name
  -f, --full-domain     Use full domain
  -b, --banner          Print banner and exit

Happy Bug Hunting
```

## Example
Search using wordlist and domain name as dork string (-f optional)
* ```GithubDorker -w path/to/wordlist.txt -oD `pwd` -t 1 -d anyname.com```  
Search using wordlist and repository as dork string
* ```GithubDorker -w path/to/wordlist.txt -oD `pwd` -t 1 -d anyname.com -r machinexa2/GithubDorker```
Search using wordlist and user as dork string
* ```GithubDorker -w path/to/wordlist.txt -oD `pwd` -t 1 -d anyname.com -u machinexa2```

## Caveats
1. Some files cause unicode error and breaks it.
2. Tries to scan for secrets in non-ascii files such as binaries
