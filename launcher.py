#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import venv
import shutil
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.main_script = self.project_root / "image_resize.py"
        
        # 플랫폼별 실행 파일 경로
        if sys.platform == "win32":
            self.python_executable = self.venv_path / "Scripts" / "python.exe"
            self.pip_executable = self.venv_path / "Scripts" / "pip.exe"
        else:
            self.python_executable = self.venv_path / "bin" / "python"
            self.pip_executable = self.venv_path / "bin" / "pip"
    
    def print_status(self, message):
        """상태 메시지 출력"""
        print(f"[이미지 리사이즈 런처] {message}")
    
    def check_venv_exists(self):
        """가상환경 존재 여부 확인"""
        return self.venv_path.exists() and self.python_executable.exists()
    
    def create_venv(self):
        """가상환경 생성"""
        try:
            self.print_status("가상환경을 생성하고 있습니다...")
            
            # 기존 가상환경이 있으면 삭제
            if self.venv_path.exists():
                shutil.rmtree(self.venv_path)
            
            # 새 가상환경 생성
            venv.create(self.venv_path, with_pip=True)
            self.print_status("가상환경 생성 완료!")
            return True
            
        except Exception as e:
            self.print_status(f"가상환경 생성 실패: {e}")
            return False
    
    def install_dependencies(self):
        """의존성 설치"""
        try:
            self.print_status("의존성을 설치하고 있습니다...")
            
            # pip 업그레이드
            subprocess.run([
                str(self.python_executable), "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, capture_output=True)
            
            # requirements.txt 설치
            if self.requirements_file.exists():
                subprocess.run([
                    str(self.pip_executable), "install", "-r", str(self.requirements_file)
                ], check=True, capture_output=True)
                
                self.print_status("의존성 설치 완료!")
            else:
                self.print_status("requirements.txt 파일이 없습니다.")
                
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_status(f"의존성 설치 실패: {e}")
            return False
    
    def check_dependencies(self):
        """의존성 확인"""
        try:
            # Pillow 확인
            result = subprocess.run([
                str(self.python_executable), "-c", "import PIL; print('Pillow OK')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def run_main_app(self):
        """메인 애플리케이션 실행"""
        try:
            self.print_status("이미지 리사이즈 프로그램을 시작합니다...")
            
            # 메인 스크립트 실행
            result = subprocess.run([
                str(self.python_executable), str(self.main_script)
            ], cwd=str(self.project_root))
            
            self.print_status("프로그램이 종료되었습니다.")
            return result.returncode == 0
            
        except Exception as e:
            self.print_status(f"프로그램 실행 실패: {e}")
            return False
    
    def setup_environment(self):
        """환경 설정 (가상환경 생성 및 의존성 설치)"""
        # 가상환경 확인
        if not self.check_venv_exists():
            self.print_status("가상환경이 없습니다. 새로 생성합니다.")
            if not self.create_venv():
                return False
        else:
            self.print_status("기존 가상환경을 사용합니다.")
        
        # 의존성 확인
        if not self.check_dependencies():
            self.print_status("의존성이 부족합니다. 설치합니다.")
            if not self.install_dependencies():
                return False
        else:
            self.print_status("의존성 확인 완료!")
        
        return True
    
    def launch(self):
        """앱 실행"""
        try:
            self.print_status("=== 이미지 리사이즈 프로그램 런처 ===")
            
            # 환경 설정
            if not self.setup_environment():
                self.print_status("환경 설정에 실패했습니다.")
                return False
            
            # 메인 앱 실행
            self.run_main_app()
            
            return True
            
        except KeyboardInterrupt:
            self.print_status("사용자에 의해 중단되었습니다.")
            return False
        except Exception as e:
            self.print_status(f"예기치 않은 오류: {e}")
            return False
        finally:
            self.print_status("런처를 종료합니다.")

def main():
    """메인 함수"""
    launcher = AppLauncher()
    success = launcher.launch()
    
    if not success:
        input("종료하려면 Enter 키를 누르세요...")
        sys.exit(1)

if __name__ == "__main__":
    main() 