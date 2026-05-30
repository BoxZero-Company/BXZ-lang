// src/core/runtime.js
import { execSync } from 'child_process';
import fs from 'fs-extra';
import path from 'path';

// Helper function to ensure directory exists
async function ensureDir(dirPath) {
    await fs.ensureDir(dirPath);
}

export const BXZ_RUNTIME = {
    runPy: (script, options = {}) => {
        try {
            // Ensure python3 is available, or adjust command
            const result = execSync(`python3 -c ${JSON.stringify(script)}`, { stdio: 'pipe', encoding: 'utf-8' });
            return result.trim(); // Return stdout
        } catch (error) {
            console.error("Error executing Python code:", error.message);
            // Consider how to pass stderr back if needed
            return `Error: ${error.message}`;
        }
    },

    genHtml: async (filePath, content) => {
        try {
            const absolutePath = path.resolve(filePath); // Resolve path relative to CWD or execution context
            const dir = path.dirname(absolutePath);
            await ensureDir(dir);
            const fullHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BXZ Generated Page</title>
</head>
<body>
${content}
</body>
</html>`;
            await fs.writeFile(absolutePath, fullHtml);
            console.log(`HTML file generated at: ${absolutePath}`);
        } catch (error) {
            console.error(`Error generating HTML file ${filePath}:`, error.message);
        }
    },

    genCss: async (filePath, content) => {
        try {
            const absolutePath = path.resolve(filePath);
            const dir = path.dirname(absolutePath);
            await ensureDir(dir);
            await fs.writeFile(absolutePath, content);
            console.log(`CSS file generated at: ${absolutePath}`);
        } catch (error) {
            console.error(`Error generating CSS file ${filePath}:`, error.message);
        }
    },

    print: (...args) => {
        // console.log(...args); // Use console.log for Node.js environment
        // In a browser context, you'd use console.log too.
        // If we need custom output formatting, implement here.
        args.forEach((arg, index) => {
             process.stdout.write(arg === null ? 'null' : arg === undefined ? 'undefined' : arg.toString());
             if (index < args.length - 1) {
                 process.stdout.write(' '); // Space between arguments
             }
         });
         process.stdout.write('\n'); // Newline at the end
    },

     readFile: async (filePath) => {
         try {
             const absolutePath = path.resolve(filePath);
             return await fs.readFile(absolutePath, 'utf-8');
         } catch (error) {
             console.error(`Error reading file ${filePath}:`, error.message);
             return null;
         }
     },
     writeFile: async (filePath, content) => {
         try {
             const absolutePath = path.resolve(filePath);
             const dir = path.dirname(absolutePath);
             await ensureDir(dir);
             await fs.writeFile(absolutePath, content);
             console.log(`File written successfully at: ${absolutePath}`);
         } catch (error) {
             console.error(`Error writing file ${filePath}:`, error.message);
         }
     }
};

// Exporting default for easier import in compiled code
export default BXZ_RUNTIME;
