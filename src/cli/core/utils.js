// src/cli/core/utils.js

// Import the file system module for Node.js
// Using sync version for simplicity in this CLI context.
// If async operations are preferred, use 'fs/promises'.
import fs from 'fs';

/**
 * Reads the content of a file.
 * @param {string} filePath - The path to the file.
 * @returns {string} The content of the file.
 * @throws {Error} If the file cannot be read.
 */
export function readFileContent(filePath) {
    try {
        // Synchronously read the file content
        const content = fs.readFileSync(filePath, 'utf-8');
        return content;
    } catch (error) {
        // Throw a more informative error if reading fails
        throw new Error(`Failed to read file "${filePath}": ${error.message}`);
    }
}

// You can add other utility functions here if needed
// export function anotherUtility() { ... }
