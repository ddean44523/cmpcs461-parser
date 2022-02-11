import sys
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
METACHARS = "</bodyuliEOI" #we don't want the > so that we dont accidently take more than we want
TAGS = ["<b>","<i>","<body>","<li>","<ul>"]
ENDTAGS = ["</b>","</i>","</body>","</li>","</ul>","<EOI>"]
TAGSMATCH = {
    "</b>": "<b>"
    ,"</i>" :"<i>"
    ,"</body>":"<body>"
    ,"</li>":"<li>"
    ,"</ul>" : "<ul>"
}
GRAMMAR = {
    "WEBPAGE":["<body>"],
    "<body>":["<body>","<b>","<i>","<ul>"],
    "<ul>": ["<li>"],
    "<li>":["<b>","<i>","<ul>"],
    "<b>": ["<i>","<b>","<ul>"],
    "<i>":["<i>","<b>","<ul>"]
}


class Token:
    "A class for representing Tokens"
    def __init__ (self, s):
        self.stmt = s
        self.type = "INVALID"
        self.type = self.typer()
        self.level = 0
        
    def getToken(self):
        return self.stmt
    
    def getType(self):
        return self.type
    
    def typer(self):
        if self.isTag():
            if self.stmt in ENDTAGS:
                if self.stmt == "<EOI>":
                    return "EOI"
                return  "ENDTAG"
            else:
                return  "TAG"
        else:
            for i in self.stmt:
                if i not in LETTERS+DIGITS:
                    return "INVALID"
            return "TEXT"
        
    def isTag(self):
        return self.stmt in TAGS + ENDTAGS
    
    def isType(self, check):
        if self.type == check: return True
        return False
    
    def __repr__(self):
        return self.type + " token: " + self.stmt  

class Lexer:
    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__ (self, s):
        self.stmt = s + "<EOI>"
        self.index = 0
        self.nextChar()
        
    def nextToken(self):
        while 1:
            if self.checkChar("<"):
                return (self.consumeChars(METACHARS))
            elif self.ch in LETTERS+DIGITS:
                return (self.consumeChars(LETTERS+DIGITS))
            else:
                self.nextChar()
            
    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1
        if self.index >= len(self.stmt):
            self.index = 0
            
    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        if charSet == METACHARS:
            r += ">"
            if self.index < len(self.stmt):
                self.nextChar()
        return r
    
    def checkChar(self, c):
        if (self.ch==c):
            return True
        return False

class Parser:
    """ parses input text in accordance to the following grammar.
       | WEBPAGE -> <body> { TEXT } </body>
       | TEXT -> STRING | <b> TEXT </b> | <i> TEXT </i> | <ul> { LISTITEM } </ul>
       | LISTITEM -> <li> TEXT </li>
       | STRING -> LETTER | DIGIT    """
    
    def __init__(self, s):
        self.lexer = Lexer(s)
        self.tokenList = self.toList()
        self.token = self.tokenList[0]
        self.cur_level = 0
        
    def toList(self):
        """Makes a list of tokens from the string passed as a parameter"""
        words = []
        while True:
            tok = self.lexer.nextToken()
            words.append(Token(tok))
            if tok == "<EOI>":
                break
        return words
        
    def parse(self):
        """Prints the text with correct indentation & returns 0 so long as there's no errors"""
        last_tag = Token("WEBPAGE")
        stack = []
        for tok in self.tokenList:
            if tok.getType() == "TAG":
                #We are dealing with the start tag & must increment the level of indentation 
                if tok.getToken() not in GRAMMAR[last_tag.getToken()]:
                    self.error_message(tok,last_tag)
                    sys.exit(1)
                print("\t"*self.cur_level + tok.getToken())
                self.cur_level +=1
                stack.append(tok.getToken())
                last_tag = tok
            elif tok.getType() == "ENDTAG":
                self.cur_level -= 1
                match = stack.pop()
                if (match != TAGSMATCH[tok.getToken()]):
                    #stack error requires a different exit message 
                    # the indices of TAGS & ENDTAGS match 
                    print(f"Syntax error: expecting {ENDTAGS[TAGS.index(match)]}; saw {TAGSMATCH[tok.getToken()]}." )
                    sys.exit(1)
                print("\t"*self.cur_level + tok.getToken())
            elif tok.getType() == "INVALID":
                print(f"Syntax error: the token {tok.getToken()} is not recognized.")
                sys.exit(1)
            elif tok.getType() == "EOI":
                #The parse was successful
                return 0
            else:
                #STRINGS
                print("\t"*self.cur_level + tok.getToken())
        
    def error_message(self,current_token,last_token):
        #if we don't start with <body>
        #if we go to wrong token catagory 
        if current_token.getToken() not in GRAMMAR[last_token.getToken()]:
            if last_token.getToken() == "WEBPAGE":
                print(f"Syntax error: expecting <body>; saw {current_token.getToken()}.")
                sys.exit(1)
            if last_token.getToken() == "<ul>":
                print(f"Syntax error: expecting <li>; saw {current_token.getToken()}.")
                sys.exit(1)
            if last_token.getToken() in GRAMMAR:
                print(f"Syntax error: expecting <b>, <i>, <ul>, STRING; saw {current_token.getToken()}.")
                sys.exit(1)
            #worst case is that we get this error
            print("Unexpected Error")
            sys.exit(1)
    
    def run(self):
        self.parse()
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
    '''A class for representing Tokens'''
    # a Token object has two fields: the token's type and its value
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal
        
    def getTokenType(self):
        return self.type
    
    def getTokenValue(self):
        return self.val
    
    
    def __repr__(self):
        if (self.type in [INT, FLOAT, ID]): 
            return self.val
        elif (self.type == BODY):
            return "<body>"
        elif (self.type == BOLD):
            return "<b>"
        elif (self.type == ITALIC):
            return "<i>"
        elif (self.type == UNORDEREDLIST):
            return "<ul>"
        elif (self.type == LIST):
            return "<li>"
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"



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

