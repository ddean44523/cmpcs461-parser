class Parser:

    #WEBPAGE -> <body> { TEXT } </body>
    #TEXT -> STRING | <b> TEXT </b> | <i> TEXT </i> | <ul> { LISTITEM } </ul>
    #LISTITEM -> <li> TEXT </li>


    def __init__(self, s):
        self.s=s
    
    def run(self):
        pass
    

class Token:
    def __init__(self):
        pass

class Lexer:
    def __init__(self):
        pass

