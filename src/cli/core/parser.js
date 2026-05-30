// src/core/parser.js

import { Token } from './lexer.js'; // فرض می‌کنیم Token از lexer.js می‌آید

export class ASTNode {
    constructor(type, value = null, children = []) {
        this.type = type; // نوع نود (مثلاً 'Program', 'FunctionDeclaration', 'VariableDeclaration', 'BinaryExpression', 'Literal')
        this.value = value; // مقدار (برای نودهای لیترال، اپراتور و...)
        this.children = children; // آرایه‌ای از نودهای فرزند
    }
}

export class Parser {
    constructor(tokens) {
        this.tokens = tokens;
        this.position = 0;
    }

    // توابع کمکی برای کار با توکن‌ها
    currentToken() {
        return this.tokens[this.position];
    }

    peek() {
        return this.tokens[this.position + 1];
    }

    advance() {
        if (this.position < this.tokens.length) {
            this.position++;
        }
    }

    match(tokenType) {
        if (this.currentToken().type === tokenType) {
            this.advance();
            return true;
        }
        throw new Error(`Expected token type ${tokenType} but got ${this.currentToken().type} at ${this.currentToken().line}:${this.currentToken().column}`);
    }

    // تابع اصلی برای پارس کردن
    parse() {
        const programNode = new ASTNode('Program');
        while (this.currentToken().type !== 'EOF') {
            // اینجا باید انواع مختلف دستورات (اعلان متغیر، تعریف تابع، ...) را تشخیص دهیم
            const statement = this.parseStatement();
            if (statement) {
                programNode.children.push(statement);
            }
            // Skip newlines between statements if not handled by parseStatement
            if (this.currentToken().type === 'NEWLINE') {
                 this.advance();
            }
        }
        return programNode;
    }

    parseStatement() {
        const token = this.currentToken();

        if (token.type === 'KEYWORD') {
            switch (token.value) {
                case 'func':
                    return this.parseFunctionDeclaration();
                case 'let':
                case 'const':
                    return this.parseVariableDeclaration(token.value); // 'let' or 'const'
                case 'return':
                    return this.parseReturnStatement();
                case 'if':
                    return this.parseIfStatement();
                 case 'while':
                    return this.parseWhileStatement();
                 case 'print':
                     return this.parsePrintStatement();
                // case 'import': return this.parseImportStatement(); // اگر import پشتیبانی می‌شود
            }
        } else if (token.type === 'IDENTIFIER') {
            // ممکن است انتساب باشد یا فراخوانی تابع
            if (this.peek().type === 'OPERATOR' && this.peek().value === '=') {
                return this.parseAssignmentStatement();
            } else if (this.peek().type === 'LPAREN') {
                return this.parseFunctionCallStatement();
            }
        }

        // اگر هیچکدام از موارد بالا نبود، ممکن است خطای سینتکس باشد یا یک عبارت تکی
         if (token.type !== 'NEWLINE' && token.type !== 'EOF') {
             // Try parsing as an expression (e.g., if it's used for its side effects or standalone)
             try {
                 const expr = this.parseExpression();
                 // If it's just an expression, wrap it in a statement node, maybe called 'ExpressionStatement'
                 // Or if it's meant to be evaluated for side effects, ensure it has them.
                 // For now, let's assume standalone expressions are valid statements.
                 return new ASTNode('ExpressionStatement', null, [expr]);
             } catch (e) {
                 // If parsing as expression fails, it's likely an error
                 console.error("Failed to parse statement. Could be an expression or syntax error.", e);
                 throw e; // Re-throw to stop parsing
             }
         }

        // Skip EOF and NEWLINE if they are not part of a specific statement structure
        if (token.type === 'EOF' || token.type === 'NEWLINE') {
            this.advance();
            return null; // Indicate no statement was parsed
        }

        throw new Error(`Unexpected token type ${token.type} with value ${token.value} at ${token.line}:${token.column}`);
    }

    parseFunctionDeclaration() {
        this.match('KEYWORD'); // Skip 'func'
        const name = this.currentToken().value;
        this.match('IDENTIFIER');
        this.match('LPAREN');
        const params = this.parseParameterList();
        this.match('RPAREN');
        this.match('LBRACE');
        const body = this.parseBlock();
        this.match('RBRACE');
        return new ASTNode('FunctionDeclaration', { name }, [params, body]);
    }

     parseParameterList() {
         const paramsNode = new ASTNode('ParameterList');
         if (this.currentToken().type !== 'RPAREN') {
             while (this.currentToken().type === 'IDENTIFIER') {
                 const paramName = this.currentToken().value;
                 paramsNode.children.push(new ASTNode('Parameter', { name: paramName }));
                 this.advance();
                 if (this.currentToken().type === 'COMMA') {
                     this.match('COMMA');
                 } else if (this.currentToken().type !== 'RPAREN') {
                     throw new Error("Expected comma or closing parenthesis in parameter list.");
                 }
             }
         }
         return paramsNode;
     }


    parseVariableDeclaration(keyword) {
        const isConst = keyword === 'const';
        this.match('KEYWORD'); // Skip 'let' or 'const'
        const name = this.currentToken().value;
        this.match('IDENTIFIER');

        let initializer = null;
        if (this.currentToken().type === 'OPERATOR' && this.currentToken().value === '=') {
            this.match('OPERATOR'); // Skip '='
            initializer = this.parseExpression();
        }
        // If no initializer, value might be undefined/null depending on language spec
        // For simplicity, we'll just store the expression, which could be null.

        // We need to consume the newline or semicolon if present, or assume it ends the line.
         if (this.currentToken().type === 'SEMICOLON') {
            this.match('SEMICOLON');
         } else if (this.currentToken().type === 'NEWLINE') {
             // Newline often acts as a statement terminator in interpreted languages
             this.advance();
         } // If neither, assume it's part of a multi-line statement or an error.

        return new ASTNode('VariableDeclaration', { name, isConst }, initializer ? [initializer] : []);
    }

    parseAssignmentStatement() {
        const variableName = this.currentToken().value;
        this.match('IDENTIFIER');
        this.match('OPERATOR'); // Skip '='
        const value = this.parseExpression();
         // Consume semicolon or newline if present
         if (this.currentToken().type === 'SEMICOLON') {
            this.match('SEMICOLON');
         } else if (this.currentToken().type === 'NEWLINE') {
            this.advance();
         }
        return new ASTNode('AssignmentStatement', { variableName }, [value]);
    }

     parseFunctionCallStatement() {
         // This is for function calls used as statements (e.g., print("hello"))
         const expr = this.parseExpression(); // parseExpression should handle the function call itself
         // Consume semicolon or newline if present
         if (this.currentToken().type === 'SEMICOLON') {
            this.match('SEMICOLON');
         } else if (this.currentToken().type === 'NEWLINE') {
             this.advance();
         }
         return new ASTNode('ExpressionStatement', null, [expr]); // Wrap call in ExpressionStatement
     }


    parseReturnStatement() {
        this.match('KEYWORD'); // Skip 'return'
        let argument = null;
        if (this.currentToken().type !== 'NEWLINE' && this.currentToken().type !== 'EOF' && this.currentToken().type !== 'RBRACE') {
            argument = this.parseExpression();
        }
        // Consume semicolon or newline if present
         if (this.currentToken().type === 'SEMICOLON') {
            this.match('SEMICOLON');
         } else if (this.currentToken().type === 'NEWLINE') {
            this.advance();
         }
        return new ASTNode('ReturnStatement', null, argument ? [argument] : []);
    }

     parseIfStatement() {
         this.match('KEYWORD'); // Skip 'if'
         const condition = this.parseExpression();
         this.match('LBRACE');
         const thenBranch = this.parseBlock();
         this.match('RBRACE');

         let elseBranch = null;
         if (this.currentToken().type === 'KEYWORD' && this.currentToken().value === 'else') {
             this.advance(); // Skip 'else'
             if (this.currentToken().type === 'LBRACE') {
                 this.match('LBRACE');
                 elseBranch = this.parseBlock();
                 this.match('RBRACE');
             } else {
                 // Handle 'else if' or throw error for unexpected token after else
                 // For simplicity, let's assume it must be a block { ... }
                 throw new Error("Expected '{' after 'else'.");
             }
         }
         return new ASTNode('IfStatement', null, [condition, thenBranch].concat(elseBranch ? [elseBranch] : []));
     }

     parseWhileStatement() {
         this.match('KEYWORD'); // Skip 'while'
         const condition = this.parseExpression();
         this.match('LBRACE');
         const body = this.parseBlock();
         this.match('RBRACE');
         return new ASTNode('WhileStatement', null, [condition, body]);
     }

     parsePrintStatement() {
         this.match('KEYWORD'); // Skip 'print'
         const argument = this.parseExpression();
          // Consume semicolon or newline if present
         if (this.currentToken().type === 'SEMICOLON') {
            this.match('SEMICOLON');
         } else if (this.currentToken().type === 'NEWLINE') {
            this.advance();
         }
         return new ASTNode('PrintStatement', null, [argument]);
     }


    parseBlock() {
        const blockNode = new ASTNode('Block');
        while (this.currentToken().type !== 'EOF' && this.currentToken().type !== 'RBRACE') {
            const statement = this.parseStatement();
            if (statement) {
                blockNode.children.push(statement);
            }
             // Skip potential newlines within the block unless parseStatement already handled it
             if (this.currentToken().type === 'NEWLINE') {
                 this.advance();
             }
        }
        return blockNode;
    }

    // Parsing expressions (handles operator precedence)
    // This is a simplified version, a full implementation would use Pratt parsing or similar
    parseExpression() {
        let left = this.parsePrimaryExpression();

        while (this.currentToken().type === 'OPERATOR' && ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>='].includes(this.currentToken().value)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parsePrimaryExpression();
            left = new ASTNode('BinaryExpression', operator, [left, right]);
        }

        return left;
    }

    parsePrimaryExpression() {
        const token = this.currentToken();

        switch (token.type) {
            case 'NUMBER':
                this.advance();
                return new ASTNode('Literal', { type: 'number', value: token.value });
            case 'STRING':
                this.advance();
                return new ASTNode('Literal', { type: 'string', value: token.value });
            case 'KEYWORD': // true, false, null
                 if (['true', 'false', 'null'].includes(token.value)) {
                     this.advance();
                     return new ASTNode('Literal', { type: 'boolean', value: token.value === 'true' ? true : (token.value === 'false' ? false : null) });
                 }
                 // Fallthrough for other keywords if they can start expressions (e.g., 'const' - though handled in declarations)
            case 'IDENTIFIER':
                this.advance();
                // Check if it's a function call
                if (this.currentToken().type === 'LPAREN') {
                    this.match('LPAREN');
                    const args = this.parseArgumentList();
                    this.match('RPAREN');
                    return new ASTNode('FunctionCall', { name: token.value }, args.children);
                }
                return new ASTNode('Identifier', { name: token.value });
            case 'LPAREN':
                this.advance();
                const expr = this.parseExpression();
                this.match('RPAREN');
                return expr; // Parenthesized expression, return the inner expression's AST node
            // case 'KEYWORD': // like 'func' if lambdas are supported
            //     return this.parseLambdaFunction();
            default:
                 // Handle errors or other token types if necessary
                throw new Error(`Unexpected token type ${token.type} in primary expression at ${token.line}:${token.column}`);
        }
    }

     parseArgumentList() {
         const argsNode = new ASTNode('ArgumentList');
         if (this.currentToken().type !== 'RPAREN') {
             while (true) {
                 const arg = this.parseExpression();
                 argsNode.children.push(arg);
                 if (this.currentToken().type === 'COMMA') {
                     this.match('COMMA');
                 } else if (this.currentToken().type === 'RPAREN') {
                     break; // End of arguments
                 } else {
                     throw new Error("Expected comma or closing parenthesis in argument list.");
                 }
             }
         }
         return argsNode;
     }

}

// Example usage (for testing purposes):
/*
import { Lexer } from './lexer.js';
const inputCode = `
let x = 10 + 5 * 2;
func greet(name) {
    print("Hello, " + name);
}
greet("World");
if (x > 20) {
    print("x is large");
}
`;
const lexer = new Lexer(inputCode);
const tokens = lexer.tokenize();
console.log("Tokens:", tokens);

const parser = new Parser(tokens);
const ast = parser.parse();
console.log("AST:", JSON.stringify(ast, null, 2));
*/
