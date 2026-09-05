import sys
import subprocess
from pathlib import Path


SERVER_CONTROL = Path(__file__).resolve().parent / "ServerControl"


def main() -> None:
    bat_files = sorted(
        (
            path
            for path in SERVER_CONTROL.iterdir()
            if path.is_file() and path.suffix.lower() == ".bat"
        ),
        key=lambda path: path.name.lower(),
    )
    
    if not bat_files:
        print(f"실행할 bat 파일이 없습니다: {SERVER_CONTROL}")
        return
    
    selected = 0
    
    while True:
        subprocess.run(
            ["cmd", "/c", "cls"],
            check=False,
        )
        
        print("방향키로 선택하세요. Enter: 실행, Esc: 종료\n")
        
        for index, bat_file in enumerate(bat_files):
            prefix = "▶" if index == selected else " "
            print(f"{prefix} {bat_file.name}")
        
        key = msvcrt.getwch()
        
        if key == "\x1b": break
            
        if key in ("\r", "\n"):
            subprocess.run(
                ["cmd", "/c", "call", str(bat_files[selected])],
                cwd=SERVER_CONTROL,
                check=False,
            )
            
            print("\n아무 키나 누르면 목록으로 돌아갑니다.")
            msvcrt.getwch()
        
        elif key in ("\x00", "\xe0"):
            arrow = msvcrt.getwch()
            
            if arrow == "H":
                selected = (selected - 1) % len(bat_files)
                
            elif arrow == "P":
                selected = (selected + 1) % len(bat_files)


if __name__ == "__main__":
    if sys.platform != "win32":
        sys.exit("Windows에서만 실행할 수 있습니다.")
    
    import msvcrt
    
    main()