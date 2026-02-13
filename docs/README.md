# My Opus Archive - 프로젝트 문서

## 프로젝트 개요

**My Opus Archive**는 클래식 음악가를 위한 공연 기록 및 관리 Streamlit 웹 애플리케이션입니다.

### 프로젝트 목표
- 클래식 음악 공연 기록을 체계적으로 관리
- 공연 정보 검색/필터링 기능
- 사용자 간 공개 아카이브 및 커뮤니티 기능 (댓글, 좋아요)
- 드롭다운 카테고리 자동 관리

### 기술 스택
- **프레임워크**: Streamlit 1.54.0
- **언어**: Python 3.12.8
- **데이터 저장**: JSON 파일 기반 (로컬)
- **버전 관리**: Git 2.53.0 + GitHub
- **IDE**: VS Code

### 저장소 구조
```
c:\vibe_0213/
├── app.py                 # 메인 Streamlit 애플리케이션
├── requirements.txt       # Python 패키지 목록
├── .gitignore            # Git 무시 파일
├── venv/                 # Python 가상환경
├── data/                 # JSON 데이터 저장소
│   ├── users.json
│   ├── performances.json
│   ├── comments.json
│   ├── likes.json
│   └── categories.json
├── docs/                 # 문서 (현재 위치)
│   ├── README.md
│   ├── SETUP.md
│   ├── FEATURES.md
│   ├── PROGRESS.md
│   ├── ARCHITECTURE.md
│   └── SESSION_NOTES.md
├── SPEC.md              # 기능 명세서
└── UNIMPLEMENT.md       # 미구현 기능 백로그
```

### 현재 버전
- **Git 커밋**: `170e8c1`
- **상태**: UI/UX 개선 진행 중
- **마지막 업데이트**: 2024년 2월 13일

## 빠른 시작

### 1. 환경 설정
```bash
cd c:\vibe_0213
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
streamlit run app.py
```

### 3. 브라우저 접속
- 로컬: `http://localhost:8501`

## 주요 기능

### ✅ 구현 완료
- 사용자 인증 (로그인/회원가입)
- 공연 기록 CRUD (생성/읽기/수정/삭제)
- 공개/비공개 설정
- 검색/필터링
- 댓글 시스템
- 좋아요 기능
- 카테고리 관리 페이지
- UI/UX 개선 (사이드바 네비게이션, 탭 기반 인증)

### 🔄 진행 중
- 댓글 입력값 자동 초기화 (완료)
- 댓글 가시성 향상

### ⏳ 미구현
- 공연 기록 수정 기능
- 비밀번호 해싱
- CSV/PDF 내보내기
- 데이터베이스 마이그레이션
- 사용자 프로필
- 팔로우 시스템

## 문서 네비게이션

- [📋 기능 명세](FEATURES.md) - 구현된 모든 기능 상세 설명
- [⚙️ 환경 설정](SETUP.md) - 개발 환경 구성 방법
- [🏗️ 앱 구조](ARCHITECTURE.md) - 코드 아키텍처 및 함수 설명
- [📈 진행 상황](PROGRESS.md) - 완료된 작업 및 남은 TODO
- [📝 세션 노트](SESSION_NOTES.md) - 개발 과정 및 주요 프롬프트

## GitHub 저장소
- URL: https://github.com/ryudh981116/my-opus-archive.git
- 메인 브랜치: `main`

## 다음 세션 체크리스트
- [ ] docs 폴더의 모든 문서 읽기
- [ ] SESSION_NOTES.md에서 마지막 세션 내용 확인
- [ ] PROGRESS.md에서 남은 TODO 확인
- [ ] 앱 실행 후 현재 상태 확인
- [ ] 다음 작업 시작

---
**마지막 정리 날짜**: 2024년 2월 13일
**작성자**: Development Session
