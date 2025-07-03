@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

rem 이미지 리사이즈 프로그램 실행 스크립트 (Windows)

rem 스크립트 경로 설정
cd /d "%~dp0"

rem 파이썬 실행 경로 확인
set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo ❌ 오류: Python이 설치되지 않았습니다.
        echo Python 3.7 이상을 설치해주세요.
        echo.
        echo Python 다운로드: https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

rem 파이썬 버전 확인
for /f "tokens=2" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i

rem 버전 파싱
for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
    set MAJOR_VERSION=%%a
    set MINOR_VERSION=%%b
)

if !MAJOR_VERSION! lss 3 (
    echo ❌ 오류: Python 3.7 이상이 필요합니다.
    echo 현재 버전: !PYTHON_VERSION!
    pause
    exit /b 1
)

if !MAJOR_VERSION! equ 3 if !MINOR_VERSION! lss 7 (
    echo ❌ 오류: Python 3.7 이상이 필요합니다.
    echo 현재 버전: !PYTHON_VERSION!
    pause
    exit /b 1
)

echo 🚀 이미지 리사이즈 프로그램을 시작합니다...
echo Python 버전: !PYTHON_VERSION!
echo.

rem 런처 실행
!PYTHON_CMD! launcher.py

rem 종료 처리
echo.
echo 프로그램이 종료되었습니다.
pause 