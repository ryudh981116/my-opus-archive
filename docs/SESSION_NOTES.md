# 세션 개발 일지 (Session Notes)

> 이 파일은 이전 세션의 개발 과정, 주요 프롬프트, 해결 방법을 기록합니다.
> 다음 세션에서 빠르게 상황을 파악하고 계속 진행할 수 있도록 작성됩니다.

---

## 📋 세션 타임라인 요약

### Session 1: 환경 설정 (약 1-2시간)
**목표**: Python/Streamlit/Git 환경 구성
**주요 성과**:
- Python 3.12.8 + venv 구성
- Streamlit 1.54.0 설치
- Git & GitHub 저장소 연동
- 초기 README.md 작성

### Session 2: 기본 기능 구현 (약 3-4시간)
**목표**: 코어 CRUD 기능 완성
**주요 성과**:
- 사용자 인증 (로그인/회원가입)
- 공연 기록 CRUD
- 댓글/좋아요 시스템
- 기본 공개/비공개 필터

### Session 3: UI/UX 개선 (약 2-3시간)
**목표**: 사용자 경험 개선 및 버그 수정
**주요 성과**:
- 로그인 폼 재배치 (sidebar → main content)
- 네비게이션 버튼 스타일 개선
- 카테고리 관리 페이지 추가
- StreamlitAPIException 버그 수정

### Session 4 (현재): 문서화 (약 1-2시간)
**목표**: 프로젝트 연속성 보장
**현재 성과**:
- README.md (프로젝트 개요)
- SETUP.md (환경 설정)
- FEATURES.md (기능 상세)
- PROGRESS.md (진행 상황)
- ARCHITECTURE.md (코드 구조)
- SESSION_NOTES.md (본 파일)

---

## 🎯 주요 프롬프트 및 구현 방법

### [Session 1] 프롬프트: "Python Streamlit 설치 및 초기 아카이브 앱 만들기"

**사용자 요청**:
```
Python과 Streamlit을 설치하고, 클래식 음악 공연 기록 앱을 만들어줄 수 있을까?
사용자 인증, 공연 기록, 댓글, 좋아요 기능이 필요하고
JSON 파일로 데이터를 저장할 거야.
```

**구현 과정**:
1. PowerShell에서 파이썬 설치 확인
2. venv 생성: `python -m venv venv`
3. 활성화: `.\venv\Scripts\Activate.ps1`
4. pip 업그레이드: `python -m pip install --upgrade pip`
5. Streamlit 설치: `pip install streamlit`
6. requirements.txt 작성

**핵심 선택사항**:
- 데이터베이스 vs JSON: JSON 선택 (프로토타이핑용 단순성)
- 비밀번호 해싱: 미구현 (초기 버전의 간단성 우선)
- 인증 저장소: JSON 파일 (프로토타입 단계)

---

### [Session 2] 프롬프트: "Streamlit 앱에서 사용자 인증과 공연 기록 CRUD 구현"

**사용자 요청**:
```
app.py에서 다음을 구현해줘:
1. 로그인/회원가입 페이지
2. 내 공연 목록 조회 및 열람
3. 새 공연 기록 추가
4. 공연 삭제
5. 공개/비공개 설정
6. 공개 아카이브 조회
7. 댓글 및 좋아요
```

**구현 과정**:

#### 인증 시스템
```python
# users.json 구조 설계
{
  "username": "password"
}

# 함수 구현
def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password  # 주의: plaintext!
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    return username in users and users[username] == password
```

#### 세션 상태 관리
```python
# 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.session_state['current_page'] = '내_연주_내역'
```

#### 페이지 레이아웃
```python
if not st.session_state['logged_in']:
    # 로그인 페이지 (탭 구조)
    st.tabs(["로그인", "회원가입"])
else:
    # 메인 페이지 (사이드바)
    st.sidebar.header("My Opus Archive")
    # ... 네비게이션
```

**주요 문제**: JSON 파일 동시성 (해결: 필요시 트랜잭션 추가)

---

### [Session 3] 프롬프트: "UI 개선 - 로그인 폼 위치 변경, 네비게이션 개선"

**사용자 요청**:
```
다음 5가지를 개선해줄 수 있을까?
1. 로그인 폼이 사이드바에 있는데 콘텐츠 상단으로 옮겨줄래?
2. 페이지 네비게이션을 라디오 버튼 대신 버튼 그리드로 만들어줄래?
3. 드롭다운 (장소, 악기) 선택지를 어디서 관리하는 게 좋을까?
4. 댓글 입력 후 입력창을 비워줄 수 있을까?
5. 댓글을 카드 같은 컨테이너에 넣고 더 잘 보이도록 할 수 있을까?
```

#### 1. 로그인 폼 재배치
**문제**: 로그인 폼이 사이드바와 메인 콘텐츠 모두에 표시됨 (중복)
**해결**:
- 사이드바 인증 UI 완전 제거
- 메인 콘텐츠 상단에만 auth tabs 이동
- 코드: 약 30라인 제거

**구현**:
```python
# 변경 전
if not st.session_state['logged_in']:
    st.sidebar.title("로그인")
    # ... sidebar auth code (제거됨)
    st.title("로그인")
    # ... main auth code

# 변경 후
if not st.session_state['logged_in']:
    st.title("My Opus Archive - 로그인")
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    # ... 인증 코드만 메인에
```

#### 2. 네비게이션 개선
**문제**: radio button은 UI가 딱딱함, 현재 페이지 구분이 안됨
**해결**:
- radio button → sidebar button grid 변경
- 현재 페이지는 `primary` 스타일 (파란색/강조)
- 다른 페이지는 `secondary` 스타일 (회색)

**구현**:
```python
pages = {
    "📚 내 연주 내역": "내_연주_내역",
    "✏️ 새 연주 기록": "새_연주_기록",
    "🌍 공개 아카이브": "공개_아카이브",
    "🔍 검색/필터": "검색_필터",
    "⚙️ 설정 관리": "설정_관리"
}

for page_name, page_key in pages.items():
    style = "primary" if st.session_state.get('current_page') == page_key else "secondary"
    if st.sidebar.button(page_name, use_container_width=True, type=style):
        st.session_state['current_page'] = page_key
        st.rerun()  # 중요!
```

**주요 학습**: `st.rerun()`이 색상 상태 재평가에 필수임을 발견

#### 3. 드롭다운 카테고리 관리
**문제**: 장소, 악기 등의 선택지가 코드에 hardcode되어 있음 (유지보수 어려움)
**해결**: 
- 새 파일 추가: `data/categories.json`
- 새 페이지 추가: "⚙️ 설정 관리"
- 함수 추가: `load_categories()`, `add_category()`, `remove_category()`

**구조**:
```json
{
  "venues": ["Concert Hall A", "Studio B", ...],
  "instruments": ["Piano", "Violin", ...],
  "sub_parts": ["Keyboard", "String", ...]
}
```

**사용**:
```python
# 새 연주 기록 페이지
categories = load_categories()
venue = st.selectbox("장소", categories['venues'])
```

#### 4. 댓글 입력값 초기화
**문제**: 댓글 제출 후 입력필드가 비워지지 않음
**시도 1**: 후속 세션 상태 조작
```python
# ❌ 에러
comment_text = st.text_input("댓글", key="comment_input")
if st.button("댓글 작성"):
    add_comment(performance_id, current_user, comment_text)
    st.session_state['comment_input'] = ""  # ERROR!
```

**해결방법**: `st.rerun()` 사용으로 위젯 자동 초기화

#### 5. 댓글 가시성 개선
**구현**:
```python
with st.container(border=True):  # 카드 컨테이너
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{comment['user']}**")
        st.write(comment['text'])
    with col2:
        # 좋아요, 삭제 버튼
```

**Commit**: `ea72389` (refactor: UI/UX 개선)

---

### [Session 3.5] 프롬프트: "로그인 폼 중복 제거 및 구조 정리"

**사용자 발견**: 로그인 폼이 여전히 sidebar에도 표시됨

**문제 원인**: 
```python
# sidebar에도 조건이 있었음
if not st.session_state['logged_in']:
    with st.sidebar:
        # ... auth code (아직도 있었음!)
```

**해결**:
1. sidebar 인증 섹션 완전 제거
2. 메인 페이지 구조 재정의:
   - 상단: 인증 탭 (not logged_in)
   - 중단: 네비게이션 버튼
   - 하단: 페이지 콘텐츠

**Commit**: `b521530` (fix: 로그인/회원가입 UI 개선)

---

### [Session 3.7] 프롬프트: "네비게이션 버튼 색상 상태 개선"

**사용자 발견**: 버튼들이 primary/secondary 색상을 제대로 표시하지 않음

**문제 원인**:
```python
# 문제 패턴
if st.sidebar.button(page_name, type='primary' if st.session_state['current_page'] == page_key else 'secondary'):
    st.session_state['current_page'] = page_key
    # st.rerun() 없음!  ← 페이지가 재렌더링되지 않아 색상 재평가 안됨
```

**해결**:
```python
# 올바른 패턴
if st.sidebar.button(page_name, use_container_width=True, type=style):
    st.session_state['current_page'] = page_key
    st.rerun()  # 페이지 즉시 재렌더링
```

**학습**: Streamlit에서 조건부 UI 상태는 `st.rerun()`이 필요

**Commit**: `2c09d6d` (feat: 네비게이션 버튼을 사이드바로 이동)

---

### [Session 3.9] 프롬프트: "설정 관리 페이지의 입력값 초기화 에러 해결"

**사용자 발견**: 카테고리 추가 후 입력필드가 비워지지 않고 오류 발생

**에러 메시지**:
```
StreamlitAPIException: 
st.session_state['key'] cannot be modified after a widget for that key has been instantiated
```

**에러 발생 코드**:
```python
# 라인 691-693 (설정 관리 페이지 - 새 장소 섹션)
new_venue = st.text_input("새 장소", key="new_venue")
if st.button("➕ 추가"):
    add_category('venues', new_venue)
    st.session_state['new_venue'] = ""  # ← ERROR 발생!
```

**근본 원인**:
- Streamlit은 단일 렌더링 사이클(render pass)에서 작동
- Widget 생성 후 같은 사이클에서 session_state 수정 불가
- 해결: 다음 사이클에서 widget이 기본값으로 재생성되도록 `st.rerun()` 호출

**시도 1: 직접 상태 수정 (실패)**
```python
# ❌ 같은 사이클에서 수정 시도
new_venue = st.text_input("새 장소", key="new_venue")
if st.button("➕ 추가"):
    add_category('venues', new_venue)
    st.session_state['new_venue'] = ""  # StreamlitAPIException!
```

**시도 2: value 파라미터 사용 (실패)**
```python
# ❌ widget 생성 시 value 파라미터 설정도 같은 문제 발생
new_venue = st.text_input(
    "새 장소",
    key="new_venue",
    value=st.session_state.get('new_venue', '')  # StreamlitAPIException!
)
```

**해결책: st.rerun() 패턴 (성공)**
```python
# ✅ st.rerun()으로 다음 사이클에서 자동 초기화
col1, col2 = st.columns([3, 1])
with col1:
    new_venue = st.text_input("새 장소", key="new_venue")
with col2:
    if st.button("➕ 추가"):
        add_category('venues', new_venue)
        st.rerun()  # 전체 페이지 재렌더링
        # 다음 사이클에서 st.text_input은 기본값("")으로 재생성됨
```

**적용 범위**: 3곳 (venue, instrument, sub_part)

**Commits**:
- `431187f` (첫 시도 - 부분 수정)
- `170e8c1` (최종 해결 - st.rerun() 패턴)

**핵심 학습**: 
> Streamlit에서 입력 필드를 초기화하려면:
> 1. session_state 직접 수정 금지
> 2. value 파라미터도 피해야 함 (같은 오류)
> 3. st.rerun() 호출로 widget 자동 초기화 (권장)
> 4. 필요시 조건부 key 사용도 옵션

---

## ⚠️ 알려진 패턴 및 주의사항

### 1. StreamlitAPIException 방지
```python
# ❌ 위험한 패턴 (같은 사이클에서 수정)
widget_value = st.text_input("입력", key="my_key")
if submit_button:
    st.session_state['my_key'] = ""  # ERROR!

# ✅ 안전한 패턴 (rerun으로 다음 사이클 유도)
widget_value = st.text_input("입력", key="my_key")
if submit_button:
    process(widget_value)
    st.rerun()  # 자동 초기화
```

### 2. 버튼 색상 상태 동기화
```python
# ❌ 색상이 업데이트 안됨
if st.button("Click", type='primary'):
    st.session_state['active'] = True

# ✅ 색상 즉시 업데이트
if st.button("Click", type='primary'):
    st.session_state['active'] = True
    st.rerun()
```

### 3. 카테고리 동적 로드
```python
# 페이지 시작
categories = load_categories()

# selectbox에 전달
venue = st.selectbox("장소", categories['venues'])

# 카테고리 추가 후 재로드 자동!
if add_button:
    add_category('venues', new_venue)
    st.rerun()  # 다음 사이클에서 load_categories() 재실행
```

---

## 🚀 다음 세션 작업 가이드

### 즉시 시작할 수 있는 작업 (Recommended)

#### 1. 공연 기록 수정 기능
**이유**: 가장 많이 요청되는 기능
**난이도**: ⭐⭐ (중간)
**예상 시간**: 2-3시간

**구현 스케치**:
```python
# "내 연주 내역" 페이지
for performance in user_performances:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"**{performance['title']}**")
    with col2:
        if st.button("✏️ 수정", key=f"edit_{performance['id']}"):
            st.session_state['edit_mode'] = True
            st.session_state['edit_id'] = performance['id']
            st.rerun()
    with col3:
        if st.button("🗑️ 삭제", key=f"del_{performance['id']}"):
            delete_performance(performance['id'])
            st.rerun()

# 수정 폼
if st.session_state.get('edit_mode'):
    perf = get_performance(st.session_state['edit_id'])
    with st.form("edit_form"):
        title = st.text_input("제목", value=perf['title'])
        venue = st.selectbox("장소", categories['venues'], index=...)
        # 다른 필드들...
        if st.form_submit_button("저장"):
            update_performance(perf['id'], {...})
            st.rerun()
```

**함수 추가**:
```python
def update_performance(performance_id, updated_data):
    performances = load_performances()
    for perf in performances:
        if perf['id'] == performance_id:
            perf.update(updated_data)
    save_performances(performances)

def get_performance(performance_id):
    performances = load_performances()
    for perf in performances:
        if perf['id'] == performance_id:
            return perf
    return None
```

#### 2. 비밀번호 해싱 추가
**이유**: 보안 필수 (현재 plaintext!)
**난이도**: ⭐⭐ (중간)
**예상 시간**: 1-2시간

**라이브러리**: `bcrypt` 또는 `hashlib`

**변경 범위**:
- `register_user()`: 비밀번호 해시
- `login_user()`: 비교 로직 수정
- 기존 사용자 마이그레이션 (선택)

#### 3. 페이지네이션 추가
**이유**: 대량 데이터 시 성능 개선
**난이도**: ⭐⭐⭐ (높음)
**예상 시간**: 3-4시간

**구현 스케치**:
```python
# 공개 아카이브 페이지
performances = get_all_public_performances()
page = st.number_input("페이지", 1, max((len(performances)-1)//20)+1)
start = (page - 1) * 20
end = start + 20
for perf in performances[start:end]:
    # 표시...
```

---

## 📚 참고 문헌 및 리소스

### 공식 문서
- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Session State Best Practices](https://docs.streamlit.io/library/advanced-features/session-state)

### 자주 참고한 패턴
```python
# 1. 조건부 렌더링
if st.session_state.get('logged_in'):
    st.write("인증됨")
else:
    st.write("인증 필요")

# 2. 이벤트 기반 처리
if st.button("클릭"):
    do_something()
    st.rerun()

# 3. Form 처리
with st.form("my_form"):
    input1 = st.text_input("입력")
    if st.form_submit_button("제출"):
        process(input1)
```

---

## 💡 경험 및 교훈

### 배운 점

1. **st.rerun() 의 중요성**
   - 많은 Streamlit 문제의 해결책
   - 상태 동기화 필수
   - 과도한 사용은 성능 저하 초래

2. **JSON vs 데이터베이스**
   - JSON: 프로토타입 단계에서 빠름
   - 한계: 1000개 레코드 이상에서 느림
   - 추후 SQLite 마이그레이션 권장

3. **Session State 관리**
   - widget과 state의 생명주기 이해 필수
   - key 중복 주의
   - 초기화 값 설정 중요

4. **UI/UX**
   - 사용자 피드백 중요 (버튼 색상, 위치 등)
   - 작은 개선이 큰 차이 만듦
   - 테스트 필요 (실제 사용자 관점)

---

## 🎓 체크리스트 (다음 세션용)

다음 세션 시작 시:
- [ ] 모든 docs/*.md 파일 읽기 (특히 README.md + PROGRESS.md)
- [ ] 가상환경 활성화: `.\venv\Scripts\Activate.ps1`
- [ ] 앱 실행: `streamlit run app.py`
- [ ] 로그인으로 기본 기능 테스트
- [ ] Git 상태 확인: `git status`
- [ ] 우선순위 작업 선택 (위 목록 참고)
- [ ] PROGRESS.md와 SESSION_NOTES.md 업데이트

---

**작성 일시**: 2024년 2월 13일
**현재 Commit**: `170e8c1`
**상태**: 개발 계속 진행 중
**다음 Target**: 공연 기록 수정 기능 또는 비밀번호 해싱
