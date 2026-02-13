# 애플리케이션 아키텍처

## 📁 파일 구조

```
c:\vibe_0213/
├── app.py                          # 메인 Streamlit 애플리케이션 (716 라인)
├── requirements.txt                # Python 의존성
├── .gitignore                      # Git 무시 파일
├── README.md                       # 프로젝트 설명
├── SPEC.md                         # 기능 명세서
├── UNIMPLEMENT.md                  # 미완성 기능 목록
├── data/                           # JSON 데이터 파일
│   ├── users.json                  # 사용자 계정 정보
│   ├── performances.json           # 공연 기록
│   ├── comments.json               # 댓글 데이터
│   ├── likes.json                  # 좋아요 데이터
│   └── categories.json             # 드롭다운 카테고리
├── docs/                           # 문서 (이번 세션)
│   ├── README.md                   # 문서 네비게이션
│   ├── SETUP.md                    # 환경 설정 가이드
│   ├── FEATURES.md                 # 기능 상세 설명
│   ├── PROGRESS.md                 # 진행 상황 (현재 파일)
│   ├── ARCHITECTURE.md             # 코드 구조 (현재 파일)
│   └── SESSION_NOTES.md            # 개발 일지
└── .git/                           # Git 저장소

```

---

## 🏗️ 시스템 아키텍처

### 3계층 아키텍처

```
┌─────────────────────────────────────────┐
│        UI 계층 (Streamlit Frontend)     │
│  - 페이지 네비게이션                     │
│  - 폼 입력 (Login, New Performance)    │
│  - 데이터 표시 (Public Archive)        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  비즈니스 로직 계층 (Business Logic)    │
│  - 인증 (register, login)               │
│  - CRUD 연산 (performances)             │
│  - 댓글/좋아요 연산                     │
│  - 카테고리 관리                        │
│  - 필터링/검색                         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│   데이터 계층 (File-based persistence)  │
│  - JSON 파일 읽기/쓰기                  │
│  - 구조: {key: value} 또는 [{...}]     │
└─────────────────────────────────────────┘
```

---

## 🔑 세션 상태 (Session State)

Streamlit은 페이지 리렌더링 간 데이터 유지를 위해 `st.session_state` 사용합니다.

### 주요 상태 변수

```python
st.session_state['logged_in']       # bool - 로그인 여부
st.session_state['current_user']    # str - 현재 사용자명
st.session_state['current_page']    # str - 현재 페이지 ('내_연주_내역', '새_연주_기록' 등)
```

### 입력 필드 상태 (Settings Management)

```python
# 카테고리 입력 필드 (자동 초기화 처리)
st.session_state['new_venue']       # str - 새 장소 입력
st.session_state['new_instrument']  # str - 새 악기 입력
st.session_state['new_sub_part']    # str - 새 세부파트 입력
```

### 세션 상태 패턴 (중요!)

**✅ 올바른 패턴**: widget 생성 후 `st.rerun()` 호출

```python
col1, col2 = st.columns([3, 1])
with col1:
    new_venue = st.text_input("새 장소", key="new_venue")
with col2:
    if st.button("추가"):
        add_category('venues', new_venue)
        st.rerun()  # 페이지 재렌더링으로 모든 위젯 초기화
```

**❌ 잘못된 패턴**: widget 생성 후 session_state 직접 수정

```python
st.text_input("새 장소", key="new_venue")
if st.button("추가"):
    add_category('venues', new_venue)
    st.session_state['new_venue'] = ""  # ERROR!
```

---

## 🔄 데이터 플로우

### 1. 인증 플로우

```
사용자 입력
    ↓
[Login 탭 또는 Signup 탭]
    ↓
login_user() 또는 register_user()
    ↓
users.json 검색/추가
    ↓
st.session_state['logged_in'] = True
st.session_state['current_user'] = username
    ↓
st.rerun() → 메인 페이지로 이동
```

### 2. 공연 기록 생성 플로우

```
사용자 폼 입력
    ↓
"새 연주 기록" 페이지
    ↓
st.form("performance_form")
    ├─ 제목, 장소, 악기 등 입력
    ├─ 카테고리는 load_categories()에서 동적 로드
    └─ 제출 버튼
        ↓
add_performance() 호출
    ↓
performances.json에 추가
    ├─ ID: uuid4() 생성
    ├─ user: current_user
    ├─ is_public: True/False
    └─ timestamp: datetime.now()
        ↓
st.success("공연 기록이 추가되었습니다!")
st.rerun()
```

### 3. 공개 아카이브 조회 플로우

```
"공개 아카이브" 페이지 방문
    ↓
get_all_public_performances()
    ├─ performances.json 읽기
    ├─ is_public=True 필터링
    └─ 날짜 역순 정렬
        ↓
각 공연에 대해:
    ├─ 공연 정보 표시
    ├─ 좋아요 버튼 + 개수
    ├─ 댓글 입력 폼
    ├─ 기존 댓글 리스트 표시
    │   └─ 댓글별 좋아요, 삭제 버튼
    └─ 검색/필터 적용 시 재렌더링
```

### 4. 카테고리 관리 플로우

```
"설정 관리" 페이지
    ↓
3개 섹션 (장소, 악기, 세부파트)
    ↓
각 섹션:
    ├─ 기존 카테고리 리스트 표시
    │   ├─ 각 항목별 "🗑️ 삭제" 버튼
    │   └─ 삭제 시 remove_category() 호출
    ├─ 새 카테고리 입력 필드
    │   └─ session_state로 상태 관리
    └─ "➕ 추가" 버튼
        ├─ add_category() 호출
        ├─ categories.json 업데이트
        └─ st.rerun() 호출 (입력 필드 초기화)
```

---

## 📦 주요 함수 참고서

### 인증 함수

#### `register_user(username, password)`
```
입력: username (str), password (str)
출력: bool
처리:
  - users.json 로드
  - 중복 검사
  - 없으면 추가 후 True 반환
  - 있으면 False 반환
```

#### `login_user(username, password)`
```
입력: username (str), password (str)
출력: bool
처리:
  - users.json 로드
  - 사용자명 및 비밀번호 확인
  - 일치하면 True, 불일치하면 False
```

### 공연(Performance) CRUD 함수

#### `add_performance(title, venue, date, instrument, sub_part, is_public, notes)`
```
입력: 공연 상세 정보 (각각 str 또는 bool)
출력: None
처리:
  - uuid4()로 performance_id 생성
  - 현재 사용자명 (st.session_state['current_user']) 포함
  - performances.json에 추가
```

#### `get_user_performances(username)`
```
입력: username (str)
출력: list[dict]
처리:
  - performances.json 로드
  - username 필터링
  - 날짜 역순 정렬
  - 리스트 반환
```

#### `delete_performance(performance_id)`
```
입력: performance_id (str - UUID)
출력: None
처리:
  - performances.json 로드
  - ID 기반 필터링 (삭제)
  - 파일 업데이트
```

#### `get_all_public_performances()`
```
입력: None
출력: list[dict]
처리:
  - performances.json 로드
  - is_public=True 필터
  - 날짜 역순 정렬
```

### 댓글 함수

#### `add_comment(performance_id, username, text)`
```
입력: performance_id, username, text (all str)
출력: None
처리:
  - 새 댓글 객체 생성 (uuid4, timestamp 포함)
  - comments.json에 추가
```

#### `get_comments(performance_id)`
```
입력: performance_id (str)
출력: list[dict]
처리:
  - comments.json 로드
  - performance_id 필터
  - 시간순 정렬
```

#### `delete_comment(comment_id)`
```
입력: comment_id (str)
출력: None
처리:
  - comments.json 로드
  - ID 기반 필터 (삭제)
  - 파일 업데이트
```

### 좋아요 함수

#### `toggle_like(performance_id, username)`
```
입력: performance_id (str), username (str)
출력: None
처리:
  - likes.json 로드
  - key = f"{performance_id}_{username}"
  - 존재하면 제거, 없으면 추가
  - 파일 업데이트
```

#### `is_liked_by_user(performance_id, username)`
```
입력: performance_id (str), username (str)
출력: bool
처리:
  - likes.json 로드
  - key = f"{performance_id}_{username}"
  - 존재 여부 반환
```

#### `get_like_count(performance_id)`
```
입력: performance_id (str)
출력: int
처리:
  - likes.json 로드
  - performance_id* 패턴 매칭
  - 일치 개수 반환
```

### 카테고리 함수

#### `load_categories()`
```
입력: None
출력: dict with keys ['venues', 'instruments', 'sub_parts']
처리:
  - categories.json 로드
  - 없으면 기본값 반환 (각각 빈 리스트)
```

#### `save_categories(categories_dict)`
```
입력: categories_dict (dict)
출력: None
처리:
  - categories.json 업데이트 (전체 덮어쓰기)
```

#### `add_category(category_type, value)`
```
입력: category_type ('venues'|'instruments'|'sub_parts'), value (str)
출력: None
처리:
  - load_categories() 호출
  - 중복 확인
  - 새 값 추가
  - save_categories() 호출
```

#### `remove_category(category_type, value)`
```
입력: category_type ('venues'|'instruments'|'sub_parts'), value (str)
출력: None
처리:
  - load_categories() 호출
  - 값 필터 제거
  - save_categories() 호출
```

### 필터/검색 함수

#### `filter_performances(performances, filters)`
```
입력: 
  - performances (list[dict])
  - filters (dict) = {
      'venue': str|None,
      'instrument': str|None,
      'sub_part': str|None,
      'search_text': str|None
    }
출력: list[dict]
처리:
  - 각 필터 조건 적용 (AND 로직)
  - search_text는 제목/공연자/장소 전문 검색
```

---

## 💾 데이터 구조

### users.json
```json
{
  "username1": "password1",
  "username2": "password2"
}
```

### performances.json
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user": "username1",
    "title": "Beethoven Piano Sonata No. 8",
    "venue": "Concert Hall A",
    "date": "2024-02-10",
    "instrument": "Piano",
    "sub_part": "Keyboard",
    "is_public": true,
    "notes": "20 minutes, good performance",
    "timestamp": "2024-02-10T15:30:00"
  }
]
```

### comments.json
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "performance_id": "550e8400-e29b-41d4-a716-446655440000",
    "user": "username2",
    "text": "Great performance!",
    "timestamp": "2024-02-10T16:00:00"
  }
]
```

### likes.json
```json
{
  "550e8400-e29b-41d4-a716-446655440000_username2": true,
  "550e8400-e29b-41d4-a716-446655440000_username3": true
}
```

### categories.json
```json
{
  "venues": ["Concert Hall A", "Studio B", "Church"],
  "instruments": ["Piano", "Violin", "Cello"],
  "sub_parts": ["Keyboard", "String", "Voice"]
}
```

---

## 🎨 페이지 구조

### 페이지 1: 로그인 페이지 (before auth)
```
┌─────────────────────────────────┐
│   My Opus Archive - 로그인      │
├─────────────────────────────────┤
│ [로그인]  [회원가입]             │
│                                 │
│ [로그인 폼 또는 회원가입 폼]     │
│                                 │
└─────────────────────────────────┘
```

### 페이지 2-6: 메인 페이지 (after auth)
```
┌─────────────────────────────────┐
│   [사이드바]    [메인 콘텐츠]   │
│                                 │
│   📚 내 연주 내역              │
│   ✏️ 새 연주 기록              │
│   🌍 공개 아카이브              │
│   🔍 검색/필터                  │
│   ⚙️ 설정 관리                 │
│                                 │
│   [로그아웃]                    │
│                                 │
│                  [선택된 페이지] │
│                  콘텐츠 표시    │
│                                 │
└─────────────────────────────────┘
```

### 페이지 2.1: 내 연주 내역
- 현재 사용자의 공연 목록 표시
- 각 공연: 수정(미구현), 삭제 버튼
- 공개/비공개 토글(미구현)

### 페이지 2.2: 새 연주 기록
- 공연 정보 입력 폼
- 카테고리는 categories.json에서 동적 로드
- 공개/비공개 선택 라디오버튼

### 페이지 2.3: 공개 아카이브
- 모든 공개 공연 목록
- 각 공연별 댓글/좋아요
- 현재 사용자 것 아닌 공연에만 댓글/좋아요 가능

### 페이지 2.4: 검색/필터
- 카테고리별 필터 (장소, 악기, 세부파트)
- 텍스트 검색 (제목/공연자)
- 필터 적용 후 결과 표시

### 페이지 2.5: 설정 관리
- 3개 섹션: 장소, 악기, 세부파트
- 각 섹션: 기존 항목 표시 + 삭제 버튼
- 새 항목 추가 입력필드 + 추가 버튼

---

## 🔌 Streamlit 위젯 사용 패턴

### 페이지 네비게이션 (사이드바 버튼)

```python
st.sidebar.title("My Opus Archive")

pages = {
    "📚 내 연주 내역": "내_연주_내역",
    "✏️ 새 연주 기록": "새_연주_기록",
    "🌍 공개 아카이브": "공개_아카이브",
    "🔍 검색/필터": "검색_필터",
    "⚙️ 설정 관리": "설정_관리"
}

for page_name, page_key in pages.items():
    # 현재 페이지 = primary, 아니면 secondary
    style = "primary" if st.session_state.get('current_page') == page_key else "secondary"
    
    if st.sidebar.button(page_name, use_container_width=True, type=style):
        st.session_state['current_page'] = page_key
        st.rerun()  # 색상 재평가 필수!
```

### 폼 처리 패턴

```python
with st.form("my_form"):
    title = st.text_input("제목")
    venue = st.selectbox("장소", categories['venues'])
    submitted = st.form_submit_button("제출")
    
    if submitted:
        add_performance(title=title, venue=venue, ...)
        st.success("저장되었습니다!")
        st.rerun()
```

### 동적 카테고리 로드 패턴

```python
categories = load_categories()
st.selectbox("장소", categories['venues'])
st.selectbox("악기", categories['instruments'])
st.selectbox("세부파트", categories['sub_parts'])
```

### 입력 필드 자동 초기화 패턴

```python
# ✅ 올바른 방식
col1, col2 = st.columns([3, 1])
with col1:
    new_venue = st.text_input("새 장소", key="new_venue")
with col2:
    if st.button("추가"):
        add_category('venues', new_venue)
        st.rerun()  # 모든 위젯이 기본값으로 초기화됨
```

---

## 🔐 보안 고려사항 (현재 미해결)

### 1. 비밀번호 해싱 (미구현)
- 현재: plaintext 저장
- 개선안: bcrypt 또는 hashlib 사용

### 2. 데이터 접근 제어 (미구현)
- 현재: is_public 플래그만 확인
- 개선안: 더 세밀한 권한 관리 필요

### 3. HTTPS/SSL (미구현)
- 현재: localhost 개발 환경
- 배포 시: 반드시 필요

---

## 📊 성능 고려사항

### 현재 구현
- 데이터: 파일 기반 JSON (단순, 느림)
- 데이터 크기: ~1000개 공연 이하 권장
- 페이지 렌더링: 전체 데이터 로드 후 필터링

### 개선 방안
1. SQLite로 마이그레이션 (속도 5-10배 향상)
2. 페이지네이션 추가 (화면에 20개씩만 표시)
3. 검색 인덱싱 (텍스트 검색 최적화)

---

**마지막 업데이트**: 2024년 2월 13일
**작성자**: Development Session
