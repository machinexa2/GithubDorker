from termcolor import colored
from sys import stdin

from lib.Globals import ColorObj

def banner():
    from pyfiglet import print_figlet as puff
    puff('Github Dorker', font='larry3d', colors='BLUE')
    print(colored('Github dorker that searches code, repositories and commit for sensitive data!', color='red', attrs=['bold']))

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
