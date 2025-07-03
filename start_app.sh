#!/bin/bash

# 이미지 리사이즈 프로그램 실행 스크립트 (macOS/Linux)

# 스크립트 경로 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 파이썬 실행 경로 확인
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 오류: Python이 설치되지 않았습니다."
    echo "Python 3.7 이상을 설치해주세요."
    read -p "계속하려면 Enter 키를 누르세요..."
    exit 1
fi

# 파이썬 버전 확인
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $MAJOR_VERSION -lt 3 || ($MAJOR_VERSION -eq 3 && $MINOR_VERSION -lt 7) ]]; then
    echo "❌ 오류: Python 3.7 이상이 필요합니다."
    echo "현재 버전: $PYTHON_VERSION"
    read -p "계속하려면 Enter 키를 누르세요..."
    exit 1
fi

echo "🚀 이미지 리사이즈 프로그램을 시작합니다..."
echo "Python 버전: $PYTHON_VERSION"
echo ""

# 런처 실행
$PYTHON_CMD launcher.py

# 종료 처리
echo ""
echo "프로그램이 종료되었습니다."
read -p "종료하려면 Enter 키를 누르세요..." 