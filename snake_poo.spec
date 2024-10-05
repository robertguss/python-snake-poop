# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['snake_poo.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('pygame', 'pygame'), ('fonts', 'fonts'), ('sounds', 'sounds'), ('images', 'images'), ('package_app.py', '.'), ('fart.mp3', '.'), ('icon.png', '.'), ('poop.png', '.')],
    hiddenimports=['pygame', 'pygame.mixer'],
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
    name='snake_poo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.png'],
)
app = BUNDLE(
    exe,
    name='snake_poo.app',
    icon='icon.png',
    bundle_identifier=None,
)
