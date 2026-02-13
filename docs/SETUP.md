# 환경 설정 가이드

## 개발 환경 정보

### 운영 체제
- **OS**: Windows 11
- **Shell**: PowerShell (Windows Terminal)

### 설치된 도구

#### Python 환경
```
Python: 3.12.8
Virtual Environment: venv (C:\vibe_0213\venv)
```

#### 핵심 패키지
```
streamlit==1.54.0
```

#### 버전 관리
```
Git: 2.53.0
Git Credential Manager: 2.7.0 (브라우저 기반 인증)
```

## 초기 설정 방법

### 1단계: 가상환경 활성화

**PowerShell에서:**
```powershell
cd c:\vibe_0213
.\venv\Scripts\Activate.ps1
```

**또는 cmd에서:**
```cmd
cd c:\vibe_0213
venv\Scripts\activate.bat
```

### 2단계: 의존성 설치

```bash
pip install -r requirements.txt
```

### 3단계: 앱 실행

```bash
streamlit run app.py
```

### 4단계: 브라우저에서 접속

```
http://localhost:8501
```

## Git 설정

### 이미 완료된 설정 (다시 할 필요 없음)

```bash
# Git 사용자 정보
git config --global user.name "ryudh981116"
git config --global user.email "ryudh98@gmail.com"

# 기본 브랜치 설정
git config --global init.defaultBranch main

# GitHub 연동 (Git Credential Manager 사용)
git remote add origin https://github.com/ryudh981116/my-opus-archive.git
```

### 일반적인 Git 커맨드

**현재 변경 상태 확인:**
```bash
& 'C:\Program Files\Git\bin\git' status --short
```

**변경사항 커밋:**
```bash
& 'C:\Program Files\Git\bin\git' add .
& 'C:\Program Files\Git\bin\git' commit -m "커밋 메시지"
```

**GitHub에 푸시:**
```bash
& 'C:\Program Files\Git\bin\git' push origin main
```

**커밋 이력 확인:**
```bash
& 'C:\Program Files\Git\bin\git' log --oneline
```

## 데이터 저장소 구조

### JSON 파일 위치
```
data/
├── users.json              # 사용자 정보
├── performances.json       # 공연 기록
├── comments.json          # 댓글
├── likes.json             # 좋아요 정보
└── categories.json        # 드롭다운 카테고리
```

### 각 파일의 구조

#### users.json
```json
{
  "username": {
    "email": "user@example.com",
    "password": "plain_text_password"  // 향후 해싱 필요
  }
}
```

#### performances.json
```json
{
  "user_id": [
    {
      "id": "unique_id",
      "date": "2024-02-13",
      "venue": "예술의전당",
      "pieces": ["곡목1", "곡목2"],
      "instrument": "바이올린",
      "sub_part": "1st Violin",
      "conductor": "지휘자명",
      "ensemble_name": "단체명",
      "is_guest": false,
      "guest_fee": null,
      "is_public": true,
      "youtube_url": "",
      "poster_url": ""
    }
  ]
}
```

#### comments.json
```json
{
  "performance_id": [
    {
      "id": "unique_id",
      "user_id": "username",
      "content": "댓글 내용",
      "created_at": "2024-02-13T12:00:00"
    }
  ]
}
```

#### likes.json
```json
{
  "performance_id": ["user1", "user2", "user3"]
}
```

#### categories.json
```json
{
  "venues": ["예술의전당", "세종문화회관", ...],
  "instruments": ["바이올린", "비올라", ...],
  "sub_parts": ["1st Violin", "2nd Violin", ...]
}
```

## 문제 해결

### Streamlit 포트 충돌
포트 8501이 이미 사용중이면:
```bash
streamlit run app.py --server.port 8502
```

### Python 모듈 임포트 오류
```bash
pip install --upgrade streamlit
```

### Git 인증 오류
Git Credential Manager를 통해 브라우저 기반 인증 수행:
1. Git 명령 실행
2. 브라우저 팝업에서 GitHub 로그인
3. 완료

### 데이터 초기화
모든 JSON 파일을 삭제하면 다음 실행 시 자동으로 재생성됨

## 개발 중 유용한 팁

### Python 구문 검사
```bash
python -m py_compile app.py
```

### 작업 중 주요 파일
- **메인 앱**: `app.py`
- **패키지 목록**: `requirements.txt`
- **무시 파일**: `.gitignore`
- **명세서**: `SPEC.md`
- **백로그**: `UNIMPLEMENT.md`

### 세션 초기화 전 확인 사항
1. 모든 커밋 완료 여부
2. GitHub 푸시 완료 여부
3. 데이터 백업 (필요시)

---
**업데이트**: 2024년 2월 13일
