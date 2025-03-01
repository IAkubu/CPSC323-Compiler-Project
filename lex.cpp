#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>

using namespace std;

unordered_map<string, string> lexToTok = {
        // Keywords
        {"int", "KEYWORD"}, {"float", "KEYWORD"}, {"char", "KEYWORD"},
        {"main", "KEYWORD"}, {"return", "KEYWORD"}, {"while", "KEYWORD"},
        {"for", "KEYWORD"}, {"break", "KEYWORD"}, {"if", "KEYWORD"},
        {"else", "KEYWORD"}, {"goto", "KEYWORD"}, {"continue", "KEYWORD"},
        {"switch", "KEYWORD"}, {"case", "KEYWORD"}, {"unsigned", "KEYWORD"},
        {"void", "KEYWORD"},

        // Separators
        {"(", "leftParen"}, {")", "rightParen"}, {"[", "leftBracket"},
        {"]", "rightBracket"}, {"{", "leftBrace"}, {"}", "rightBrace"},
        {";", "semicolon"}, {",", "comma"},

        // Operators
        {".", "dot"}, {"+", "plus"}, {"-", "minus"}, {"*", "multiply"},
        {"/", "divide"}, {"%", "modulus"}, {"<", "lessThan"}, {">", "greaterThan"},
        {"=", "assignment"}, {"++", "increment"}, {"--", "decrement"},
        {"<=", "lessThanEq"}, {">=", "greaterThanEq"}, {"==", "logicEqual"},
        {"&&", "logicAnd"}, {"||", "logicOr"}, {"!", "logicNot"},
        {"&", "bitAnd"}, {"|", "bitOr"}
};

struct Token {
    string typeOfToken;
    string lexeme;
};

bool isSeparator(char ch) {
    return ch == '(' || ch == ')' || ch == '[' || ch == ']' ||
           ch == '{' || ch == '}' || ch == ';' || ch == ',';
}

bool isOperator(char ch) {
    return ch == '+' || ch == '-' || ch == '=' || ch == '<' ||
           ch == '>' || ch == '/' || ch == '*';
}


// DFA using switch case to determine lexemes and hash table to find token

Token getToken(ifstream& source) {
    enum State { START, IN_NUMBER, IN_OPERATOR, IN_IDENTIFIER, IN_SEPARATOR, END }; // needs an IN_COMMENT state
    char currentCh;
    string currentLexeme;
    Token token;
    State currentState = START;

    while (currentState != END) {
        switch (currentState) {
            case START:
                if (source.get(currentCh)) {
                    currentLexeme = currentCh;
                    if (isdigit(currentCh)) currentState = IN_NUMBER;
                    else if (isOperator(currentCh)) currentState = IN_OPERATOR;
                    else if (isalpha(currentCh)) currentState = IN_IDENTIFIER;
                    else if (isSeparator(currentCh)) currentState = IN_SEPARATOR;
                } else {
                    currentState = END;
                }
                break;

            case IN_IDENTIFIER:
                while (source.get(currentCh) && (isalnum(currentCh) || currentCh == '_'))
                    currentLexeme += currentCh;
                if (source) source.unget();
                token.typeOfToken = lexToTok.count(currentLexeme) ? lexToTok[currentLexeme] : "IDENTIFIER";
                token.lexeme = currentLexeme;
                currentState = END;
                break;

            case IN_NUMBER:
                while (source.get(currentCh) && isdigit(currentCh))
                    currentLexeme += currentCh;
                if (source) source.unget();
                token.typeOfToken = "NUMBER";
                token.lexeme = currentLexeme;
                currentState = END;
                break;

            case IN_OPERATOR:
                while (source.get(currentCh) && isOperator(currentCh))
                    currentLexeme += currentCh;
                if (source) source.unget();
                token.typeOfToken = lexToTok.count(currentLexeme) ? lexToTok[currentLexeme] : "UNKNOWN";
                token.lexeme = currentLexeme;
                currentState = END;
                break;

            case IN_SEPARATOR:
                token.typeOfToken = lexToTok.count(currentLexeme) ? lexToTok[currentLexeme] : "UNKNOWN";
                token.lexeme = currentLexeme;
                currentState = END;
                break;

            case END:
                break;
        }
    }
    return token;
}

// Utilized reading from text file to easily implement DFA logic

int main() {
    string source;
    cout << "Enter name of source file you want to open: ";
    cin >> source;

    ifstream sourceFile(source);
    if (!sourceFile.is_open()) {
        cerr << "Couldn't open file." << endl;
        return 1;
    }

    Token token;
    while (sourceFile) {
        token = getToken(sourceFile);
        if (token.lexeme.empty()) break;
        cout << "Token: " << token.typeOfToken << "  Lexeme: " << token.lexeme << "\n";
    }

    sourceFile.close();
    return 0;
}
