
class Dfa:
    def __init__(self, sts, alph, trans, start, accStates):
        self.sts = sts
        self.alph = alph
        self.trans = trans
        self.start = start
        self.accStates = accStates

    def procStr(self, inpStr):
        curState = self.start
        lex = ""
        lastAccState = None
        lastLex = ""
        
        for sym in inpStr:
            if sym not in self.alph:
                break  
            nxtState = self.trans.get((curState, sym))
            if nxtState is None:
                break  
            curState = nxtState
            lex += sym
            if curState in self.accStates:
                lastAccState = curState
                lastLex = lex
        
        if lastAccState is None:
            raise ValueError("No valid token found in input")
        
        tokType = self.accStates[lastAccState]
        return tokType, lastLex


# Dfa for ids (matches a letter followed by letters/digits)
idSts = {"start", "inId"}
idAlph = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
idTrans = {}
for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
    idTrans[("start", letter)] = "inId"
for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    idTrans[("inId", char)] = "inId"
idStart = "start"
idAccStates = {"inId": "id"}
idDfa = Dfa(idSts, idAlph, idTrans, idStart, idAccStates)


# Dfa for nums (matches one or more digits)
numSts = {"start", "inNum"}
numAlph = set("0123456789")
numTrans = {}
for digit in "0123456789":
    numTrans[("start", digit)] = "inNum"
for digit in "0123456789":
    numTrans[("inNum", digit)] = "inNum"
numStart = "start"
numAccStates = {"inNum": "num"}
numDfa = Dfa(numSts, numAlph, numTrans, numStart, numAccStates)


# Lexer class using DFAs and table-driven approach for opperators and keywords
class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.toks = []
        # Keywords per project reqs
        self.kws = {"int", "return", "if", "switch", "float", "while", 
                    "else", "case", "char", "for", "goto", "unsigned", 
                    "main", "break", "continue", "void"}

    def nextChar(self):
        if self.pos < len(self.src):
            ch = self.src[self.pos]
            self.pos += 1
            return ch
        return None

    def peekChar(self):
        if self.pos < len(self.src):
            return self.src[self.pos]
        return None

    def lex(self):
        while self.pos < len(self.src):
            ch = self.peekChar()
            if ch.isspace():
                self.pos += 1
                continue
            # Handle comments: skip '//' until newline
            if ch == '/' and self.pos + 1 < len(self.src) and self.src[self.pos+1] == '/':
                self.lexComment()
                continue
            if ch.isalpha():
                tok, lex = self.lexId()
                if lex in self.kws:
                    tok = lex  # Token is the lexeme for keywords
                self.toks.append((tok, lex))
                continue
            if ch.isdigit():
                tok, lex = self.lexNum()
                self.toks.append((tok, lex))
                continue
            tok, lex = self.lexOpSep()
            self.toks.append((tok, lex))
        return self.toks

    def lexId(self):
        substr = ""
        while self.pos < len(self.src) and self.src[self.pos].isalnum():
            substr += self.src[self.pos]
            self.pos += 1
        tok, lex = idDfa.procStr(substr)
        return tok, lex

    def lexNum(self):
        substr = ""
        while self.pos < len(self.src) and self.src[self.pos].isdigit():
            substr += self.src[self.pos]
            self.pos += 1
        tok, lex = numDfa.procStr(substr)
        return tok, lex

    def lexOpSep(self):
        ch = self.nextChar()
        nxt = self.peekChar() if self.peekChar() is not None else ''
        # Check multi-char tokens first
        if ch == '+' and nxt == '+':
            self.pos += 1
            return ("incr", "++")
        if ch == '-' and nxt == '-':
            self.pos += 1
            return ("decr", "--")
        if ch == '<' and nxt == '=':
            self.pos += 1
            return ("leq", "<=")
        if ch == '>' and nxt == '=':
            self.pos += 1
            return ("geq", ">=")
        if ch == '=' and nxt == '=':
            self.pos += 1
            return ("eq", "==")
        if ch == '&' and nxt == '&':
            self.pos += 1
            return ("land", "&&")
        if ch == '|' and nxt == '|':
            self.pos += 1
            return ("lor", "||")
        
        # Single-char tokens mapped in a dict
        tokMap = {
            '(': "lParen",
            ')': "rParen",
            '[': "lBrack",
            ']': "rBrack",
            '{': "lBrace",
            '}': "rBrace",
            '.': "dot",
            '+': "plus",
            '-': "minus",
            '*': "mult",
            '/': "div",
            '%': "mod",
            '<': "lt",
            '>': "gt",
            '=': "assign",
            ';': "semi",
            ',': "comma",
            '!': "lnot",
            '&': "band",
            '|': "bor"
        }
        tok = tokMap.get(ch, "unk")
        return (tok, ch)

    def lexComment(self):
        self.pos += 2  # skip '//'
        while self.pos < len(self.src) and self.src[self.pos] != '\n':
            self.pos += 1
        if self.pos < len(self.src) and self.src[self.pos] == '\n':
            self.pos += 1  # skip newline


# Example usage:
if __name__ == "__main__":
    srcCode = "int x = 10; // init x"
    lexr = Lexer(srcCode)
    tokens = lexr.lex()
    for tok in tokens:
        print(tok)
