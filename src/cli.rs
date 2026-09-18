use std::env;
use std::io::{self, Write};
use std::process::Command;

const OFFICIAL_VERSION: &str = "v1.2.2.1";

#[cfg(windows)]
fn enable_windows_ansi() -> bool {
    let status = Command::new("powershell")
        .args([
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            r#"
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class BXZConsole {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr GetStdHandle(int nStdHandle);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);
}
'@
$h = [BXZConsole]::GetStdHandle(-11)
$m = 0
if ($h -ne [IntPtr]::Zero -and [BXZConsole]::GetConsoleMode($h, [ref]$m)) {
    [void][BXZConsole]::SetConsoleMode($h, ($m -bor 4))
    exit 0
}
exit 1
"#,
        ])
        .status();

    status.map(|s| s.success()).unwrap_or(false)
}

#[cfg(not(windows))]
fn enable_windows_ansi() -> bool { false }

fn supports_ansi() -> bool {
    #[cfg(windows)]
    { enable_windows_ansi() }

    #[cfg(not(windows))]
    {
        env::var_os("NO_COLOR").is_none()
            && (env::var_os("TERM").is_some() || env::var_os("COLORTERM").is_some())
    }
}

fn clear_screen(color: bool) {
    if color {
        print!("\x1b[2J\x1b[H");
        let _ = io::stdout().flush();
        return;
    }

    #[cfg(windows)]
    {
        let _ = Command::new("cmd").args(["/C", "cls"]).status();
    }

    #[cfg(not(windows))]
    {
        print!("\n\n");
        let _ = io::stdout().flush();
    }
}

fn prompt(color: bool) {
    if color {
        print!("\x1b[36m>>>\x1b[0m ");
    } else {
        print!(">>> ");
    }
    let _ = io::stdout().flush();
}

fn banner(color: bool) {
    if color {
        println!("\x1b[36mBXZ-lang {OFFICIAL_VERSION}\x1b[0m");
        println!("\x1b[90mInteractive shell • type `help` for commands\x1b[0m");
    } else {
        println!("BXZ-lang {OFFICIAL_VERSION}");
        println!("Interactive shell • type `help` for commands");
    }
    println!();
}

fn help(color: bool) {
    if color {
        println!("\x1b[33mCommands\x1b[0m");
    } else {
        println!("Commands");
    }
    println!("  help                 Show this help");
    println!("  about                Show BXZ-lang information");
    println!("  version              Show the language version");
    println!("  run <file.bxz>       Run a BXZ source file");
    println!("  check <file.bxz>     Check a BXZ source file");
    println!("  print <text>         Print text");
    println!("  clear                Clear the console");
    println!("  exit / quit          Leave the REPL");
    println!();
    println!("CLI:");
    println!("  bxz -v, --version");
    println!("  bxz -h, --help");
    println!("  bxz -a, --about");
    println!("  bxz -s, --server");
    println!("  bxz -p, --port <port>");
}

fn about() {
    println!("BXZ-lang {OFFICIAL_VERSION}");
    println!("Developer : BXZ Language Team");
    println!("Maintainer: boxzero.company");
    println!("Runtime   : Rust + x86-64 Assembly");
    println!("Platform  : Windows");
    println!("REPL      : enabled");
}

fn error(message: &str, color: bool) {
    if color {
        eprintln!("\x1b[33m[BXZ] {message}\x1b[0m");
    } else {
        eprintln!("[BXZ] {message}");
    }
}

fn run_file(path: &str, color: bool) -> i32 {
    match crate::runtime::run_file(path) {
        Ok(()) => 0,
        Err(err) => {
            error(&err.to_string(), color);
            1
        }
    }
}

fn check_file(path: &str, color: bool) -> i32 {
    match std::fs::read_to_string(path) {
        Ok(source) => {
            let tokens = crate::lexer::lex(&source);
            match crate::parser::parse(tokens) {
                Ok(_) => {
                    println!("[BXZ] OK: {path}");
                    0
                }
                Err(err) => {
                    error(&err, color);
                    1
                }
            }
        }
        Err(err) => {
            error(&format!("cannot read '{path}': {err}"), color);
            1
        }
    }
}

fn repl() {
    let color = supports_ansi();
    banner(color);

    let stdin = io::stdin();

    loop {
        prompt(color);

        let mut line = String::new();
        match stdin.read_line(&mut line) {
            Ok(0) => {
                println!();
                break;
            }
            Ok(_) => {}
            Err(err) => {
                error(&format!("input error: {err}"), color);
                break;
            }
        }

        let input = line.trim();
        if input.is_empty() {
            continue;
        }

        match input {
            "help" | "?" => help(color),
            "about" => about(),
            "version" | "-v" | "--version" => println!("BXZ-lang {OFFICIAL_VERSION}"),
            "clear" | "cls" => {
                clear_screen(color);
                banner(color);
            }
            "exit" | "quit" | ":q" => {
                println!("Goodbye.");
                break;
            }
            "run" => error("usage: run <file.bxz>", color),
            "check" => error("usage: check <file.bxz>", color),
            "print" => error("usage: print <text>", color),
            cmd if cmd.starts_with("run ") => {
                let _ = run_file(cmd[4..].trim(), color);
            }
            cmd if cmd.starts_with("check ") => {
                let _ = check_file(cmd[6..].trim(), color);
            }
            cmd if cmd.starts_with("print ") => println!("{}", &cmd[6..]),
            _ => error("unknown command. Type `help` to see available commands.", color),
        }
    }
}

pub fn run() {
    let args: Vec<String> = env::args().skip(1).collect();

    if args.is_empty() {
        repl();
        return;
    }

    let mut server = false;
    let mut port = 8080u16;
    let mut source: Option<String> = None;
    let mut i = 0usize;

    while i < args.len() {
        match args[i].as_str() {
            "-v" | "--version" => {
                println!("BXZ-lang {OFFICIAL_VERSION}");
                return;
            }
            "-h" | "--help" => {
                println!("BXZ-lang {OFFICIAL_VERSION}");
                help(false);
                return;
            }
            "-a" | "--about" => {
                about();
                return;
            }
            "-s" | "--server" => server = true,
            "-p" | "--port" => {
                i += 1;
                if i >= args.len() {
                    error("--port requires a value", false);
                    std::process::exit(2);
                }
                port = match args[i].parse() {
                    Ok(v) => v,
                    Err(_) => {
                        error("invalid port", false);
                        std::process::exit(2);
                    }
                };
            }
            arg if arg.starts_with('-') => {
                error(&format!("unknown option: {arg}"), false);
                std::process::exit(2);
            }
            arg => {
                if source.is_some() {
                    error("only one source file can be supplied", false);
                    std::process::exit(2);
                }
                source = Some(arg.to_string());
            }
        }
        i += 1;
    }

    if server {
        if source.is_some() {
            error("server mode cannot be combined with a source file", false);
            std::process::exit(2);
        }
        println!("BXZ-lang {OFFICIAL_VERSION}");
        println!("Server listening on 127.0.0.1:{port}");
        crate::server::run(port);
        return;
    }

    if let Some(path) = source {
        std::process::exit(run_file(&path, false));
    }

    repl();
}
