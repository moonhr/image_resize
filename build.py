#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def build_executable():
    """실행파일 빌드"""
    print("이미지 리사이즈 프로그램 빌드를 시작합니다...")
    icon_file = "resizeIcon.ico"

    # 빌드 옵션 설정
    build_options = [
        "pyinstaller",
        "--onefile",  # 단일 파일로 빌드
        "--windowed",  # 윈도우 모드 (콘솔 창 숨김)
        "--name=ImageResize",  # 실행파일 이름
        "--clean",  # 빌드 전 정리
        "--noconfirm",  # 확인 없이 진행
        "image_resize.py"
    ]

    # Windows 빌드에서는 루트의 .ico를 실행파일 아이콘으로 사용
    if sys.platform == "win32" and os.path.exists(icon_file):
        build_options.insert(-1, f"--icon={icon_file}")
    
    try:
        # 빌드 실행
        result = subprocess.run(build_options, check=True, capture_output=True, text=True)
        print("빌드가 성공적으로 완료되었습니다!")
        print(f"실행파일 위치: {os.path.join('dist', 'ImageResize.exe' if sys.platform == 'win32' else 'ImageResize')}")
        
        # 불필요한 파일들 정리
        cleanup_files = ["ImageResize.spec"]
        cleanup_dirs = ["build", "__pycache__"]
        
        for file in cleanup_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"정리됨: {file}")
        
        for dir in cleanup_dirs:
            if os.path.exists(dir):
                shutil.rmtree(dir)
                print(f"정리됨: {dir}")
                
        print("\n빌드 완료! dist 폴더에서 실행파일을 찾을 수 있습니다.")
        
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    # 필요한 패키지 확인
    try:
        import PIL
        print("Pillow가 설치되어 있습니다.")
    except ImportError:
        print("Pillow가 설치되지 않았습니다. pip install Pillow를 실행하세요.")
        sys.exit(1)
    
    try:
        import PyInstaller
        print("PyInstaller가 설치되어 있습니다.")
    except ImportError:
        print("PyInstaller가 설치되지 않았습니다. pip install pyinstaller를 실행하세요.")
        sys.exit(1)
    
    # 빌드 실행
    if build_executable():
        print("\n성공적으로 빌드되었습니다!")
    else:
        print("\n빌드에 실패했습니다.") 
