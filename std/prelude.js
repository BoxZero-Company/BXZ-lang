// src/std/prelude.js

// Ensure BXZ_RUNTIME is available. It should be injected by the compiler/runner.
// If this prelude is loaded as a module, BXZ_RUNTIME might be passed as an argument
// or accessed via a global context provided by the runtime environment.

// For simplicity, assume BXZ_RUNTIME is globally accessible when this code runs.
// If not, the runner needs to inject it.

// Make runtime functions directly accessible for convenience
// Use try-catch in case BXZ_RUNTIME is not yet defined (e.g., during initial compilation)
let runPy, genHtml, genCss, print, readFile, writeFile;
try {
    runPy = BXZ_RUNTIME.runPy;
    genHtml = BXZ_RUNTIME.genHtml;
    genCss = BXZ_RUNTIME.genCss;
    print = BXZ_RUNTIME.print;
    readFile = BXZ_RUNTIME.readFile;
    writeFile = BXZ_RUNTIME.writeFile;
} catch (e) {
    console.warn("BXZ_RUNTIME not fully available during prelude loading. Functions may be undefined.");
    // Define dummy functions to prevent runtime errors
    runPy = () => console.error("runPy not available");
    genHtml = async () => console.error("genHtml not available");
    genCss = async () => console.error("genCss not available");
    print = console.log; // Fallback to console.log
    readFile = async () => { console.error("readFile not available"); return null; };
    writeFile = async () => { console.error("writeFile not available"); };
}


// Global constants
const PI = 3.14159;
const E = 2.71828;

// Built-in functions (examples)
function len(input) {
    if (typeof input === 'string' || Array.isArray(input)) {
        return input.length;
    }
    // Add handling for other types if needed
    return 0;
}

function typeOf(value) {
    return typeof value;
}

// Example of a function that might interact with the runtime
async function getFileContent(filePath) {
    return await readFile(filePath);
}

// If module system were implemented, exports would go here
// export { PI, E, len, typeOf, getFileContent };
