# 이미지 리사이즈 프로그램

PNG, JPEG 이미지를 리사이즈하여 300KB 이하로 압축하고, WebP 형식으로도 변환할 수 있는 GUI 프로그램입니다.  
**단일 파일 처리**와 **폴더 일괄 처리** 두 가지 모드를 지원합니다.

## 🚀 주요 기능

### **단일 이미지 처리**

- **지원 입력 형식**: PNG, JPEG
- **지원 출력 형식**: PNG, JPEG, WebP
- **파일 크기 제한**: 300KB 이하로 자동 조정
- **자동 파일명**: 원본명\_resize.확장자로 자동 저장
- **이미지 정보 표시**: 파일명, 형식, 크기, 해상도, 파일 크기

### **폴더 일괄 처리**

- **폴더 전체 WebP 변환**: 폴더 내 모든 이미지를 WebP로 일괄 변환
- **자동 출력 폴더**: 기존 폴더명 + "\_webp"로 새 폴더 생성
- **진행률 표시**: 실시간 처리 진행률과 결과 표시
- **대용량 처리**: 수백 개의 이미지도 한 번에 처리

### **사용자 친화적 UI**

- **직관적 인터페이스**: 명확한 모드 선택과 버튼 배치
- **실시간 피드백**: 처리 상태와 결과를 실시간으로 확인
- **품질 조정**: JPEG/WebP 형식의 품질 설정 가능 (10-100%)
- **결과 로그**: 처리된 파일 목록과 크기 정보 표시

## 🖥️ 시스템 요구사항

- Python 3.7 이상
- macOS, Windows, Linux 지원
- 최소 200MB 여유 공간 (대용량 폴더 처리 시)

## 📦 설치 및 실행

### 🎯 간편 실행 (권장)

**가상환경과 의존성을 자동으로 관리하는 방식입니다. 별도의 설치 과정이 필요하지 않습니다.**

#### macOS/Linux:

```bash
# 실행 권한 부여 (최초 1회만)
chmod +x start_app.sh

# 앱 실행
./start_app.sh
```

#### Windows:

```bash
# 배치 파일 실행
start_app.bat
```

파일 탐색기에서 `start_app.bat` (Windows) 또는 `start_app.sh` (macOS/Linux)를 더블클릭하여 실행할 수도 있습니다.

### 🔧 수동 실행

#### 1. 의존성 설치

```bash
pip3 install -r requirements.txt --break-system-packages
```

#### 2. 프로그램 실행

```bash
python3 image_resize.py
```

### 📦 실행파일 생성

실행파일을 만들려면 다음 명령어를 실행하세요:

```bash
python3 build.py
```

빌드가 완료되면 `dist` 폴더에 실행파일이 생성됩니다.

### 🪟 Windows 1클릭 설치파일(`setup.exe`) 생성

일반 사용자 배포용으로는 `ImageResize.exe`보다 `setup.exe` 배포를 권장합니다.

#### 방법 1) 로컬 Windows에서 생성

1. [Inno Setup](https://jrsoftware.org/isdl.php) 설치
2. PowerShell에서 프로젝트 폴더 이동 후 실행

```powershell
.\scripts\build_windows_installer.ps1 -AppVersion 2.0.0
```

완료 후 설치파일은 `dist\installer\ImageResize-Setup-2.0.0.exe` 형태로 생성됩니다.

#### 방법 2) GitHub Actions로 자동 생성 (권장)

- 워크플로 파일: `.github/workflows/windows-installer.yml`
- 실행 방법:
  1. GitHub 저장소 `Actions` 탭에서 **Build Windows Installer** 실행 (`workflow_dispatch`)
  2. 또는 `v2.0.0` 같은 태그 푸시 시 자동 실행

태그 푸시 예시:

```bash
git tag v2.0.0
git push origin v2.0.0
```

결과:
- Actions Artifact에 `setup.exe` 업로드
- 태그 빌드인 경우 GitHub Release Asset에도 자동 업로드

## 📖 사용법

### **단일 이미지 리사이즈**

1. **이미지 파일 선택**: "단일 이미지 파일 선택" 버튼을 클릭하여 PNG 또는 JPEG 파일을 선택합니다.

2. **이미지 정보 확인**: 선택한 이미지의 정보가 자동으로 표시됩니다.

   - 파일명
   - 형식 (PNG/JPEG)
   - 크기 (픽셀 단위)
   - 해상도
   - 파일 크기

3. **출력 설정**:

   - **출력 형식**: PNG, JPEG, WebP 중 선택
   - **품질**: JPEG/WebP의 경우 10-100% 범위에서 품질 조정

4. **리사이즈 실행**: "단일 이미지 리사이즈" 버튼을 클릭하여 처리를 시작합니다.

5. **자동 저장**: 원본 파일과 같은 폴더에 `원본명_resize.확장자` 형태로 자동 저장됩니다.

### **폴더 일괄 WebP 변환**

1. **폴더 선택**: "폴더 선택 (WebP 변환)" 버튼을 클릭하여 이미지가 들어있는 폴더를 선택합니다.

2. **폴더 정보 확인**: 선택한 폴더의 정보가 표시됩니다.

   - 폴더명
   - 발견된 이미지 파일 개수

3. **품질 설정**: WebP 변환 품질을 10-100% 범위에서 설정합니다.

4. **일괄 변환**: "폴더 전체 WebP 변환" 버튼을 클릭하여 변환을 시작합니다.

5. **진행률 확인**:

   - 상단 진행률 바에서 전체 진행률 확인
   - 하단 결과 창에서 개별 파일 처리 결과 실시간 확인

6. **결과 확인**: 원본 폴더와 같은 위치에 `폴더명_webp` 새 폴더가 생성되어 모든 WebP 파일이 저장됩니다.

## 🔧 기술적 특징

- **지능적 리사이즈**: 목표 파일 크기(300KB)에 맞춰 자동으로 이미지 크기를 조정
- **비율 유지**: 이미지의 원본 비율을 유지하면서 크기 조정
- **품질 최적화**: 각 형식별로 최적화된 압축 설정 적용
- **투명도 처리**: PNG의 투명도를 JPEG로 변환 시 흰색 배경으로 처리
- **대용량 처리**: 메모리 효율적인 배치 처리로 대량의 이미지도 안정적으로 처리
- **오류 처리**: 개별 파일 처리 실패 시에도 전체 작업 계속 진행

## 📁 파일 구조

```
image_resize/
├── .github/workflows/
│   └── windows-installer.yml  # Windows 설치파일 자동 빌드
├── installer/
│   └── ImageResize.iss         # Inno Setup 설치 스크립트
├── scripts/
│   └── build_windows_installer.ps1  # 로컬 Windows 설치파일 빌드
├── image_resize.py     # 메인 프로그램
├── launcher.py        # 런처 (가상환경 자동 관리)
├── start_app.sh       # 실행 스크립트 (macOS/Linux)
├── start_app.bat      # 실행 스크립트 (Windows)
├── build.py           # 빌드 스크립트
├── requirements.txt   # 의존성 목록
├── README.md         # 사용법 설명
├── venv/             # 가상환경 (자동 생성)
└── dist/             # 빌드 결과물
    ├── ImageResize        # 실행파일 (macOS/Linux)
    ├── ImageResize.app/   # 앱 번들 (macOS)
    └── installer/         # Windows setup.exe 출력 폴더
```

## 🎯 사용 예시

### **단일 파일 처리**

```
입력: photo.jpg (2MB)
출력: photo_resize.webp (280KB)
```

### **폴더 일괄 처리**

```
입력 폴더: vacation_photos/ (50개 이미지)
출력 폴더: vacation_photos_webp/ (50개 WebP 파일)
```

## 🛠️ 문제 해결

### **런처 관련 문제**

1. **Python을 찾을 수 없음**:

   - Python 3.7 이상이 설치되어 있는지 확인하세요.
   - macOS: `brew install python3`
   - Windows: https://www.python.org/downloads/

2. **권한 오류 (macOS/Linux)**:

   ```bash
   chmod +x start_app.sh
   ```

3. **가상환경 생성 실패**:
   - 디스크 공간이 충분한지 확인하세요.
   - `venv` 폴더를 삭제하고 다시 실행해보세요.

### **일반적인 문제**

1. **모듈을 찾을 수 없음**:

   - 런처를 사용하면 자동으로 해결됩니다.
   - 수동 실행 시:

   ```bash
   pip3 install -r requirements.txt --break-system-packages
   ```

2. **이미지 로드 실패**:

   - 파일이 손상되었거나 지원하지 않는 형식일 수 있습니다.
   - 파일 권한을 확인하세요.

3. **파일 크기가 300KB를 초과**:

   - 이미지가 너무 크거나 복잡할 경우 300KB 이하로 줄이기 어려울 수 있습니다.
   - 품질을 더 낮춰보세요.

4. **폴더 변환 실패**:
   - 출력 폴더 생성 권한을 확인하세요.
   - 디스크 공간이 충분한지 확인하세요.

### **macOS 관련 문제**

1. **tkinter 오류**:

   ```bash
   brew install python-tk
   ```

2. **PyInstaller 오류**:

   ```bash
   pip3 install --upgrade pyinstaller
   ```

3. **실행파일 실행 오류**:
   - 시스템 환경설정 > 보안 및 개인정보 보호에서 실행을 허용하세요.

### **성능 최적화**

1. **대용량 폴더 처리**:

   - 500개 이상의 이미지가 있는 폴더는 분할 처리를 권장합니다.
   - 처리 중에는 다른 무거운 작업을 피하세요.

2. **메모리 부족**:
   - 매우 큰 이미지(10MB 이상)는 개별 처리를 권장합니다.

## 🆕 버전 히스토리

### **v2.0 (현재 버전)**

- ✨ 폴더 일괄 WebP 변환 기능 추가
- 🔄 자동 파일명 생성 (기존명+resize)
- 📊 실시간 진행률 표시
- 🎨 향상된 UI 디자인
- 📋 처리 결과 로그 기능

### **v1.0**

- 🎯 단일 이미지 리사이즈 기능
- 📏 300KB 이하 자동 압축
- 🖼️ PNG, JPEG, WebP 지원
- 🎛️ 품질 조정 기능

## 📄 라이센스

이 프로그램은 개인 및 상업적 용도로 자유롭게 사용할 수 있습니다.

## 👨‍💻 개발자 정보

이미지 리사이즈 프로그램은 Python과 Pillow 라이브러리를 사용하여 개발되었습니다.

**주요 기술 스택:**

- Python 3.7+
- Pillow (PIL) - 이미지 처리
- tkinter - GUI 인터페이스
- PyInstaller - 실행파일 생성

**개발 목적:**
웹 최적화를 위한 이미지 압축과 대용량 이미지 폴더의 효율적인 WebP 변환을 목표로 개발되었습니다.
