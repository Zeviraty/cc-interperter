import sys
from enum import Enum
from collections import deque
from decimal import Decimal

global Errors
Errors = []
global Line
Line = 1

class TokenType(Enum):
    LEFT_PAREN    = "("
    RIGHT_PAREN   = ")"
    LEFT_BRACE    = "{"
    RIGHT_BRACE   = "}"
    SEMICOLON     = ";"
    COMMA         = ","
    PLUS          = "+"
    MINUS         = "-"
    STAR          = "*"
    BANG_EQUAL    = "!="
    BANG          = "!"
    EQUAL_EQUAL   = "=="
    EQUAL         = "="
    LESS_EQUAL    = "<="
    GREATER_EQUAL = ">="
    LESS          = "<"
    GREATER       = ">"
    SLASH         = "/"
    DOT           = "."
    EOF           = None
    ERROR         = "ERROR"
    STRING        = "STRINGDATA"
    NUMBER        = "NUMBERDATA"
    IDENTIFIER    = "IDENTITYDATA"

    @classmethod
    def _missing_(cls, value):
        global Errors
        Errors.append((Line,value,ErrorType.UNEXPECTED))

class ErrorType(Enum):
    UNEXPECTED          = 0
    UNTERMINATED_STRING = 1

class LookaheadIterator:
    def __init__(self, iterable):
        self.iter = iter(iterable)
        self.buffer = deque()

    def peek(self):
        if not self.buffer:
            try:
                self.buffer.append(next(self.iter))
            except StopIteration:
                return None
        return self.buffer[0]

    def next(self):
        if self.buffer:
            return self.buffer.popleft()
        try:
            return next(self.iter)
        except StopIteration:
            return None

def scantoken(chars):
    global Line
    global Errors
    c = chars.next()
    if c == None:
        return (TokenType.EOF,None)
    if c == "\n":
        Line += 1
        return ("",None)
    if c in "!=<>":
        next_c = chars.peek()
        if next_c == '=':
            c += chars.next()
    if c == " " or c == "\t":
        return ("",None)
    if c == '"':
        building = ""
        while True:
            c = chars.next()
            if c == '"':
                return (TokenType.STRING,building)
            elif c == None:
                Errors.append((Line,None,ErrorType.UNTERMINATED_STRING))
                return (TokenType.EOF,None)
            elif c == "\n":
                Errors.append((Line,None,ErrorType.UNTERMINATED_STRING))
                Line += 1
                return ("",None)
            else:
                building += c
    if c.isdigit():
        building = c
        has_decimal = False
        while True:
            c = chars.peek()
            if c is None or not (c.isdigit() or (c == "." and not has_decimal)):
                break
            if c == ".":
                if has_decimal:
                    return (TokenType.NUMBER, Decimal(building),True)
            c = chars.next()
            if c == ".":
                has_decimal = True
            building += c
        return (TokenType.NUMBER, Decimal(building),False)
    if c == '/':
        next_c = chars.peek()
        if next_c == '/':
            while chars.next() not in ("\n",None): pass
            Line += 1
            return ("",None)
    if c in list(TokenType):
        try:
            return (TokenType(c),None)
        except:
            pass
    else:
        if c == None:
            return (TokenType.EOF,None)
        if c not in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
            return (TokenType.ERROR,None)
        building = c
        while True:
            c = chars.peek()
            if c == None:
                return (TokenType.IDENTIFIER,"")
            c = chars.next()
            if c not in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                return (TokenType.IDENTIFIER,building)
            building += c
        return (TokenType.ERROR,None)

def main():
    global Errors
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
        chars = LookaheadIterator(file_contents)

    if file_contents:
        Tokens = []
        token = [None,None]
        while token[0] != TokenType.EOF:
            token = scantoken(chars)
            if token[0] != "":
                Tokens.append(token)
        for error in Errors:
            if error[2].name == "UNEXPECTED":
                print(f"[line {error[0]}] Error: Unexpected character: {error[1]}",file=sys.stderr)
            if error[2].name == "UNTERMINATED_STRING":
                print(f"[line {error[0]}] Error: Unterminated string.",file=sys.stderr)
        for full in Tokens:
            token = full[0]
            data = full[1]
            if token.name == "ERROR":
                continue
            if token.name == "STRING":
                print(f"STRING \"{data}\" {data}")
                continue
            if token.name == "NUMBER":
                if full[2] == False:
                    print(f"NUMBER {data if not str(data).endswith('.0') else int(data)} {float(data)}")
                else:
                    print(f"NUMBER {data if not str(data).endswith('.0') else int(data)} {float(data)}")
                continue
            if token.name == "IDENTIFIER":
                print(f"IDENTIFIER {data} null")
                continue
            print(f"{token.name} {token.value if token.value != None else ''} null")
        if len(Errors) != 0:
            exit(65)
    else:
        print("EOF  null")

if __name__ == "__main__":
    main()
