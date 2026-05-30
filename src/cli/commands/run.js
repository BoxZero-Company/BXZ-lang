// src/cli/commands/run.js

import { Lexer } from '../core/lexer.js';
import { Parser } from '../core/parser.js';
import { Compiler } from '../core/compiler.js';
// این خط فرض می کند که utils.js تابع readFileContent را export می کند
import { readFileContent } from '../core/utils.js';

export const runCommand = {
    command: 'run <file>',
    describe: 'Run a BXZ file',
    builder: (yargs) => {
        return yargs.positional('file', {
            describe: 'Path to the BXZ file to run',
            type: 'string',
        });
    },
    handler: async (argv) => {
        const filePath = argv.file;
        console.log(`Attempting to run BXZ file: ${filePath}`);

        try {
            // 1. Read the file content using the imported utility function
            const bxzCode = readFileContent(filePath);

            // 2. Tokenize the code using the Lexer class
            const lexer = new Lexer(bxzCode);
            const tokens = lexer.tokenize();
            // console.log("Tokens:", tokens); // Uncomment for debugging

            // 3. Parse the tokens into an AST using the Parser class
            const parser = new Parser(tokens);
            const ast = parser.parse();
            // console.log("AST:", JSON.stringify(ast, null, 2)); // Uncomment for debugging

            // 4. Compile the AST into JavaScript using the Compiler class
            const compiler = new Compiler(); // Uses BXZ_RUNTIME by default
            const compiledJsCode = compiler.compile(ast);
            // console.log("Compiled JS:", compiledJsCode); // Uncomment for debugging

            // 5. Execute the compiled JavaScript code
            // Mock BXZ_RUNTIME for demonstration purposes.
            // In a real app, this would be properly injected or managed.
            const BXZ_RUNTIME = {
                print: (msg) => console.log(msg),
                readFile: async (path) => {
                    // Note: readFile here is part of the runtime, might need async fs
                    const fsPromises = await import('fs/promises');
                    return await fsPromises.readFile(path, 'utf-8');
                },
                writeFile: async (path, content) => {
                    const fsPromises = await import('fs/promises');
                    await fsPromises.writeFile(path, content, 'utf-8');
                },
                init: () => console.log("BXZ Runtime Initialized."),
                cleanup: () => console.log("BXZ Runtime Cleaned up."),
                enterFunctionScope: () => {},
                exitFunctionScope: () => {},
                declareVariable: (name) => { /* runtime scope management */ },
            };

            // Create a new function context to run the compiled code
            const executableCode = `
                const ${compiler.runtimeNamespace} = arguments[0]; // Make runtime available
                ${compiledJsCode} // The compiled BXZ code
            `;

            // Execute using Function constructor for better isolation
            const runFunction = new Function(executableCode);
            runFunction(BXZ_RUNTIME); // Pass the runtime object

            console.log(`Successfully executed ${filePath}`);

        } catch (error) {
            console.error(`Error running BXZ file '${filePath}':`, error.message);
            // console.error(error); // Uncomment for full stack trace
        }
    },
};

// Note: No export default here, using export const
