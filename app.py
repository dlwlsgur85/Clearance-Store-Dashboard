import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import io
import base64

# 페이지 설정
st.set_page_config(
    page_title="재고적정성 관리 시스템",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 비밀번호 상수
CORRECT_PASSWORD = "dy1234"

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-box {
        background: #ff6b6b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background: #27ae60;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-box {
        background: #3498db;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 로그인 함수
def check_password():
    """비밀번호 확인"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # 로그인 페이지
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #667eea;">🎯 재고적정성 관리 시스템</h1>
        <p style="color: #7f8c8d; font-size: 1.2em;">8단계 분류 기반 스마트 재고 관리</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                    color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <strong>📧 접속 정보</strong><br>
            승인된 사용자만 접근 가능합니다<br>
            문의: inventory@company.com
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("🔐 접속 비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("🚀 시스템 접속", use_container_width=True):
                if password == CORRECT_PASSWORD:
                    st.session_state["password_correct"] = True
                    st.success("✅ 로그인 성공!")
                    st.rerun()
                else:
                    st.error("❌ 잘못된 비밀번호입니다.")

        # 기능 소개
        st.markdown("""
        ### 🌟 주요 기능
        - ✓ 실시간 재고적정성 8단계 분석
        - ✓ BIZ별 맞춤 할인 전략 제공  
        - ✓ 스마트 계산기 (할인/수익/예측)
        - ✓ 자동 알림 & 이메일 리포트
        - ✓ FOS 엑셀 데이터 자동 분석
        - ✓ 채널별 최적 배분 가이드
        """)

    return False

# 재고적정성 계산 함수들
def calculate_grade(stock):
    """재고량에 따른 등급 계산"""
    if stock < 50: return 'A'
    elif stock < 100: return 'B'
    elif stock < 200: return 'C'
    elif stock < 500: return 'D'
    elif stock < 1000: return 'E'
    elif stock < 2000: return 'F'
    elif stock < 4000: return 'G'
    else: return 'H'

def calculate_score(stock):
    """재고량에 따른 점수 계산"""
    if stock < 50: return 70
    elif stock < 100: return 75
    elif stock < 200: return 85
    elif stock < 500: return 90
    elif stock < 1000: return 95
    elif stock < 2000: return 80
    elif stock < 4000: return 50
    else: return 20

def get_max_discount(biz, category='기본'):
    """BIZ별 최대 할인율"""
    discount_map = {
        'AP': {'BETTER': 50, '부진': 53, '차기시즌': 50, '주문없는': 53, '이월': 60, '기본': 50},
        'FW': {'BETTER': 42, '부진': 49, '차기시즌': 44, '주문없는': 54, '이월': 62, '기본': 45},
        'EQ': {'BETTER': 32, '부진': 47, '차기시즌': 36, '주문없는': 45, '이월': 51, '기본': 35}
    }
    return discount_map.get(biz, {}).get(category, 40)

def get_channels(stock):
    """재고량에 따른 운영 채널"""
    if stock < 50: return ['FOS']
    elif stock < 100: return ['FOS', '대전모다']
    elif stock < 200: return ['FOS', '대전모다', 'LF']
    else: return ['온라인']

def get_strategy(stock):
    """재고량에 따른 관리 전략"""
    if stock < 50: return '신속정리'
    elif stock < 100: return '계획적 소진'
    elif stock < 200: return '표준 운영'
    elif stock < 500: return '안정적 관리'
    elif stock < 1000: return '적극 확대'
    elif stock < 2000: return '적극 판매'
    elif stock < 4000: return '할인 검토'
    else: return '긴급 처분'

def calculate_margin(price, biz, discount_rate):
    """마진 계산"""
    cost_rates = {'AP': 0.47, 'FW': 0.51, 'EQ': 0.47}
    cost_rate = cost_rates.get(biz, 0.47)
    final_price = price * (1 - discount_rate / 100)
    cost = price * cost_rate
    return round(((final_price - cost) / final_price) * 100, 1) if final_price > 0 else 0

# 샘플 데이터 생성
@st.cache_data
def load_sample_data():
    """샘플 데이터 로드"""
    np.random.seed(42)
    
    products = []
    bizs = ['AP', 'FW', 'EQ']
    seasons = ['25FA', '25SU', '25SP', '24HO']
    categories = ['BETTER 단독 신상품', '부진 신상품', '차기시즌 주문상품', '주문없는 상품', '이월 상품']
    
    for i in range(100):
        biz = np.random.choice(bizs)
        stock = np.random.randint(1, 500)
        current_discount = np.random.randint(10, 60)
        price = np.random.randint(30000, 200000)
        
        product = {
            'name': f'{biz} 상품 {i+1:03d}',
            'biz': biz,
            'season': np.random.choice(seasons),
            'category': np.random.choice(categories),
            'stock': stock,
            'grade': calculate_grade(stock),
            'score': calculate_score(stock),
            'current_discount': current_discount,
            'max_discount': get_max_discount(biz),
            'price': price,
            'expected_margin': calculate_margin(price, biz, current_discount),
            'channels': get_channels(stock),
            'strategy': get_strategy(stock)
        }
        products.append(product)
    
    return pd.DataFrame(products)

# 메인 대시보드
def main_dashboard():
    """메인 대시보드"""
    
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🎯 재고적정성 관리 시스템</h1>
        <p style="text-align: center; color: white; margin: 0;">
            8단계 분류 기반 실시간 재고 분석 및 할인 전략 최적화
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("🔧 제어 패널")
        
        # 파일 업로드
        uploaded_file = st.file_uploader("📁 FOS 엑셀 파일", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success("✅ 파일 업로드 성공!")
            except Exception as e:
                st.error(f"❌ 파일 처리 오류: {str(e)}")
                df = load_sample_data()
        else:
            df = load_sample_data()
        
        # 필터
        st.subheader("🔍 필터 설정")
        
        biz_filter = st.selectbox("BIZ 선택", ['전체'] + list(df['biz'].unique()))
        grade_filter = st.selectbox("등급 선택", ['전체'] + ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        
        # 이메일 설정
        st.subheader("📧 알림 설정")
        email = st.text_input("담당자 이메일", placeholder="example@company.com")
        alert_freq = st.selectbox("알림 빈도", ["실시간", "일일", "주간"])
        
        if st.button("💾 설정 저장"):
            st.session_state['email_settings'] = {'email': email, 'frequency': alert_freq}
            st.success("설정이 저장되었습니다!")

    # 데이터 필터링
    filtered_df = df.copy()
    if biz_filter != '전체':
        filtered_df = filtered_df[filtered_df['biz'] == biz_filter]
    if grade_filter != '전체':
        filtered_df = filtered_df[filtered_df['grade'] == grade_filter]

    # 메트릭스
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = len(filtered_df)
        st.metric("📦 총 상품 수", f"{total_products:,}")
    
    with col2:
        avg_score = filtered_df['score'].mean()
        st.metric("🎯 평균 점수", f"{avg_score:.1f}점")
    
    with col3:
        risk_products = len(filtered_df[filtered_df['grade'].isin(['F', 'G', 'H'])])
        st.metric("🚨 위험 상품", f"{risk_products}")
    
    with col4:
        avg_margin = filtered_df['expected_margin'].mean()
        st.metric("💰 평균 마진", f"{avg_margin:.1f}%")

    # 알림 체크
    if risk_products > 0:
        st.markdown(f"""
        <div class="alert-box">
            🚨 <strong>긴급 알림</strong><br>
            {risk_products}개 상품이 과다재고 상태입니다. 즉시 대응이 필요합니다.
        </div>
        """, unsafe_allow_html=True)

    # 차트 섹션
    st.subheader("📊 분석 차트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 등급별 분포
        grade_counts = filtered_df['grade'].value_counts().sort_index()
        fig1 = px.pie(
            values=grade_counts.values, 
            names=[f"{g}급" for g in grade_counts.index],
            title="등급별 상품 분포",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # BIZ별 현황
        biz_data = filtered_df.groupby('biz').agg({
            'name': 'count',
            'current_discount': 'mean'
        }).round(1)
        
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(
            go.Bar(x=biz_data.index, y=biz_data['name'], name="상품 수"),
            secondary_y=False,
        )
        fig2.add_trace(
            go.Scatter(x=biz_data.index, y=biz_data['current_discount'], 
                      mode='lines+markers', name="평균 할인율"),
            secondary_y=True,
        )
        fig2.update_layout(title="BIZ별 현황 분석")
        fig2.update_yaxes(title_text="상품 수", secondary_y=False)
        fig2.update_yaxes(title_text="평균 할인율 (%)", secondary_y=True)
        st.plotly_chart(fig2, use_container_width=True)

    # 계산기 섹션
    st.subheader("🧮 할인율 계산기")
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    
    with calc_col1:
        calc_price = st.number_input("정가 (원)", value=100000, min_value=1000)
        calc_biz = st.selectbox("BIZ 선택", ['AP', 'FW', 'EQ'])
        calc_discount = st.slider("할인율 (%)", 0, 90, 30)
    
    with calc_col2:
        cost_rates = {'AP': 0.47, 'FW': 0.51, 'EQ': 0.47}
        cost_rate = cost_rates[calc_biz]
        final_price = calc_price * (1 - calc_discount / 100)
        cost = calc_price * cost_rate
        profit = final_price - cost
        profit_rate = (profit / final_price) * 100 if final_price > 0 else 0
        
        st.metric("최종 판매가", f"{final_price:,.0f}원")
        st.metric("예상 마진", f"{profit:,.0f}원")
        
    with calc_col3:
        st.metric("수익률", f"{profit_rate:.1f}%")
        
        if profit_rate > 20:
            st.success("✅ 건전한 수익률")
        elif profit_rate > 10:
            st.warning("⚠️ 주의 필요")
        else:
            st.error("🚨 손실 위험")

    # 상세 테이블
    st.subheader("📋 상세 재고 현황")
    
    # 테이블 표시용 데이터 준비
    display_df = filtered_df.copy()
    display_df['channels_str'] = display_df['channels'].apply(lambda x: ', '.join(x))
    
    columns_to_show = ['name', 'biz', 'season', 'stock', 'grade', 'score', 
                      'current_discount', 'max_discount', 'expected_margin', 
                      'channels_str', 'strategy']
    
    column_names = {
        'name': '상품명',
        'biz': 'BIZ',
        'season': '시즌',
        'stock': '재고량',
        'grade': '등급',
        'score': '점수',
        'current_discount': '현재 할인율(%)',
        'max_discount': '최대 할인율(%)',
        'expected_margin': '예상 마진(%)',
        'channels_str': '운영 채널',
        'strategy': '관리 전략'
    }
    
    st.dataframe(
        display_df[columns_to_show].rename(columns=column_names),
        use_container_width=True,
        hide_index=True
    )
    
    # 다운로드 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            "📊 CSV 다운로드",
            csv,
            "inventory_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    with col2:
        if st.button("📧 리포트 발송"):
            if 'email_settings' in st.session_state and st.session_state['email_settings']['email']:
                st.success("✅ 리포트가 발송되었습니다!")
            else:
                st.error("❌ 이메일 설정을 먼저 완료해주세요.")

# 메인 실행
def main():
    if check_password():
        main_dashboard()

if __name__ == "__main__":
    main()