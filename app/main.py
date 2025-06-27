import sys
from enum import Enum
from collections import deque

class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    SEMICOLON = ";"
    COMMA = ","
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    BANG_EQUAL = "!="
    EQUAL_EQUAL = "=="
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    LESS = "<"
    GREATER = ">"
    SLASH = "/"
    DOT = "."
    EOF = None

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
    c = chars.next()
    if c == None:
        return TokenType.EOF
    if c == "\n":
        return ""
    if c in "!=<>":
        next_c = chars.peek()
        if next_c == '=':
            c += chars.next()
    return TokenType(c)

def main():
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
        token = None
        while token != TokenType.EOF:
            token = scantoken(chars)
            if token != "":
                print(f"{token.name} {token.value if token.value != None else ""} null")
    else:
        print("EOF  null")

if __name__ == "__main__":
    main()
