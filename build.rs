use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    println!("cargo:rerun-if-changed=assets/bxz.ico");
    println!("cargo:rerun-if-changed=assets/bxz-file.ico");

    /*
        Embed BXZ application icon into bxz.exe.
    */
    #[cfg(windows)]
    {
        let mut resource = winres::WindowsResource::new();

        resource.set_icon("assets/bxz.ico");

        if let Err(error) = resource.compile() {
            panic!("BXZ application icon embedding failed: {error}");
        }
    }

    /*
        Cargo profile:
            debug
            release
    */
    let profile = env::var("PROFILE")
        .expect("Could not determine Cargo profile.");

    let target_dir = PathBuf::from("target").join(&profile);
    let assets_dir = target_dir.join("assets");

    /*
        Create:

        target/debug/assets
        or
        target/release/assets
    */
    fs::create_dir_all(&assets_dir)
        .expect("Failed to create target assets directory.");

    /*
        Copy .bxz file icon next to bxz.exe.
    */
    fs::copy(
        "assets/bxz-file.ico",
        assets_dir.join("bxz-file.ico"),
    )
    .expect("Failed to copy assets/bxz-file.ico.");

    /*
        Optional PNG copy.
    */
    if let Err(error) = fs::copy(
        "assets/bxz.png",
        assets_dir.join("bxz.png"),
    ) {
        println!(
            "cargo:warning=Could not copy bxz.png: {error}"
        );
    }

    /*
        Copy the file icon PNG too, if present.
    */
    if let Err(error) = fs::copy(
        "assets/bxz-file.png",
        assets_dir.join("bxz-file.png"),
    ) {
        println!(
            "cargo:warning=Could not copy bxz-file.png: {error}"
        );
    }
}