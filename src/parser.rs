use crate::lexer::{Token, TokenKind};

#[derive(Debug)]
pub struct Program {
    pub units: Vec<Unit>,
}

#[derive(Debug)]
pub struct Unit {
    pub name: String,
    pub body: Vec<Stmt>,
}

#[derive(Debug)]
pub enum Stmt {
    Hold { name: String, value: String },
    Emit { value: String },
}

pub fn parse(tokens: Vec<Token>) -> Result<Program, String> {
    let mut i = 0usize;
    let mut units = Vec::new();

    while i < tokens.len() {
        match &tokens[i].kind {
            TokenKind::Newline => i += 1,
            TokenKind::Eof => break,

            TokenKind::Unit => {
                i += 1;

                let name = match tokens.get(i).map(|t| &t.kind) {
                    Some(TokenKind::Identifier(value)) => value.clone(),
                    _ => return Err("expected unit name".into()),
                };
                i += 1;

                while matches!(
                    tokens.get(i).map(|t| &t.kind),
                    Some(TokenKind::Newline)
                ) {
                    i += 1;
                }

                let mut body = Vec::new();

                loop {
                    match tokens.get(i).map(|t| &t.kind) {
                        Some(TokenKind::Newline) => i += 1,

                        Some(TokenKind::Seal) => {
                            i += 1;
                            break;
                        }

                        Some(TokenKind::Hold) => {
                            i += 1;

                            let var = match tokens.get(i).map(|t| &t.kind) {
                                Some(TokenKind::Identifier(value)) => value.clone(),
                                _ => return Err("expected variable name after hold".into()),
                            };
                            i += 1;

                            if !matches!(
                                tokens.get(i).map(|t| &t.kind),
                                Some(TokenKind::Assign)
                            ) {
                                return Err("expected := after variable name".into());
                            }
                            i += 1;

                            let value = match tokens.get(i).map(|t| &t.kind) {
                                Some(TokenKind::String(value)) => value.clone(),
                                Some(TokenKind::Number(value)) => value.clone(),
                                Some(TokenKind::Identifier(value)) => format!("${value}"),
                                _ => return Err("expected a value after :=".into()),
                            };
                            i += 1;

                            body.push(Stmt::Hold { name: var, value });
                        }

                        Some(TokenKind::Emit) => {
                            i += 1;

                            if !matches!(
                                tokens.get(i).map(|t| &t.kind),
                                Some(TokenKind::Shift)
                            ) {
                                return Err("expected << after emit".into());
                            }
                            i += 1;

                            let value = match tokens.get(i).map(|t| &t.kind) {
                                Some(TokenKind::String(value)) => value.clone(),
                                Some(TokenKind::Number(value)) => value.clone(),
                                Some(TokenKind::Identifier(value)) => format!("${value}"),
                                _ => return Err("expected a value after <<".into()),
                            };
                            i += 1;

                            body.push(Stmt::Emit { value });
                        }

                        Some(other) => {
                            return Err(format!("unexpected token: {other:?}"));
                        }

                        None => {
                            return Err("unexpected end of input; expected seal".into());
                        }
                    }
                }

                units.push(Unit { name, body });
            }

            other => {
                return Err(format!("expected unit, found {other:?}"));
            }
        }
    }

    Ok(Program { units })
}
