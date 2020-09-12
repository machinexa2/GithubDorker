from termcolor import colored
from lib.Globals import ColorObj
def banner():
    from pyfiglet import print_figlet as puff
    puff('CRLF Injector', font='larry3d', colors='BLUE')
    print(colored('A smart CRLF Injector, which can inject CRLF when given either subdomain or crawler file', color='red', attrs=['bold']))
    print(colored('It intelligently fuzzes in parameters and path', color='red', attrs=['bold']))

def starter(argv):
    if argv.banner:
        banner()
        exit(0)
    if not argv.wordlist or not argv.output_directory or not argv.threads:
        print("{} Use --help".format(ColorObj.bad))
        exit()
    if not argv.user and not argv.repository:
        if not argv.domain:
            print("{} Supply user, repository or domain".format(ColorObj.bad))
            exit()
