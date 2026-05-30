// src/core/compiler.js

import { ASTNode } from './parser.js';
import { BXZ_RUNTIME } from './runtime.js'; // برای فراخوانی توابع runtime
import { Token } from './lexer.js'; // برای استفاده از Token اگر لازم شد

export class Compiler {
    constructor(runtimeNamespace = 'BXZ_RUNTIME') {
        this.runtimeNamespace = runtimeNamespace; // نام سراسری runtime
        this.scope = []; // مدیریت scope ها (global, function, block)
        this.currentScope = {}; // اشیاء scope فعلی
        this.output = ''; // کد جاوا اسکریپت تولید شده
        this.tempVarCounter = 0; // شمارنده برای متغیرهای موقت
    }

    // ایجاد نام منحصر به فرد برای متغیرهای موقت
    generateTempVar() {
        return `__temp_${this.tempVarCounter++}`;
    }

    // مدیریت Scope
    enterScope() {
        this.scope.push(this.currentScope);
        this.currentScope = {}; // اسکوپ جدید را خالی می‌کنیم
    }

    exitScope() {
        this.currentScope = this.scope.pop() || {};
    }

    // ثبت متغیر در اسکوپ فعلی
    declareVariable(name, isConst = false) {
        if (this.currentScope[name]) {
            throw new Error(`Variable '${name}' is already declared in this scope.`);
        }
        this.currentScope[name] = { isConst };
    }

    // دریافت اطلاعات متغیر (برای چک کردن const و ...)
    getVariableInfo(name) {
        // Check current scope first, then outer scopes
        if (this.currentScope.hasOwnProperty(name)) {
            return this.currentScope[name];
        }
        // Iterate through outer scopes (if implemented properly)
        // For simplicity, this example only checks the immediate scope.
        // A real compiler would traverse the scope chain.
        return null;
    }

     // Check if a variable exists in any accessible scope
     variableExists(name) {
         // Check current scope
         if (this.currentScope.hasOwnProperty(name)) return true;
         // In a full implementation, you'd check parent scopes here.
         // For now, assume only global and current scope matter directly.
         // Accessing global variables might go through the runtime object.
         return false;
     }


    compile(ast) {
        // Reset compiler state for a new compilation
        this.scope = [];
        this.currentScope = {};
        this.output = '';
        this.tempVarCounter = 0;

        // Start with global scope
        this.enterScope(); // Global scope

        // Assume the AST is a Program node
        if (ast.type === 'Program') {
            ast.children.forEach(statement => {
                this.compileNode(statement);
            });
        } else {
            throw new Error("Invalid AST: Root must be a Program node.");
        }

        this.exitScope(); // Exit global scope

        // Wrap the generated code in a way that BXZ_RUNTIME is available
        // This assumes BXZ_RUNTIME is globally available or imported elsewhere
        // For Node.js, we might need to explicitly require or pass it.
        // Let's assume it's globally injected by the runner.
        return `${this.runtimeNamespace}.init();\n${this.output}\n${this.runtimeNamespace}.cleanup();`;
    }

    compileNode(node) {
        switch (node.type) {
            case 'Program':
                node.children.forEach(child => this.compileNode(child));
                break;

            case 'Block':
                this.enterScope();
                node.children.forEach(child => this.compileNode(child));
                this.exitScope();
                break;

            case 'FunctionDeclaration':
                this.compileFunctionDeclaration(node);
                break;

            case 'VariableDeclaration':
                this.compileVariableDeclaration(node);
                break;

            case 'AssignmentStatement':
                this.compileAssignmentStatement(node);
                break;

            case 'ReturnStatement':
                this.compileReturnStatement(node);
                break;

             case 'IfStatement':
                 this.compileIfStatement(node);
                 break;

             case 'WhileStatement':
                 this.compileWhileStatement(node);
                 break;

             case 'PrintStatement':
                 this.compilePrintStatement(node);
                 break;

            case 'ExpressionStatement':
                 // Evaluate the expression for its side effects (like function calls)
                 // We discard the return value unless it's a side effect we need to capture
                 this.compileNode(node.children[0]);
                 break;

            case 'Literal':
                return this.compileLiteral(node);

            case 'Identifier':
                 return this.compileIdentifier(node);

             case 'BinaryExpression':
                 return this.compileBinaryExpression(node);

            case 'FunctionCall':
                 return this.compileFunctionCall(node);

            // Add cases for other AST node types...

            default:
                throw new Error(`Unknown AST node type: ${node.type}`);
        }
    }

    compileFunctionDeclaration(node) {
        const { name } = node.value;
        const params = node.children[0]; // ParameterList node
        const body = node.children[1]; // Block node

        this.declareVariable(name, false); // Functions are typically variables holding the function reference

        const paramNames = params.children.map(p => p.value.name);
        const compiledBody = this.compile(body); // Compile the body within its own scope

        // Generate JS function string
        // Note: The generated JS function needs access to the correct scope chain and BXZ_RUNTIME
        // For simplicity, we'll assume BXZ_RUNTIME is global.
        // A more robust compiler would handle scope resolution explicitly.

        // We define the function in the current scope.
        // The compiledBody needs to be wrapped to handle its scope correctly.
        const functionCode = `
            function ${name}(${paramNames.join(', ')}) {
                // Entering function scope
                ${this.runtimeNamespace}.enterFunctionScope(); // Hypothetical runtime function
                // Declare parameters in the new scope
                ${paramNames.map(pName => `this.declareVariable('${pName}');`).join('\n')} // Assuming 'this' refers to compiler instance or similar in runtime

                // Compile the body code
                let functionBodyOutput = '';
                try {
                    ${this.compile(body)} // Compile the body separately, it returns JS code
                } finally {
                     ${this.runtimeNamespace}.exitFunctionScope(); // Clean up function scope
                }
                return functionBodyOutput; // Return compiled body code
            }
        `;
        // This part is tricky: how to compile the body *within* the context of the function?
        // A better approach might be to return the compiled JS code from compile()
        // and then use that code string here.

        // Let's simplify: Assume compile() returns JS code.
        const compiledBodyCode = this.compile(body); // Get the JS code for the body
        // Wrap the body in a closure or similar structure for scope management.
         const funcJs = `
             ${name}: function(${paramNames.join(', ')}) {
                 // Entering function scope (managed by runtime)
                 const _oldScope = this.currentScope;
                 this.currentScope = {}; // New scope for the function
                 ${paramNames.map(pName => `this.declareVariable('${pName}');`).join('\n')}

                 let result;
                 try {
                     result = (function() { // Use a closure for the body
                         // Code within the function body will execute here
                         ${compiledBodyCode.replace('${this.runtimeNamespace}.init();', '').replace('${this.runtimeNamespace}.cleanup();', '')} // Remove outer runtime calls
                     })();
                 } finally {
                     this.currentScope = _oldScope; // Restore outer scope
                 }
                 return result;
             }
         `;

        // Store the function definition in the current scope (global or block scope)
        // This assumes functions are first-class citizens and stored in variables.
        // If functions are directly callable by name, this needs adjustment.
        // Let's assume they are stored under their name.
        this.output += `
            // Define function ${name}
            this.currentScope['${name}'] = {
                isConst: false, // Functions are variables
                value: (${funcJs.split(':')[1].trim()}) // The actual JS function
            };
            // Assign to global/runtime if needed:
            // ${this.runtimeNamespace}['${name}'] = this.currentScope['${name}'].value;
        `;
         // Simplified: Directly assign to the runtime object or global scope
         // This needs careful scope management.
         // A common pattern is to compile the function body and store it.

         // Let's try compiling the function as a value assigned to its name
         // This requires a way to pass the scope and runtime context to the compiled function.
         // For now, assume runtime context is globally available via BXZ_RUNTIME
         const functionParameters = paramNames.join(', ');
         // Need to re-compile the body in a way that captures the current compiler state correctly.
         // This is a complex part of compilation. For now, a placeholder:
         this.output += `
             ${this.runtimeNamespace}['${name}'] = function(${functionParameters}) {
                 // Function body compilation needs to be done here or referenced.
                 // For this example, let's just create a placeholder.
                 console.warn("Function '${name}' compilation is simplified.");
                 // A real compiler would generate the body code here, managing scope.
                 return (function() {
                    // Placeholder for compiled function body
                    ${this.compile(body)}
                 })();
             };
         `;
    }

    compileVariableDeclaration(node) {
        const { name, isConst } = node.value;
        const initializer = node.children.length > 0 ? node.children[0] : null;

        this.declareVariable(name, isConst);

        let compiledInitializer = 'undefined'; // Default value
        if (initializer) {
            compiledInitializer = this.compileNode(initializer);
        }

        // Add to current scope. We'll use JS 'let' or 'const' when generating code.
        // For simplicity here, let's assume declaration happens at the top level or within a scope block.
        // The actual JS code generation will use `let` or `const`.
        this.output += `let ${name} = ${compiledInitializer};\n`;
        // If compiling to a context where variables are managed differently (e.g., a runtime object),
        // this line would change to something like:
        // this.currentScope[name] = { value: compiledInitializer, isConst };
    }

    compileAssignmentStatement(node) {
        const variableName = node.value.variableName;
        const valueNode = node.children[0];

        // Check if variable exists and if it's const
        if (!this.variableExists(variableName)) {
            throw new Error(`Cannot assign to an undeclared variable '${variableName}'.`);
        }
        const varInfo = this.getVariableInfo(variableName);
        if (varInfo && varInfo.isConst) {
            throw new Error(`Cannot assign to a constant variable '${variableName}'.`);
        }

        const compiledValue = this.compileNode(valueNode);
        this.output += `${variableName} = ${compiledValue};\n`;
    }

    compileReturnStatement(node) {
        let returnValue = 'undefined'; // Default return value
        if (node.children.length > 0) {
            returnValue = this.compileNode(node.children[0]);
        }
        this.output += `return ${returnValue};\n`;
    }

     compileIfStatement(node) {
         const condition = this.compileNode(node.children[0]);
         const thenBranch = node.children[1]; // Block node
         const elseBranch = node.children.length > 2 ? node.children[2] : null; // Optional Block node

         // Compile the branches. Each branch compilation will generate JS code.
         // The generated code needs to be executed only if the condition is met.
         // The compile() method returns the JS code string.

         // We need to compile the branches and wrap them in functions or blocks
         // to manage scope correctly.
         const compiledThenBranch = this.compile(thenBranch);
         const compiledElseBranch = elseBranch ? this.compile(elseBranch) : '';

         this.output += `
             if (${condition}) {
                 ${compiledThenBranch.replace('${this.runtimeNamespace}.init();', '').replace('${this.runtimeNamespace}.cleanup();', '')} // Execute 'then' block code
             } ${elseBranch ? `else {
                 ${compiledElseBranch.replace('${this.runtimeNamespace}.init();', '').replace('${this.runtimeNamespace}.cleanup();', '')} // Execute 'else' block code
             }` : ''}
         `;
     }

     compileWhileStatement(node) {
         const condition = this.compileNode(node.children[0]);
         const body = node.children[1]; // Block node

         const compiledBody = this.compile(body); // Compile the body

         this.output += `
             while (${condition}) {
                 ${compiledBody.replace('${this.runtimeNamespace}.init();', '').replace('${this.runtimeNamespace}.cleanup();', '')} // Execute body code
             }
         `;
     }

     compilePrintStatement(node) {
         const argument = node.children[0];
         const compiledArg = this.compileNode(argument);
         // Assuming 'print' is a function provided by BXZ_RUNTIME
         this.output += `${this.runtimeNamespace}.print(${compiledArg});\n`;
     }


    compileLiteral(node) {
        const { type, value } = node.value;
        if (type === 'string') {
            // Escape special characters within the string if necessary for JS
            const escapedValue = JSON.stringify(value); // Handles quotes and escapes
            return escapedValue;
        } else if (type === 'number' || type === 'boolean') {
            return String(value);
        } else if (type === 'null') {
            return 'null';
        }
        throw new Error(`Unsupported literal type: ${type}`);
    }

    compileIdentifier(node) {
        const { name } = node.value;
        // Here we need to resolve the variable name to its actual value in the current scope.
        // If it's not in the current scope, we might need to look in outer scopes or globals.
        if (!this.variableExists(name)) {
             // Check if it's a global runtime function/variable
             if (this.runtimeNamespace && typeof BXZ_RUNTIME[name] !== 'undefined') {
                 return `${this.runtimeNamespace}.${name}`;
             }
            throw new Error(`Undefined variable '${name}'.`);
        }
        // In a real compiler, you'd return the name if it's in the current scope,
        // or handle scope resolution (e.g., prefixing with `this.currentScope` or similar).
        // For JS output, just returning the name is often enough if variables are globally scoped or declared with `let`/`const`.
        return name;
    }

    compileBinaryExpression(node) {
        const operator = node.value; // The operator itself
        const left = this.compileNode(node.children[0]);
        const right = this.compileNode(node.children[1]);

        // Add type checks or coercion if needed by BXZ language rules
        return `(${left} ${operator} ${right})`;
    }

    compileFunctionCall(node) {
        const functionName = node.value.name; // This is the AST 'FunctionCall' node's value.name
        const args = node.children; // This is the array of AST nodes for arguments

        const compiledArgs = args.map(arg => this.compileNode(arg));

        // How to call the function?
        // If the function is a variable in the current scope:
        // Check if the function name exists and is callable.
        if (!this.variableExists(functionName)) {
             // Could it be a built-in runtime function?
             if (this.runtimeNamespace && typeof BXZ_RUNTIME[functionName] === 'function') {
                  return `${this.runtimeNamespace}.${functionName}(${compiledArgs.join(', ')})`;
             }
            throw new Error(`Call to undefined function or variable '${functionName}'.`);
        }

        // Assuming the function name refers to a variable holding a function
        // The compiled name should resolve to the function object.
        return `${functionName}(${compiledArgs.join(', ')})`;
    }
}


// Example usage (for testing purposes):
/*
import { Lexer } from './lexer.js';
import { Parser } from './parser.js';

const inputCode = `
let x = 10;
const y = 20;
func add(a, b) {
    return a + b;
}
let result = add(x, y);
print("Result: " + result);
if (result > 30) {
    print("Big result!");
}
`;

const lexer = new Lexer(inputCode);
const tokens = lexer.tokenize();
const parser = new Parser(tokens);
const ast = parser.parse();

const compiler = new Compiler(); // Uses BXZ_RUNTIME by default
const compiledCode = compiler.compile(ast);

console.log("--- AST ---");
console.log(JSON.stringify(ast, null, 2));
console.log("\n--- Compiled JavaScript ---");
console.log(compiledCode);

// To actually run this, you'd need a runtime environment
// that provides BXZ_RUNTIME. For example, in Node.js:
//
// const BXZ_RUNTIME = {
//     print: (msg) => console.log(msg),
//     // other runtime functions like readFile, writeFile, etc.
//     init: () => console.log("Runtime initialized."),
//     cleanup: () => console.log("Runtime cleaned up."),
//     enterFunctionScope: () => {}, // Placeholder
//     exitFunctionScope: () => {},  // Placeholder
//     declareVariable: (name) => {}, // Placeholder
//     // ... potentially global variables/functions here
// };
//
// // Make runtime available globally or inject it
// global.BXZ_RUNTIME = BXZ_RUNTIME;
//
// try {
//     // Use eval or Function constructor to run the compiled code string
//     // WARNING: eval is generally unsafe. Function constructor is slightly better.
//     const run = new Function(compiledCode);
//     run();
// } catch (error) {
//     console.error("Runtime Error:", error);
// }

*/
