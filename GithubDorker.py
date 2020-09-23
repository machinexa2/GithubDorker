#!/usr/bin/python3
from argparse import ArgumentParser
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

from lib.Globals import ColorObj
from lib.Functions import starter
from lib.GithubDorker import GithubDork
from lib.PathFunctions import PathFunction

parser = ArgumentParser(description=colored('Automatic Github Dorker', color='yellow'), epilog=colored("Happy Bug Hunting", color='yellow'))
group = parser.add_mutually_exclusive_group()
group_two = parser.add_mutually_exclusive_group()
group_two.add_argument('---', '---', type=str,dest="stdin", help='Stdin')
parser.add_argument('-w', '--wordlist', type=str, help='Wordlist')
parser.add_argument('-oD', '--output-directory', type=str, help='Output directory')
parser.add_argument('-d', '--domain', type=str, help='Domain name')
parser.add_argument('-t', '--threads', type=int, help='Number of threads')
group.add_argument('-r', '--repository', type=str, help='Repository name')
group.add_argument('-u', '--user', type=str, help='User name')
parser.add_argument('-f', '--full-domain', action="store_true", help='Use full domain')
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

FPathApp = PathFunction()
GithubApp = GithubDork()
input_wordlist = starter(argv)
if argv.output_directory:
    git_save = open(FPathApp.slasher(argv.output_directory) + argv.domain + ".gitdork", 'a')

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
        GitRepo = GithubApp.search_repo(Query)
        GitCode= GithubApp.search_code(Query)
        GitCommit= GithubApp.search_commit(Query)
        if argv.output_directory:
            for write in GitRepo:
                git_save.write(write)
            for write in GitCode:
                git_save.write(write)
            for write in GitCommit:
                git_save.write(write)
    #with ThreadPoolExecutor(max_workers=argv.threads) as executor:
    #    executor.map(search_all, input_wordlist)

main()
