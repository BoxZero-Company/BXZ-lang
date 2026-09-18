use std::io::{Read, Write};
use std::net::TcpListener;

pub fn run(port: u16) {
    let listener = match TcpListener::bind(("127.0.0.1", port)) {
        Ok(listener) => listener,
        Err(err) => {
            eprintln!("[BXZ] server error: {err}");
            return;
        }
    };

    for stream in listener.incoming() {
        let Ok(mut stream) = stream else { continue };
        let mut buffer = [0u8; 1024];
        let _ = stream.read(&mut buffer);

        let body = "BXZ-lang server is running.";
        let response = format!(
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
            body.len(), body
        );

        let _ = stream.write_all(response.as_bytes());
    }
}
