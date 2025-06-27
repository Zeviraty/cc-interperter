import sys
from enum import Enum
from collections import deque

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
    STRING        = "MODULAR"

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
        return ""
    if c in "!=<>":
        next_c = chars.peek()
        if next_c == '=':
            c += chars.next()
    if c == " " or c == "\t":
        return ""
    if c == '"':
        building = ""
        while True:
            c = chars.next()
            if c == '"':
                return (TokenType.STRING,building)
            elif c == None:
                Errors.append((Line,None,ErrorType.UNTERMINATED_STRING))
            else:
                building += c
    if c == '/':
        next_c = chars.peek()
        if next_c == '/':
            while chars.next() not in ("\n",None): pass
            Line += 1
            return ""
    try:
        return (TokenType(c),None)
    except:
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
        token = None
        while token != TokenType.EOF:
            token = scantoken(chars)
            if token != "":
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
                print("STRING \"{data}\" {data}")
                continue
            print(f"{token.name} {token.value if token.value != None else ''} null")
        if len(Errors) != 0:
            exit(65)
    else:
        print("EOF  null")

if __name__ == "__main__":
    main()
