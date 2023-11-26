# Jet Dodge [ v1.0 ]

This is console-based game. This create by Mr. Ryto  (Rizky Sugiharto)

## How to convert .py into .exe?

- Using pyinstaller (one file): `pyinstaller src/main.py --onefile`
- Using pyinstaller (one dir): `pyinstaller src/main.py --onedir`
- Using cx-Freeze: `cxfreeze -OO -c src/main.py --target-dir dist`
- Using Nuitka (standalone / onedir): `nuitka --standalone src/main.py`
- Using Nuitka (onefile): `nuitka --onefile src/main.py`

## How to setup the repository?

1. Clone the repository, using command: `git clone https://github.com/RizkySugiharto/Jet-Dodge`
2. Install the packages, using command: `pip install -r requirements.txt`
3. Ready to debug and edit

## License

-- **MIT** ---