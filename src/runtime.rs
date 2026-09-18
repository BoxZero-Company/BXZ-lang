use std::collections::HashMap;
use std::fs;

pub fn run_file(path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let source = fs::read_to_string(path)?;
    let tokens = crate::lexer::lex(&source);
    let program = crate::parser::parse(tokens).map_err(std::io::Error::other)?;

    for unit in program.units {
        let mut vars: HashMap<String, String> = HashMap::new();

        for stmt in unit.body {
            match stmt {
                crate::parser::Stmt::Hold { name, value } => {
                    vars.insert(name, resolve(&value, &vars));
                }
                crate::parser::Stmt::Emit { value } => {
                    println!("{}", resolve(&value, &vars));
                }
            }
        }
    }

    Ok(())
}

fn resolve(value: &str, vars: &HashMap<String, String>) -> String {
    if let Some(name) = value.strip_prefix('$') {
        vars.get(name).cloned().unwrap_or_else(|| value.to_string())
    } else {
        value.to_string()
    }
}
