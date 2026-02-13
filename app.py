"""
My Opus Archive - 클래식 공연 연주 내역 관리 웹앱
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# ==================== 설정 ====================
st.set_page_config(
    page_title="My Opus Archive",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 저장 경로
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
PERFORMANCES_FILE = DATA_DIR / "performances.json"
COMMENTS_FILE = DATA_DIR / "comments.json"
LIKES_FILE = DATA_DIR / "likes.json"

# ==================== 데이터 로드/저장 함수 ====================

def load_json(file_path):
    """JSON 파일 로드"""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(file_path, data):
    """JSON 파일 저장"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== 초기 세션 상태 ====================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# ==================== 사용자 관리 함수 ====================

def register_user(username, email, password):
    """사용자 등록"""
    users = load_json(USERS_FILE)
    
    if username in users:
        return False, "이미 존재하는 사용자명입니다."
    
    if any(user['email'] == email for user in users.values()):
        return False, "이미 등록된 이메일입니다."
    
    users[username] = {
        'email': email,
        'password': password,  # ⚠️ 실제 운영 환경에서는 해싱 필요
        'created_at': datetime.now().isoformat()
    }
    save_json(USERS_FILE, users)
    return True, "회원가입이 완료되었습니다."

def login_user(username, password):
    """사용자 로그인"""
    users = load_json(USERS_FILE)
    
    if username not in users:
        return False, "존재하지 않는 사용자입니다."
    
    if users[username]['password'] != password:
        return False, "비밀번호가 일치하지 않습니다."
    
    return True, "로그인 성공"

# ==================== 연주 내역 관리 함수 ====================

def add_performance(user_id, data):
    """연주 내역 추가"""
    performances = load_json(PERFORMANCES_FILE)
    
    perf_id = f"perf_{datetime.now().timestamp()}"
    performances[perf_id] = {
        'id': perf_id,
        'user_id': user_id,
        'date': data['date'],
        'venue': data['venue'],
        'pieces': data['pieces'],
        'instrument': data['instrument'],
        'sub_part': data['sub_part'],
        'is_guest': data['is_guest'],
        'guest_fee': data.get('guest_fee', ''),
        'conductor': data['conductor'],
        'ensemble_name': data['ensemble_name'],
        'is_public': data['is_public'],
        'youtube_url': data.get('youtube_url', ''),
        'poster_url': data.get('poster_url', ''),
        'created_at': datetime.now().isoformat()
    }
    save_json(PERFORMANCES_FILE, performances)
    return perf_id

def get_user_performances(username):
    """사용자의 연주 내역 조회"""
    performances = load_json(PERFORMANCES_FILE)
    user_perfs = [p for p in performances.values() if p['user_id'] == username]
    return sorted(user_perfs, key=lambda x: x['date'], reverse=True)

def get_public_performances():
    """공개 연주 내역 조회"""
    performances = load_json(PERFORMANCES_FILE)
    public_perfs = [p for p in performances.values() if p['is_public']]
    return sorted(public_perfs, key=lambda x: x['date'], reverse=True)

def delete_performance(perf_id):
    """연주 내역 삭제"""
    performances = load_json(PERFORMANCES_FILE)
    if perf_id in performances:
        del performances[perf_id]
        save_json(PERFORMANCES_FILE, performances)
        
        # 댓글과 좋아요도 함께 삭제
        comments = load_json(COMMENTS_FILE)
        comments = {k: v for k, v in comments.items() if v['performance_id'] != perf_id}
        save_json(COMMENTS_FILE, comments)
        
        likes = load_json(LIKES_FILE)
        likes = {k: v for k, v in likes.items() if v['performance_id'] != perf_id}
        save_json(LIKES_FILE, likes)
        
        return True
    return False

def update_performance(perf_id, data):
    """연주 내역 수정"""
    performances = load_json(PERFORMANCES_FILE)
    if perf_id in performances:
        performances[perf_id].update(data)
        performances[perf_id]['updated_at'] = datetime.now().isoformat()
        save_json(PERFORMANCES_FILE, performances)
        return True
    return False

# ==================== 댓글 기능 ====================

def add_comment(performance_id, user_id, content):
    """댓글 추가"""
    comments = load_json(COMMENTS_FILE)
    comment_id = f"comment_{datetime.now().timestamp()}"
    comments[comment_id] = {
        'id': comment_id,
        'performance_id': performance_id,
        'user_id': user_id,
        'content': content,
        'created_at': datetime.now().isoformat()
    }
    save_json(COMMENTS_FILE, comments)
    return comment_id

def get_comments(performance_id):
    """댓글 조회"""
    comments = load_json(COMMENTS_FILE)
    perf_comments = [c for c in comments.values() if c['performance_id'] == performance_id]
    return sorted(perf_comments, key=lambda x: x['created_at'])

def delete_comment(comment_id):
    """댓글 삭제"""
    comments = load_json(COMMENTS_FILE)
    if comment_id in comments:
        del comments[comment_id]
        save_json(COMMENTS_FILE, comments)
        return True
    return False

# ==================== 좋아요 기능 ====================

def toggle_like(performance_id, user_id):
    """좋아요 토글"""
    likes = load_json(LIKES_FILE)
    like_key = f"{performance_id}_{user_id}"
    
    if like_key in likes:
        del likes[like_key]
        save_json(LIKES_FILE, likes)
        return False, "좋아요 취소"
    else:
        likes[like_key] = {
            'performance_id': performance_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat()
        }
        save_json(LIKES_FILE, likes)
        return True, "좋아요 완료"

def get_like_count(performance_id):
    """좋아요 개수 조회"""
    likes = load_json(LIKES_FILE)
    return len([l for l in likes.values() if l['performance_id'] == performance_id])

def is_liked_by_user(performance_id, user_id):
    """사용자가 이미 좋아요했는지 확인"""
    likes = load_json(LIKES_FILE)
    like_key = f"{performance_id}_{user_id}"
    return like_key in likes

# ==================== 검색/필터 함수 ====================

def filter_performances(performances, filters):
    """연주 내역 필터링"""
    result = performances
    
    if filters['venue']:
        result = [p for p in result if filters['venue'].lower() in p['venue'].lower()]
    
    if filters['conductor']:
        result = [p for p in result if filters['conductor'].lower() in p['conductor'].lower()]
    
    if filters['ensemble']:
        result = [p for p in result if filters['ensemble'].lower() in p['ensemble_name'].lower()]
    
    if filters['instrument']:
        result = [p for p in result if filters['instrument'].lower() in p['instrument'].lower()]
    
    if filters['date_from']:
        result = [p for p in result if p['date'] >= filters['date_from']]
    
    if filters['date_to']:
        result = [p for p in result if p['date'] <= filters['date_to']]
    
    return result

# ==================== UI: 헤더 ====================

st.title("🎼 My Opus Archive")
st.markdown("_클래식 공연 연주 내역을 간편하게 기록하세요_")

# ==================== UI: 사이드바 ====================

st.sidebar.title("🎭 네비게이션")

if not st.session_state.logged_in:
    # 로그인 페이지
    st.sidebar.subheader("👤 계정")
    auth_mode = st.sidebar.radio("선택", ["로그인", "회원가입"], label_visibility="collapsed")
    
    if auth_mode == "로그인":
        st.sidebar.markdown("---")
        username = st.sidebar.text_input("사용자명", key="login_username")
        password = st.sidebar.text_input("비밀번호", type="password", key="login_password")
        
        if st.sidebar.button("🔓 로그인"):
            success, message = login_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("로그인되었습니다!")
                st.rerun()
            else:
                st.error(message)
    
    else:  # 회원가입
        st.sidebar.markdown("---")
        new_username = st.sidebar.text_input("사용자명", key="signup_username")
        new_email = st.sidebar.text_input("이메일", key="signup_email")
        new_password = st.sidebar.text_input("비밀번호", type="password", key="signup_password")
        new_password_check = st.sidebar.text_input("비밀번호 확인", type="password", key="signup_password_check")
        
        if st.sidebar.button("✍️ 회원가입"):
            if not new_username or not new_email or not new_password:
                st.error("모든 필드를 입력해주세요.")
            elif new_password != new_password_check:
                st.error("비밀번호가 일치하지 않습니다.")
            else:
                success, message = register_user(new_username, new_email, new_password)
                if success:
                    st.success(message)
                    st.info("로그인 페이지에서 로그인해주세요.")
                else:
                    st.error(message)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 계정을 만들거나 로그인하여 연주 내역을 기록하세요!")

else:
    # 로그아웃 및 페이지 선택
    st.sidebar.subheader(f"👋 {st.session_state.current_user}님")
    
    page = st.sidebar.radio(
        "페이지",
        ["내 연주 내역", "새 연주 기록", "공개 아카이브", "검색/필터"],
        label_visibility="collapsed"
    )
    
    if st.sidebar.button("🚪 로그아웃"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

# ==================== UI: 메인 콘텐츠 ====================

if not st.session_state.logged_in:
    st.markdown("""
    ---
    
    ## 🎵 My Opus Archive에 오신 것을 환영합니다!
    
    **클래식 공연 연주 내역을 체계적으로 관리하세요.**
    
    ### ✨ 주요 기능
    
    - 📝 **연주 내역 기록**: 공연 일시, 장소, 곡목, 악기, 지휘자 등 상세 정보 저장
    - 🔐 **공개/비공개 설정**: 자신의 아카이브 공개 범위 선택
    - 🔍 **검색/필터**: 날짜, 장소, 지휘자, 악기 등으로 빠르게 검색
    - 💬 **커뮤니티**: 다른 음악가의 연주를 감상하고 댓글, 좋아요 남기기
    - ✏️ **수정/삭제**: 언제든지 연주 내역 관리
    
    ### 🚀 시작하기
    
    왼쪽 사이드바에서 **회원가입** 또는 **로그인**하세요!
    """)

elif page == "내 연주 내역":
    st.header("📚 내 연주 내역")
    
    performances = get_user_performances(st.session_state.current_user)
    
    if not performances:
        st.info("아직 연주 내역이 없습니다. 새로운 연주를 기록해보세요!")
    else:
        st.markdown(f"**총 {len(performances)}건의 연주 내역**")
        
        for perf in performances:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**📍 {perf['venue']}**")
                    st.caption(f"📅 {perf['date']} | 🎻 {perf['instrument']} ({perf['sub_part']})")
                    st.caption(f"🎼 {perf['ensemble_name']} | 🎩 지휘: {perf['conductor']}")
                    
                    if perf.get('youtube_url'):
                        st.markdown(f"[🎬 유튜브 영상]({perf['youtube_url']})")
                    
                    # 곡목 표시
                    if perf['pieces']:
                        st.markdown(f"**곡목**: {' | '.join(perf['pieces'])}")
                
                with col2:
                    is_public = "🌍 공개" if perf['is_public'] else "🔒 비공개"
                    st.caption(is_public)
                
                with col3:
                    edit_btn, delete_btn = st.columns(2)
                    with edit_btn:
                        if st.button("✏️", key=f"edit_{perf['id']}", help="수정"):
                            st.session_state.editing_perf_id = perf['id']
                    with delete_btn:
                        if st.button("🗑️", key=f"delete_{perf['id']}", help="삭제"):
                            if delete_performance(perf['id']):
                                st.success("삭제되었습니다.")
                                st.rerun()

elif page == "새 연주 기록":
    st.header("✏️ 새 연주 기록")
    
    with st.form("performance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            perf_date = st.date_input("연주회 날짜", key="perf_date")
            venue = st.text_input("연주 장소", placeholder="예: 예술의전당 콘서트홀", key="perf_venue")
            conductor = st.text_input("지휘자", placeholder="예: 라포 시닉", key="perf_conductor")
        
        with col2:
            ensemble_name = st.text_input("단체명", placeholder="예: 서울 필하모닉", key="perf_ensemble")
            instrument = st.text_input("악기", placeholder="예: 바이올린", key="perf_instrument")
            sub_part = st.text_input("세부 파트", placeholder="예: 1st Violin", key="perf_sub_part")
        
        st.subheader("📋 곡목")
        col1, col2, col3 = st.columns(3)
        
        parts_dict = {}
        with col1:
            if st.checkbox("1부 있음"):
                parts_dict['1부'] = st.text_area("1부 곡목", placeholder="차이코프스키 바이올린 협주곡\n베토벤 크로이처 소나타", key="part1", height=100)
        
        with col2:
            if st.checkbox("2부 있음"):
                parts_dict['2부'] = st.text_area("2부 곡목", placeholder="드보르작 '아메리카' 교향곡", key="part2", height=100)
        
        with col3:
            if st.checkbox("앵콜 있음"):
                parts_dict['앵콜'] = st.text_area("앵콜 곡목", placeholder="크라이슬러 사랑의 기쁨", key="encore", height=100)
        
        pieces = [f"{k}: {v}" for k, v in parts_dict.items() if v]
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            is_guest = st.checkbox("객원 출연")
            if is_guest:
                guest_fee = st.number_input("페이 (원)", min_value=0, step=10000, key="guest_fee")
            else:
                guest_fee = None
        
        with col2:
            is_public = st.checkbox("공개 (다른 사용자가 볼 수 있습니다)", value=False)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            youtube_url = st.text_input("유튜브 영상 URL (선택사항)", placeholder="https://www.youtube.com/...", key="youtube_url")
        with col2:
            poster_url = st.text_input("포스터 이미지 URL (선택사항)", placeholder="https://...", key="poster_url")
        
        submitted = st.form_submit_button("💾 저장", use_container_width=True)
        
        if submitted:
            if not venue or not conductor or not ensemble_name or not instrument or not sub_part or not pieces:
                st.error("필수 정보를 모두 입력해주세요.")
            else:
                perf_data = {
                    'date': perf_date.isoformat(),
                    'venue': venue,
                    'pieces': pieces,
                    'instrument': instrument,
                    'sub_part': sub_part,
                    'is_guest': is_guest,
                    'guest_fee': guest_fee or '',
                    'conductor': conductor,
                    'ensemble_name': ensemble_name,
                    'is_public': is_public,
                    'youtube_url': youtube_url,
                    'poster_url': poster_url
                }
                perf_id = add_performance(st.session_state.current_user, perf_data)
                st.success(f"✅ 연주 내역이 저장되었습니다!")

elif page == "공개 아카이브":
    st.header("🌍 공개 아카이브")
    st.markdown("_다른 음악가들의 연주 내역을 감상하세요!_")
    
    performances = get_public_performances()
    
    if not performances:
        st.info("아직 공개된 연주 내역이 없습니다.")
    else:
        st.markdown(f"**총 {len(performances)}건의 공개 연주 내역**")
        
        for perf in performances:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**👤 {perf['user_id']}**")
                    st.markdown(f"**📍 {perf['venue']}**")
                    st.caption(f"📅 {perf['date']} | 🎻 {perf['instrument']} ({perf['sub_part']})")
                    st.caption(f"🎼 {perf['ensemble_name']} | 🎩 지휘: {perf['conductor']}")
                    
                    if perf.get('youtube_url'):
                        st.markdown(f"[🎬 유튜브 영상]({perf['youtube_url']})")
                    
                    if perf['pieces']:
                        st.markdown(f"**곡목**: {' | '.join(perf['pieces'][:3])}")
                
                with col2:
                    like_count = get_like_count(perf['id'])
                    is_liked = is_liked_by_user(perf['id'], st.session_state.current_user)
                    
                    like_button_text = f"❤️ {like_count}" if is_liked else f"🤍 {like_count}"
                    
                    if st.button(like_button_text, key=f"like_{perf['id']}", use_container_width=True):
                        toggle_like(perf['id'], st.session_state.current_user)
                        st.rerun()
                
                # 댓글
                st.markdown("**💬 댓글**")
                comments = get_comments(perf['id'])
                
                if comments:
                    for comment in comments:
                        st.caption(f"**{comment['user_id']}**: {comment['content']}")
                        if comment['user_id'] == st.session_state.current_user:
                            if st.button("삭제", key=f"delete_comment_{comment['id']}", use_container_width=False):
                                delete_comment(comment['id'])
                                st.rerun()
                else:
                    st.caption("_등록된 댓글이 없습니다._")
                
                # 댓글 입력
                new_comment = st.text_input("댓글 작성", placeholder="댓글을 입력하세요...", key=f"comment_{perf['id']}")
                if st.button("댓글 작성", key=f"submit_comment_{perf['id']}", use_container_width=True):
                    if new_comment.strip():
                        add_comment(perf['id'], st.session_state.current_user, new_comment)
                        st.success("댓글이 등록되었습니다!")
                        st.rerun()
                    else:
                        st.warning("댓글을 입력해주세요.")

elif page == "검색/필터":
    st.header("🔍 검색 및 필터")
    
    # 필터 설정
    col1, col2 = st.columns(2)
    with col1:
        filter_venue = st.text_input("장소", placeholder="예술의전당", key="filter_venue")
        filter_conductor = st.text_input("지휘자", placeholder="라포", key="filter_conductor")
        filter_ensemble = st.text_input("단체명", placeholder="서울 필", key="filter_ensemble")
    
    with col2:
        filter_instrument = st.text_input("악기", placeholder="바이올린", key="filter_instrument")
        filter_date_from = st.date_input("시작 날짜", key="filter_date_from", value=None)
        filter_date_to = st.date_input("종료 날짜", key="filter_date_to", value=None)
    
    search_scope = st.radio("검색 범위", ["내 연주 내역만", "공개 아카이브"], horizontal=True)
    
    if st.button("🔍 검색"):
        if search_scope == "내 연주 내역만":
            performances = get_user_performances(st.session_state.current_user)
        else:
            performances = get_public_performances()
        
        filters = {
            'venue': filter_venue,
            'conductor': filter_conductor,
            'ensemble': filter_ensemble,
            'instrument': filter_instrument,
            'date_from': filter_date_from.isoformat() if filter_date_from else None,
            'date_to': filter_date_to.isoformat() if filter_date_to else None
        }
        
        filtered = filter_performances(performances, filters)
        
        st.markdown(f"**검색 결과: {len(filtered)}건**")
        
        if not filtered:
            st.info("검색 결과가 없습니다.")
        else:
            for perf in filtered:
                with st.container(border=True):
                    st.markdown(f"**👤 {perf['user_id']}** | **📍 {perf['venue']}**")
                    st.caption(f"📅 {perf['date']} | 🎻 {perf['instrument']} | 🎩 {perf['conductor']}")
                    if perf['pieces']:
                        st.caption(f"곡목: {' | '.join(perf['pieces'][:2])}")

# ==================== 푸터 ====================

st.markdown("---")
st.caption("🎼 My Opus Archive v1.0 | Made with Streamlit")
