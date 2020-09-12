from time import time,sleep
from math import log
from re import search
from requests import get
from github import Github
from base64 import b64decode 
from os import getenv
from os import path
from bs4 import BeautifulSoup
from termcolor import colored
from json import load as jload

from lib.GithubError import InvalidArgument
from lib.Globals import ColorObj

python_dir = path.dirname(path.abspath(__file__))
with open(python_dir + '/regexes.json') as regex_file:
        regex_data = jload(regex_file)
        json_list = [json_items[1] for json_items in regex_data.items()]

class GithubDork:
    def __init__(self):
        self.conn = Github(getenv('GITHUB_ACCESS_TOKEN'))
        self.query = [] 
        self.orchestra = {'repo': False, 'code': False, 'commit': False}
        self.hexchar = "1234567890abcdefABCDEF"
        self.base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def git_rate_limit(self):
        T = time()
        left_to_try = self.conn.rate_limiting[0]
        if left_to_try <= 2:
            death_sleep = int(int(self.conn.rate_limiting_resettime)-int(T) + int(3))
            if death_sleep < 2:
                death_sleep = 7
            sleep(death_sleep)
        else:
            return 0
        sleep(0.2)

    def shannon_entropy(self, data, iterator):
        if not data:
            return 0
        entropy = 0
        for val in iterator:
            p_x = float(data.count(val))/len(data)
            if p_x > 0:
                entropy += - p_x * log(p_x, 2)
        return float(entropy)
    
    def return_query(self, input_wordlist: list, argv) -> list:
        print(f"{ColorObj.information} Generating payloads")
        if argv.repository:
            dork_type = "repo:" + argv.repository
        elif argv.user:
            dork_type = "user:" + argv.user
        elif argv.domain:
            print("EXECUTED DOMAIN")
            dork_type = argv.domain.split('.')[0] if not argv.full_domain else argv.domain
        else:
            raise InvalidArgument("{} The argument is either not supplied properly or other error occured".format(ColorObj.bad))
        for line in input_wordlist:
            print(f"{ColorObj.information} Generating payload for: {colored(line, color='cyan')}")
            git_query = dork_type + " " + line + " " + "in:readme,description,name"
            self.query.append(git_query.lstrip(' '))
        return self.query

    def search_orchestrator(self, query: str) -> dict:
        try:
            repo_search = self.conn.search_repositories(query)
            repo_count = repo_search.totalCount
            self.orchestra['repo'] = True
            self.git_rate_limit()
        except Exception as E:
            print("{} ERROR: {}".format(ColorObj.bad,E))
        try:
           code_search = self.conn.search_code(query) 
           code_count = code_search.totalCount
           self.orchestra['code'] = True
           self.git_rate_limit()
        except Exception as E:
            print("{} ERROR: {}".format(ColorObj.bad,E))
        try:
            commit_search = self.conn.search_commits(query)
            commit_count = code_search.totalCount
            self.orchestra['code'] = True
            self.git_rate_limit()
        except Exception as E:
            print("{} ERROR: {}".format(ColorObj.bad,E))
        return self.orchestra 
    
    def search_repo(self, query: str) -> list:
        repo_temp_list = []
        if self.orchestra['repo']:
            print(f"{ColorObj.information} Searching for data in Repositories!")
            repo_search = self.conn.search_repositories(query)
            self.git_rate_limit()
            for unit_repo in repo_search:
                repo = self.conn.get_repo(unit_repo.full_name)
                temp_x = "Fetching data from this repo: {}\n".format(colored(repo.full_name, color='cyan'))
                repo_temp_list.append(temp_x.lstrip(' '))
                print(ColorObj.good + " " + temp_x.rstrip('\n'))
                repo_list = repo.get_contents("")
                while repo_list:
                    repo_file = repo_list.pop(0)
                    if repo_file.type == "dir":
                        repo_list.extend(repo.get_contents(repo_file.path))
                    else:
                        try:
                            repo_file_lines = b64decode(repo_file.content).decode('UTF-8').split('\n')
                        except Exception as E:
                            print(E,E.__class__)
                            continue
                        temp_x = "File: {}\n".format(colored(repo_file, color='cyan'))
                        repo_temp_list.append(temp_x.lstrip(' '))
                        line_searched = False
                        for repo_file_line in repo_file_lines:
                            for regex in json_list:
                                if search(regex, repo_file_line):
                                    temp_x = "{:<40} <--- File from repo regex \n".format(colored(repo_file_line, color='red'))
                                    repo_temp_list.append(temp_x.lstrip(' '))
                                    line_searched = True
                            if line_searched:
                                line_searched = False
                                continue
                            for repo_file_word in repo_file_line.split(' '):
                                if self.shannon_entropy(repo_file_word, self.base64char) >= float(4):
                                    temp_x = "{:<40} <--- From Repo entropy! \n".format(colored(repo_file_word, color='red'))
                                    repo_temp_list.append(temp_x.lstrip(' '))
                                if self.shannon_entropy(repo_file_word, self.hexchar) >= float(3):
                                    temp_x = "{:<40} <--- From Repo entropy! \n".format(colored(repo_file_word, color='red'))
                                    repo_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['repo'] = False
        sleep(1)
        return repo_temp_list

    def search_code(self, query: str) -> list:
        code_temp_list = []
        if self.orchestra['code']:
            print(f"{ColorObj.information} Searching for data in Codes")
            code_search = self.conn.search_code(query) 
            for unit_code in code_search:
                temp_x = "Name:{}, Repo:{}, URL: {}\n".format(colored(unit_code.name, color='cyan'), colored(unit_code.repository.full_name, color='cyan'), colored(unit_code.download_url, color='cyan'))
                print("{} Searching for code in {} from repository {}".format(ColorObj.good, colored(unit_code.name, color='cyan'), colored(unit_code.repository.full_name, color='cyan')))
                code_temp_list.append(temp_x.lstrip(' '))
                self.git_rate_limit()
                code = b64decode(unit_code.content).decode('UTF-8').split('\n')
                line_searched = False
                for code_line in code:
                    for regex in json_list:
                        if search(regex, code_line):
                            temp_x = "{:<40} <--- File from code regex \n".format(colored(code_line, color='red'))
                            code_temp_list.append(temp_x.lstrip(' '))
                            line_searched = True
                    if line_searched:
                        line_searched = False
                        continue
                    for code_word in code_line.split(' '):
                        if self.shannon_entropy(code_word, self.base64char) >= float(4):
                            temp_x = "{:<40} <--- From code entropy! \n".format(colored(code_word, color='red'))
                            code_temp_list.append(temp_x.lstrip(' '))
                        if self.shannon_entropy(code_word, self.hexchar) >= float(3):
                            temp_x = "{:<40} <--- From code entropy! \n".format(colored(code_word, color='red'))
                            code_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['code'] = False
        sleep(1)
        return code_temp_list
    
    def search_commit(self, query: str) -> list:
        commit_temp_list = []
        if self.orchestra['commit']:
            print(f"{ColorObj.information} Searching for data in Commits")
            commit_search = self.conn.search_commit(query)
            for unit_commit in commit_search:
                commit_url = unit_commit.html_url
                temp_x = "Repo:{} Commit:{}\n".format(colored("/".join(commit_url.split('/')[3:5]), color='cyan'), colored(commit_url.split('/')[6:][-1]), color='cyan')
                print(ColorObj.good + " " + temp_x.rstrip('\n'))
                commit_temp_list.append(temp_x.lstrip(' '))
                self.git_rate_limit()
                commit_response = get(commit_url)
                commit_soup = BeautifulSoup(commit_response.content, 'html.parser')
                commit_data = commit_soup.find_all("span")
                line_searced = False
                for commit_line in commit_data:
                    for regex in json_list:
                        if search(regex, commit_line):
                            temp_x = "{:<40} <--- File from code regex \n".format(colored(commit_line, color='red'))
                            commit_temp_list.append(temp_x.lstrip(' '))
                            line_searched = True
                    if line_searched:
                        line_searched = False
                        continue
                    for commit_word in commit_line.split(' '):
                        if self.shannon_entropy(commit_word, self.base64char) >= float(4):
                            temp_x = "{:<40} <--- From code entropy! \n".format(colored(commit_word, color='red'))
                            code_temp_list.append(temp_x.lstrip(' '))
                        if self.shannon_entropy(repo_file_word, self.hexchar) >= float(3):
                            temp_x = "{:<40} <--- From code entropy! \n".format(colored(commit_word, color='red'))
                            code_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['commit'] = False
        sleep(1)
        return commit_temp_list
