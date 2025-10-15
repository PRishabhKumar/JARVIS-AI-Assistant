# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect Porcupine resources (includes keyword files and model files)
porcupine_data = collect_data_files("pvporcupine")

a = Analysis(
    ['runJARVIS.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Frontend HTML, CSS, and JS files
        ('FRONT_END/index.html', 'FRONT_END'),
        ('FRONT_END/style.css', 'FRONT_END'),
        ('FRONT_END/main.js', 'FRONT_END'),
        ('FRONT_END/controller.js', 'FRONT_END'),
        ('FRONT_END/script.js', 'FRONT_END'),

        # Frontend Audio
        ('FRONT_END/Assets/Audio/start_sound.mp3', 'FRONT_END/Assets/Audio'),
    ] + porcupine_data,  # Include Porcupine's internal files
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='runJARVIS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='runJARVIS'
)
