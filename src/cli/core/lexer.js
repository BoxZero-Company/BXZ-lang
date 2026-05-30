// src/core/lexer.js

import { BXZ_RUNTIME } from './runtime.js'; // فرض می‌کنیم runtime در اینجا استفاده می‌شود

export class Token {
    constructor(type, value, line, column) {
        this.type = type; // نوع توکن (مثلاً 'KEYWORD', 'IDENTIFIER', 'NUMBER', 'OPERATOR', 'STRING', 'EOF')
        this.value = value; // مقدار توکن
        this.line = line; // شماره خط
        this.column = column; // شماره ستون
    }

    toString() {
        return `Token(${this.type}, ${this.value}, L${this.line}:${this.column})`;
    }
}

export class Lexer {
    constructor(input) {
        this.input = input;
        this.position = 0;
        this.line = 1;
        this.column = 1;
        this.tokens = [];
        this.keywords = new Set([
            'func', 'if', 'else', 'while', 'for', 'return', 'let', 'const', 'import', 'print', 'true', 'false', 'null'
            // کلمات کلیدی دیگر BXZ را اینجا اضافه کنید
        ]);
    }

    // توابع کمکی برای بررسی کاراکترها
    isDigit(char) {
        return char >= '0' && char <= '9';
    }

    isAlpha(char) {
        return (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z') || char === '_';
    }

    isAlphaNumeric(char) {
        return this.isAlpha(char) || this.isDigit(char);
    }

    isWhitespace(char) {
        return char === ' ' || char === '\t' || char === '\n' || char === '\r';
    }

    // تابع اصلی برای توکنایز کردن
    tokenize() {
        while (this.position < this.input.length) {
            const char = this.input[this.position];

            if (char === '\n') {
                this.tokens.push(new Token('NEWLINE', char, this.line, this.column));
                this.line++;
                this.column = 1;
                this.position++;
                continue;
            }

            if (this.isWhitespace(char)) {
                this.position++;
                this.column++;
                continue;
            }

            if (char === '/' && this.input[this.position + 1] === '/') {
                // Comment
                while (this.position < this.input.length && this.input[this.position] !== '\n') {
                    this.position++;
                    this.column++;
                }
                continue;
            }

            if (char === '"' || char === "'") {
                // String literal
                this.tokens.push(this.readString(char));
                continue;
            }

            if (this.isDigit(char)) {
                // Number literal
                this.tokens.push(this.readNumber());
                continue;
            }

            if (this.isAlpha(char)) {
                // Identifier or keyword
                const value = this.readIdentifier();
                if (this.keywords.has(value)) {
                    this.tokens.push(new Token('KEYWORD', value, this.line, this.column - value.length));
                } else {
                    this.tokens.push(new Token('IDENTIFIER', value, this.line, this.column - value.length));
                }
                continue;
            }

            // Operators and Punctuation
            switch (char) {
                case '+':
                    this.tokens.push(new Token('OPERATOR', char, this.line, this.column)); this.position++; this.column++; break;
                case '-':
                    this.tokens.push(new Token('OPERATOR', char, this.line, this.column)); this.position++; this.column++; break;
                case '*':
                    this.tokens.push(new Token('OPERATOR', char, this.line, this.column)); this.position++; this.column++; break;
                case '/':
                    this.tokens.push(new Token('OPERATOR', char, this.line, this.column)); this.position++; this.column++; break;
                case '%':
                    this.tokens.push(new Token('OPERATOR', char, this.line, this.column)); this.position++; this.column++; break;
                case '=':
                    if (this.input[this.position + 1] === '=') {
                        this.tokens.push(new Token('OPERATOR', '==', this.line, this.column));
                        this.position += 2; this.column += 2;
                    } else {
                        this.tokens.push(new Token('OPERATOR', '=', this.line, this.column));
                        this.position++; this.column++;
                    }
                    break;
                case '!':
                     if (this.input[this.position + 1] === '=') {
                        this.tokens.push(new Token('OPERATOR', '!=', this.line, this.column));
                        this.position += 2; this.column += 2;
                    } else {
                        this.tokens.push(new Token('OPERATOR', '!', this.line, this.column));
                        this.position++; this.column++;
                    }
                    break;
                case '<':
                     if (this.input[this.position + 1] === '=') {
                        this.tokens.push(new Token('OPERATOR', '<=', this.line, this.column));
                        this.position += 2; this.column += 2;
                    } else {
                        this.tokens.push(new Token('OPERATOR', '<', this.line, this.column));
                        this.position++; this.column++;
                    }
                    break;
                case '>':
                     if (this.input[this.position + 1] === '=') {
                        this.tokens.push(new Token('OPERATOR', '>=', this.line, this.column));
                        this.position += 2; this.column += 2;
                    } else {
                        this.tokens.push(new Token('OPERATOR', '>', this.line, this.column));
                        this.position++; this.column++;
                    }
                    break;
                case '(':
                    this.tokens.push(new Token('LPAREN', char, this.line, this.column)); this.position++; this.column++; break;
                case ')':
                    this.tokens.push(new Token('RPAREN', char, this.line, this.column)); this.position++; this.column++; break;
                case '{':
                    this.tokens.push(new Token('LBRACE', char, this.line, this.column)); this.position++; this.column++; break;
                case '}':
                    this.tokens.push(new Token('RBRACE', char, this.line, this.column)); this.position++; this.column++; break;
                case '[':
                    this.tokens.push(new Token('LBRACKET', char, this.line, this.column)); this.position++; this.column++; break;
                case ']':
                    this.tokens.push(new Token('RBRACKET', char, this.line, this.column)); this.position++; this.column++; break;
                case ',':
                    this.tokens.push(new Token('COMMA', char, this.line, this.column)); this.position++; this.column++; break;
                case '.':
                     this.tokens.push(new Token('DOT', char, this.line, this.column)); this.position++; this.column++; break;
                case ';':
                    this.tokens.push(new Token('SEMICOLON', char, this.line, this.column)); this.position++; this.column++; break;
                // اپراتورهای دیگر و کاراکترهای خاص را اینجا اضافه کنید
                default:
                    // کاراکتر ناشناخته
                    console.warn(`Unknown character '${char}' at line ${this.line}, column ${this.column}`);
                    this.tokens.push(new Token('UNKNOWN', char, this.line, this.column));
                    this.position++;
                    this.column++;
            }
        }

        this.tokens.push(new Token('EOF', null, this.line, this.column)); // End Of File token
        return this.tokens;
    }

    readString(quoteChar) {
        let startCol = this.column;
        let value = '';
        this.position++; // skip opening quote
        this.column++;

        while (this.position < this.input.length) {
            const char = this.input[this.position];
            if (char === quoteChar) {
                this.position++;
                this.column++;
                return new Token('STRING', value, this.line, startCol);
            }
            // handle escape sequences if needed (e.g., \n, \t, \")
            if (char === '\\') {
                 if (this.input[this.position + 1] === quoteChar || this.input[this.position + 1] === '\\') {
                    value += this.input[this.position + 1];
                    this.position += 2;
                    this.column += 2;
                 } else {
                     // handle other escapes or throw error
                     value += char; // default: just add the backslash
                     this.position++;
                     this.column++;
                 }
            } else {
                value += char;
                this.position++;
                this.column++;
            }
        }
        // If we reach here, the string was not closed
        throw new Error(`Unterminated string literal starting at line ${this.line}, column ${startCol}`);
    }


    readNumber() {
        let startCol = this.column;
        let value = '';
        while (this.position < this.input.length && this.isDigit(this.input[this.position])) {
            value += this.input[this.position];
            this.position++;
            this.column++;
        }
        // Handle floating point numbers if supported
        if (this.position < this.input.length && this.input[this.position] === '.') {
             value += '.';
             this.position++;
             this.column++;
             while (this.position < this.input.length && this.isDigit(this.input[this.position])) {
                 value += this.input[this.position];
                 this.position++;
                 this.column++;
             }
        }
        return new Token('NUMBER', parseFloat(value), this.line, startCol);
    }

    readIdentifier() {
        let startCol = this.column;
        let value = '';
        while (this.position < this.input.length && this.isAlphaNumeric(this.input[this.position])) {
            value += this.input[this.position];
            this.position++;
            this.column++;
        }
        return value;
    }
}

// Example usage (for testing purposes):
/*
const inputCode = `
func add(a, b) {
    return a + b;
}
let result = add(10, 5);
print("Result is: " + result);
`;

const lexer = new Lexer(inputCode);
const tokens = lexer.tokenize();
console.log(tokens);
*/
