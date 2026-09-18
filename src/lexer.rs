#[derive(Debug, Clone, PartialEq)]
pub enum TokenKind {
    Unit,
    Seal,
    Hold,
    Emit,
    Identifier(String),
    String(String),
    Number(String),
    Assign,
    Shift,
    Newline,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub kind: TokenKind,
    pub line: usize,
    pub column: usize,
}

pub fn lex(source: &str) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut chars = source.chars().peekable();
    let mut line = 1usize;
    let mut column = 1usize;

    while let Some(ch) = chars.next() {
        match ch {
            ' ' | '\t' | '\r' => column += 1,
            '\n' => {
                tokens.push(Token { kind: TokenKind::Newline, line, column });
                line += 1;
                column = 1;
            }
            '#' => {
                while let Some(&next) = chars.peek() {
                    if next == '\n' { break; }
                    chars.next();
                    column += 1;
                }
            }
            ':' => {
                if chars.peek() == Some(&'=') {
                    chars.next();
                    tokens.push(Token { kind: TokenKind::Assign, line, column });
                    column += 2;
                } else {
                    column += 1;
                }
            }
            '<' => {
                if chars.peek() == Some(&'<') {
                    chars.next();
                    tokens.push(Token { kind: TokenKind::Shift, line, column });
                    column += 2;
                } else {
                    column += 1;
                }
            }
            '"' => {
                let start_col = column;
                column += 1;
                let mut value = String::new();

                while let Some(next) = chars.next() {
                    column += 1;
                    match next {
                        '"' => break,
                        '\\' => {
                            if let Some(escaped) = chars.next() {
                                column += 1;
                                value.push(match escaped {
                                    'n' => '\n',
                                    'r' => '\r',
                                    't' => '\t',
                                    '"' => '"',
                                    '\\' => '\\',
                                    other => other,
                                });
                            }
                        }
                        other => value.push(other),
                    }
                }

                tokens.push(Token {
                    kind: TokenKind::String(value),
                    line,
                    column: start_col,
                });
            }
            ch if ch.is_ascii_digit() => {
                let start_col = column;
                let mut value = String::from(ch);
                column += 1;

                while let Some(&next) = chars.peek() {
                    if next.is_ascii_digit() || next == '.' {
                        value.push(next);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }

                tokens.push(Token {
                    kind: TokenKind::Number(value),
                    line,
                    column: start_col,
                });
            }
            ch if ch.is_ascii_alphabetic() || ch == '_' => {
                let start_col = column;
                let mut value = String::from(ch);
                column += 1;

                while let Some(&next) = chars.peek() {
                    if next.is_ascii_alphanumeric() || next == '_' {
                        value.push(next);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }

                let kind = match value.as_str() {
                    "unit" => TokenKind::Unit,
                    "seal" => TokenKind::Seal,
                    "hold" => TokenKind::Hold,
                    "emit" => TokenKind::Emit,
                    _ => TokenKind::Identifier(value),
                };

                tokens.push(Token { kind, line, column: start_col });
            }
            _ => column += 1,
        }
    }

    tokens.push(Token { kind: TokenKind::Eof, line, column });
    tokens
}
