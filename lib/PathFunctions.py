from re import search
class PathFunction:
    def __init__(self):
        pass
    
    def __str__(self):
        return("{}, {}, {}".format(self.slasher, self.payloader, self.urler))
    
    def slasher(self, xpath: str) -> str:
        if xpath[-1] != '/':
            ypath = xpath + '/'
        else:
            ypath = xpath
        return ypath
    
    def payloader(self, xpath: str) -> str:
        if xpath[0] == '/':
            ypath = xpath[1:]
        else:
            ypath = xpath
        return ypath

    def urler(self, xpath: str) -> str:
        if not search("^(http://.*|https://.*)", xpath):
            ypath = "http://" + xpath
        else:
            ypath = xpath
        return ypath
