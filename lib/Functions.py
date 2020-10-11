from math import log
from sys import stdin
from termcolor import colored

from lib.Globals import ColorObj
from lib.PathFunctions import PathFunction

def banner():
    banner = '\x1b[5m\x1b[1m\x1b[40m\x1b[31m   _______ __  __          __       ____             __            \n  / ____(_) /_/ /_  __  __/ /_     / __ \\____  _____/ /_____  _____\n / / __/ / __/ __ \\/ / / / __ \\   / / / / __ \\/ ___/ //_/ _ \\/ ___/\n/ /_/ / / /_/ / / / /_/ / /_/ /  / /_/ / /_/ / /  / ,< /  __/ /    \n\\____/_/\\__/_/ /_/\\__,_/_.___/  /_____/\\____/_/  /_/|_|\\___/_/     \n                                                                   \n\x1b[0m'
    print(banner)
    print(colored('Dork code, repository and commit for sensitive data!', color='red', attrs=['bold']))

def starter(argv):
    if argv.banner:
        banner()
        exit(0)
    if argv.output_directory:
        if not argv.domain:
            print("{} Output directory used without specifying domain".format(ColorObj.bad))
    if not argv.wordlist:
        if not argv.domain:
            if not argv.stdin:
                print("{} Use --help".format(ColorObj.bad))
                exit()
            else:
                return [line.rstrip('\n').strip(' ') for line in stdin.read().split('\n') if line]
        else:
            return [argv.domain]
    else:
        return [line.rstrip('\n').strip(' ') for line in open(argv.wordlist) if line]

    if not argv.user and not argv.repository:
        if not argv.domain:
            print("{} Supply user, repository or domain".format(ColorObj.bad))
            exit()

def write_output_directory(filepath, filename, towrite):
    path_fn = PathFunctions()
    f = open(path_fn.slasher(filepath) + filename + ".github", 'a')
    for data in towrite:
        for d in data:
            f.write(d)
    f.close()

def write_output(filename, towrite):
    f = open(filename, 'a')
    for data in towrite:
        for d in data:
            f.write(d)
    f.close()

def shannon_entropy(data, iterator):
    if not data:
        return 0
    entropy = 0
    for val in iterator:
        p_x = float(data.count(val))/len(data)
        if p_x > 0:
            entropy += - p_x * log(p_x, 2)
    return float(entropy)
