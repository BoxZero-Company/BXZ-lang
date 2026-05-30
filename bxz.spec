# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bxz.py'],
    pathex=[],
    binaries=[],
    datas=[('web', 'web'), ('examples', 'examples'), ('polyglot', 'polyglot'), ('templates', 'templates'), ('api', 'api'), ('scripts', 'scripts')],
    hiddenimports=['json', 're', 'subprocess', 'http.server', 'urllib.parse'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='bxz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bxz.ico'],
)
