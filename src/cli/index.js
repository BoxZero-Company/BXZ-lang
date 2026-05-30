#!/usr/bin/env node

import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

// Import command handlers - Ensure only one way to import each command
// Assuming runCommand is exported as a named export: export const runCommand
import { runCommand } from './commands/run.js';
// If other commands are also named exports, import them similarly
// For example: import { buildCommand } from './commands/build.js';
// If they are default exports, use: import buildCommand from './commands/build.js';

// Assuming other commands are also named exports, adjust if they are default exports.
import { buildCommand } from './commands/build.js';
import { initCommand } from './commands/init.js';
import { fmtCommand } from './commands/fmt.js';
import { checkCommand } from './commands/check.js';


// Setup yargs commands
const argv = yargs(hideBin(process.argv))
    .command('run <file>', 'Run a BXZ file', (yargs) => {
        yargs.positional('file', {
            describe: 'Path to the BXZ file to run',
            type: 'string',
        });
    })
    .command('build [projectDir]', 'Build a BXZ project', (yargs) => {
        yargs.positional('projectDir', {
            describe: 'Path to the BXZ project directory',
            type: 'string',
            default: '.',
        });
    })
    .command('init <projectName>', 'Initialize a new BXZ project', (yargs) => {
        yargs.positional('projectName', {
            describe: 'Name of the new project',
            type: 'string',
        });
    })
    .command('fmt [path]', 'Format BXZ code', (yargs) => {
        yargs.positional('path', {
            describe: 'Path to file or directory to format',
            type: 'string',
            default: '.',
        });
    })
    .command('check [path]', 'Check BXZ code for errors', (yargs) => {
        yargs.positional('path', {
            describe: 'Path to file or directory to check',
            type: 'string',
            default: '.',
        });
    })
    // IMPORTANT: If runCommand is a named export, use it as shown above.
    // If it's a default export, you'd need to adjust the import and potentially this line.
    // Assuming runCommand is now correctly imported as a named export:
    .command(runCommand) // This line might be redundant if runCommand is already defined as a command option above.
                        // However, yargs often allows passing a command object directly. Let's keep it for now
                        // but be aware it might need adjustment based on how runCommand is structured in its file.
                        // If the 'run <file>' command definition above is sufficient, this line might be removable.
    .demandCommand(1, 'You need at least one command before moving on')
    .help()
    .alias('h', 'help')
    .argv;

const command = argv._[0];

async function main() {
    try {
        switch (command) {
            case 'run':
                // Ensure argv.file is correctly passed if runCommand expects it as an argument
                // The command definition `run <file>` should populate argv.file
                await runCommand(argv.file);
                break;
            case 'build':
                await buildCommand(argv.projectDir);
                break;
            case 'init':
                await initCommand(argv.projectName);
                break;
            case 'fmt':
                await fmtCommand(argv.path);
                break;
            case 'check':
                await checkCommand(argv.path);
                break;
            default:
                console.log('Unknown command. Use --help for options.');
        }
    } catch (error) {
        console.error("CLI Error:", error.message);
        process.exit(1);
    }
}

main();
