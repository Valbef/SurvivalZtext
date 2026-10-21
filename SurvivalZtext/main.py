import os
import sys
import colorama
colorama.just_fix_windows_console()
os.environ["PYTHONIOENCODING"] = "utf-8"
from juego import Juego

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

def main():

    juego = Juego()
    juego.menu()


if __name__ == "__main__":
    main()
