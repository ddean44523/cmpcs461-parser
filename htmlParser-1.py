
INT, FLOAT, ID, SEMICOLON, ASSIGNMENTOP, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"


class Parser:

    # WEBPAGE -> <body> { TEXT } </body>
    # TEXT -> STRING | <b> TEXT </b> | <i> TEXT </i> | <ul> { LISTITEM } </ul>
    # LISTITEM -> <li> TEXT </li>

    def __init__(self, s):
        self.s = s

    def run(self):
        pass


class Token:
    def __init__(self, s):
        self.s = s


class Lexer:
    def __init__(self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextChar(self):
        self.ch = self.stmt[self.index]
        self.index = self.index + 1 

    def nextToken(self):
        while True:
            if self.ch.isalpha():
                id = self.consumeChars(LETTERS+DIGITS)
                return Token(ID,id)
            elif self.ch.isdigit():
                num = self.consumeChars(DIGITS)
                if self.ch != ".":
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit(): 
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                else: return Token(INVALID, num)
            elif self.ch==' ': 
                self.nextChar()
            elif self.ch==';': 
                self.nextChar()
                return Token(SEMICOLON, "")
            elif self.ch==":":
                self.nextChar()
                if self.checkChar("="):
                    return Token(ASSIGNMENTOP, "")
                else: return Token(INVALID, "")
            elif self.ch=='$':
                return Token(EOI,"")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)
    
    def consumeChars(self,charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r
    
    def checkChar(self, c):
        if (self.ch==c):
            self.nextChar()
            return True
        return False

