#!/usr/bin/python3
from argparse import ArgumentParser
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

from lib.Globals import ColorObj
from lib.Functions import starter
from lib.Functions import write_output, write_output_directory
from lib.GithubDorker import GithubDork

parser = ArgumentParser(description=colored('Automatic Github Dorker', color='yellow'), epilog=colored("Happy Bug Hunting", color='yellow'))
input_group = parser.add_mutually_exclusive_group()
input_mode_group = parser.add_mutually_exclusive_group()
output_group = parser.add_mutually_exclusive_group()

input_group.add_argument('---', '---', action="store_true", dest="stdin", help='Stdin')
input_group.add_argument('-w', '--wordlist', type=str, help='Dorks wordlist')
output_group.add_argument('-oD', '--output-directory', type=str, help='Output directory')
output_group.add_argument('-o', '--output', type=str, help='Output directory')
parser.add_argument('-d', '--domain', type=str, help='Domain name')
parser.add_argument('-t', '--threads', type=int, help='Number of threads')
input_mode_group.add_argument('-r', '--repository', type=str, help='Repository name')
input_mode_group.add_argument('-u', '--user', type=str, help='User name')
parser.add_argument('-f', '--full-domain', action="store_true", help='Use full domain')
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

GithubApp = GithubDork()
input_wordlist = starter(argv)

def main():
    try:
        GitQueries = GithubApp.return_query(input_wordlist, argv)
    except Exception as E:
        print(f"{ColorObj.bad} Error: {E},{E.__class__} Exiting!")
        exit()
    for Query in GitQueries:
        print("{} Dorking Github using: {}".format(ColorObj.information, colored(Query, color='cyan')))
        try:
            GithubApp.search_orchestrator(Query)
        except Exception as E:
            print(E,E.__class__)
        git_repo = GithubApp.search_repo(Query)
        git_code= GithubApp.search_code(Query)
        git_commit= GithubApp.search_commit(Query)
        git_list = [git_repo, git_code, git_commit] #lists list
        if argv.output_directory:
            write_output_directory(argv.output_directory, argv.domain, git_list)
        if argv.output:
            if git_list:
                write_output(argv.output, git_list)

if __name__ == "__main__":
    main()

#with ThreadPoolExecutor(max_workers=argv.threads) as executor:
#    executor.map(search_all, input_wordlist)

