mod cli;
mod lexer;
mod parser;
mod runtime;
mod server;

#[cfg(windows)]
fn register_bxz_file_association() {
    use std::env;
    use std::process::Command;

    let exe = match env::current_exe() {
        Ok(path) => path,
        Err(error) => {
            eprintln!("[BXZ] Could not locate bxz.exe: {error}");
            return;
        }
    };

    let exe_dir = match exe.parent() {
        Some(path) => path,
        None => {
            eprintln!("[BXZ] Could not determine bxz.exe directory.");
            return;
        }
    };

    /*
        Expected layout:

        bxz.exe
        assets/
        └── bxz-file.ico
    */

    let icon_path = exe_dir.join("assets").join("bxz-file.ico");

    if !icon_path.exists() {
        eprintln!(
            "[BXZ] Warning: BXZ file icon was not found:\n{}",
            icon_path.display()
        );
        return;
    }

    let exe_path = exe.to_string_lossy().to_string();
    let icon_path = icon_path.to_string_lossy().to_string();

    /*
        .bxz
          ↓
        BXZFile
    */
    let extension_status = Command::new("reg")
        .args([
            "add",
            r"HKCU\Software\Classes\.bxz",
            "/ve",
            "/d",
            "BXZFile",
            "/f",
        ])
        .status();

    if extension_status.is_err() {
        eprintln!("[BXZ] Failed to register .bxz extension.");
        return;
    }

    /*
        File type name
    */
    let _ = Command::new("reg")
        .args([
            "add",
            r"HKCU\Software\Classes\BXZFile",
            "/ve",
            "/d",
            "BXZ Source File",
            "/f",
        ])
        .status();

    /*
        IMPORTANT:
        Assign bxz-file.ico to every .bxz file.
    */
    let _ = Command::new("reg")
        .args([
            "add",
            r"HKCU\Software\Classes\BXZFile\DefaultIcon",
            "/ve",
            "/d",
            &icon_path,
            "/f",
        ])
        .status();

    /*
        Double-click .bxz:
            bxz.exe "file.bxz"
    */
    let open_command = format!("\"{}\" \"%1\"", exe_path);

    let _ = Command::new("reg")
        .args([
            "add",
            r"HKCU\Software\Classes\BXZFile\shell\open\command",
            "/ve",
            "/d",
            &open_command,
            "/f",
        ])
        .status();

    /*
        Tell Windows Explorer that file associations changed.
    */
    let _ = Command::new("ie4uinit.exe")
        .arg("-show")
        .status();

    /*
        Restart Explorer so the new icon appears immediately.
    */
    let _ = Command::new("taskkill")
        .args(["/f", "/im", "explorer.exe"])
        .status();

    let _ = Command::new("explorer.exe").spawn();

    println!("[BXZ] .bxz association registered.");
    println!("[BXZ] File icon: {}", icon_path);
}

#[cfg(not(windows))]
fn register_bxz_file_association() {
    // BXZ currently uses Windows file associations.
}

fn main() {
    register_bxz_file_association();

    cli::run();
}