from re import search
from requests import get
from github import Github
from time import time,sleep
from base64 import b64decode 
from bs4 import BeautifulSoup
from termcolor import colored

from lib.Globals import hexchar, base64char
from lib.Globals import ColorObj, search_regex
from lib.Globals import github_access_token, Headers
from lib.Functions import shannon_entropy

class GithubDork:
    def __init__(self):
        self.conn = Github(github_access_token)
        self.query = [] 
        self.orchestra = {'repo': False, 'code': False, 'commit': False}

    def git_rate_limit(self):
        T = time()
        left_to_try = self.conn.rate_limiting[0]
        if left_to_try <= 2:
            death_sleep = int(int(self.conn.rate_limiting_resettime)-int(T) + int(3))
            if death_sleep < 2:
                death_sleep = 7
            sleep(death_sleep)
        else:
            return
        sleep(0.2)
        
    def return_query(self, input_wordlist: list, argv) -> list:
        print(f"{ColorObj.information} Generating payloads")
        if argv.repository:
            dork_type = "repo:" + argv.repository
        elif argv.user:
            dork_type = "user:" + argv.user
        elif argv.domain:
            dork_type = argv.domain.split('.')[0] if not argv.full_domain else argv.domain
        else:
            assert False, "Error occured"
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
                        for repoline in repo_file_lines:
                            for regex in search_regex:
                                if search(regex, repoline):
                                    temp_x = f"{colored(repoline, color='red')} "
                                    temp_x += "<--- File from repo regex \n".rjust(150-len(temp_x))
                                    repo_temp_list.append(temp_x.lstrip(' '))
                                    line_searched = True
                            if line_searched:
                                line_searched = False
                                continue
                            for repoword in repoline.split(' '):
                                temp_x = f"{colored(repoword, color='red')} "
                                temp_x += "<--- From Repo entropy! \n".rjust(150-len(temp_x))
                                if shannon_entropy(repoword, base64char) >= float(4.5):
                                    repo_temp_list.append(temp_x.lstrip(' '))
                                if shannon_entropy(repoword, hexchar) >= float(4.1):
                                    repo_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['repo'] = False
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
                    for regex in search_regex:
                        if search(regex, code_line):
                            temp_x = f"{colored(code_line, color='red')} "
                            temp_x += " <--- File from code regex \n".rjust(150-len(temp_x))
                            code_temp_list.append(temp_x.lstrip(' '))
                            line_searched = True
                    if line_searched:
                        line_searched = False
                        continue
                    for code_word in code_line.split(' '):
                        temp_x = f"{colored(code_word, color='red')} "
                        temp_x += "<--- From code entropy! \n".rjust(150-len(temp_x))
                        if shannon_entropy(code_word, base64char) >= float(4.6):
                            code_temp_list.append(temp_x.lstrip(' '))
                        if shannon_entropy(code_word, hexchar) >= float(4):
                            code_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['code'] = False
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
                    for regex in search_regex:
                        if search(regex, commit_line):
                            temp_x = f"{colored(commit_line, color='red')}" 
                            temp_x += "<--- File from commit regex \n".rjust(148-len(temp_x))
                            commit_temp_list.append(temp_x.lstrip(' '))
                            line_searched = True
                    if line_searched:
                        line_searched = False
                        continue
                    for commit_word in commit_line.split(' '):
                        temp_x = f"{colored(commit_word, color='red')} "
                        temp_x += "<--- From commit entropy! \n".rjust(148-len(temp_x))
                        if shannon_entropy(commit_word, base64char) >= float(4.6):
                            code_temp_list.append(temp_x.lstrip(' '))
                        if shannon_entropy(commit_word, hexchar) >= float(4.1):
                            code_temp_list.append(temp_x.lstrip(' '))
        self.orchestra['commit'] = False
        return commit_temp_list
