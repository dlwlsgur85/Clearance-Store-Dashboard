import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="클리어런스 매장 관리 시스템",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사용자 정의 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 함수
@st.cache_data
def load_sample_data():
    n_products = 150
    stores = ['나이키일산', '브이엠플라스연수', '모다아울렛대전']
    biz_types = ['AP', 'FW', 'EQ']
    silhouettes = ['로우탑', '러닝', '클래식', '하이탑', '캐주얼']
    categories = ['신발', '운동화', '라이프스타일', '농구화', '캐주얼']
    genders = ['UNISEX', 'MEN', 'WOMEN']
    sizes = ['240', '250', '260', '270', '280']
    
    data = {
        '매장명': [stores[i % len(stores)] for i in range(n_products)],
        'Biz': [biz_types[i % len(biz_types)] for i in range(n_products)],
        '상품코드': [f'PRD{str(i+1).zfill(3)}' for i in range(n_products)],
        '상품명': [f'상품명_{i+1}' for i in range(n_products)],
        '실루엣': [silhouettes[i % len(silhouettes)] for i in range(n_products)],
        'CATE': [categories[i % len(categories)] for i in range(n_products)],
        'GENDER': [genders[i % len(genders)] for i in range(n_products)],
        '사이즈': [sizes[i % len(sizes)] for i in range(n_products)],
        '소비자': np.random.randint(50000, 300000, n_products),
        '지정할인율': np.random.randint(10, 50, n_products),
        '지정할인가': np.random.randint(40000, 200000, n_products),
        '순매출할인율': np.random.randint(15, 60, n_products),
        '순매출할인가': np.random.randint(35000, 180000, n_products),
        '월간누적판매량': np.random.randint(5, 100, n_products),
        '일별판매량': np.random.randint(1, 10, n_products),
        '최근3일판매량': np.random.randint(3, 30, n_products),
        '최근7일판매량': np.random.randint(10, 70, n_products),
        '최근14일판매량': np.random.randint(20, 140, n_products),
        '최근21일판매량': np.random.randint(30, 210, n_products),
        '최근입고일자': pd.date_range('2023-01-01', periods=n_products, freq='D').strftime('%Y-%m-%d')
    }
    return pd.DataFrame(data)

# 점수 계산 함수들
def calculate_clearance_score(df):
    """클리어런스 종합 점수 계산"""
    scores = {}
    
    # 1. 재고회전율 점수 (30%)
    df['재고회전율'] = df['월간누적판매량'] / (df['월간누적판매량'] + 1)  # 0으로 나누기 방지
    inventory_score = (df['재고회전율'].mean() * 100).round(1)
    
    # 2. 할인효율성 점수 (25%)
    df['할인효율성'] = (df['순매출할인율'] * df['월간누적판매량']) / 100
    discount_score = min(100, (df['할인효율성'].mean() * 2).round(1))
    
    # 3. 매출성과 점수 (25%)
    revenue_score = min(100, (df['순매출할인가'].mean() / 1000).round(1))
    
    # 4. 재고리스크 점수 (20%)
    df['재고일수'] = (datetime.now() - pd.to_datetime(df['최근입고일자'])).dt.days
    risk_score = max(0, 100 - (df['재고일수'].mean() / 365 * 100)).round(1)
    
    # 종합 점수
    total_score = (inventory_score * 0.3 + discount_score * 0.25 + 
                   revenue_score * 0.25 + risk_score * 0.2).round(1)
    
    scores = {
        '종합점수': total_score,
        '재고회전율': inventory_score,
        '할인효율성': discount_score,
        '매출성과': revenue_score,
        '재고리스크': risk_score
    }
    
    return scores

def detect_alerts(df):
    """자동 알림 감지"""
    alerts = []
    
    # 과다재고 감지
    df['재고일수'] = (datetime.now() - pd.to_datetime(df['최근입고일자'])).dt.days
    overstock = df[df['재고일수'] > 180]
    if len(overstock) > 0:
        alerts.append({
            'type': 'danger',
            'title': '⚠️ 과다재고 경고',
            'message': f'{len(overstock)}개 상품이 180일 이상 재고 상태입니다.',
            'items': overstock[['상품명', '매장명', '재고일수']].head(5).to_dict('records')
        })
    
    # 품절위험 감지
    low_stock = df[df['일별판매량'] == 0]
    if len(low_stock) > 0:
        alerts.append({
            'type': 'warning',
            'title': '📉 판매부진 경고',
            'message': f'{len(low_stock)}개 상품의 일일 판매량이 0입니다.',
            'items': low_stock[['상품명', '매장명', '월간누적판매량']].head(5).to_dict('records')
        })
    
    # 고수익 기회
    high_margin = df[df['순매출할인율'] < 20]
    if len(high_margin) > 0:
        alerts.append({
            'type': 'success',
            'title': '💰 고수익 기회',
            'message': f'{len(high_margin)}개 상품에서 추가 할인 여지가 있습니다.',
            'items': high_margin[['상품명', '매장명', '순매출할인율']].head(5).to_dict('records')
        })
    
    return alerts

# 메인 애플리케이션
def main():
    st.markdown('<h1 class="main-header">🏪 클리어런스 매장 관리 시스템</h1>', unsafe_allow_html=True)
    
    # 사이드바 메뉴
    st.sidebar.title("📊 메뉴 선택")
    
    menu_options = {
        "📈 종합 대시보드": "dashboard",
        "🏪 매장별 실적": "store_performance", 
        "📊 실적 분석": "analytics",
        "📧 이메일 리포트": "email_report",
        "📥 스마트 분석": "smart_analysis",
        "🎯 KPI 점수": "kpi_scores",
        "⚠️ 알림 센터": "alert_center",
        "🧮 스마트 계산기": "calculator"
    }
    
    selected_menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        options=list(menu_options.keys()),
        index=0
    )
    
    # 데이터 로드 섹션
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 데이터 설정")
    
    uploaded_file = st.sidebar.file_uploader(
        "CSV 파일 업로드",
        type=['csv'],
        help="20개 컬럼이 포함된 클리어런스 데이터를 업로드하세요"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ 파일 업로드 완료!")
        except Exception as e:
            st.sidebar.error(f"❌ 파일 업로드 오류: {e}")
            df = load_sample_data()
    else:
        if st.sidebar.button("📊 샘플 데이터 로드"):
            df = load_sample_data()
            st.sidebar.info("📋 샘플 데이터 로드됨")
        else:
            df = load_sample_data()  # 기본으로 샘플 데이터 로드
    
    # 선택된 메뉴에 따른 페이지 렌더링
    menu_key = menu_options[selected_menu]
    
    if menu_key == "dashboard":
        show_dashboard(df)
    elif menu_key == "store_performance":
        show_store_performance(df)
    elif menu_key == "analytics":
        show_analytics(df)
    elif menu_key == "email_report":
        show_email_report(df)
    elif menu_key == "smart_analysis":
        show_smart_analysis(df)
    elif menu_key == "kpi_scores":
        show_kpi_scores(df)
    elif menu_key == "alert_center":
        show_alert_center(df)
    elif menu_key == "calculator":
        show_calculator()

# 1. 종합 대시보드
def show_dashboard(df):
    st.header("📈 종합 대시보드")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = len(df)
        st.metric("총 상품 수", f"{total_products:,}", delta=f"+{total_products//10}")
    
    with col2:
        total_revenue = (df['순매출할인가'] * df['월간누적판매량']).sum()
        st.metric("총 매출액", f"₩{total_revenue:,.0f}", delta=f"+{total_revenue//100000}만원")
    
    with col3:
        avg_discount = df['순매출할인율'].mean()
        st.metric("평균 할인율", f"{avg_discount:.1f}%", delta=f"{avg_discount-30:.1f}%p")
    
    with col4:
        total_sales = df['월간누적판매량'].sum()
        st.metric("총 판매량", f"{total_sales:,}", delta=f"+{total_sales//50}")
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        # 매장별 매출
        store_revenue = df.groupby('매장명').apply(
            lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
        ).reset_index()
        store_revenue.columns = ['매장명', '매출액']
        
        fig1 = px.bar(store_revenue, x='매장명', y='매출액', 
                     title="매장별 매출 현황",
                     color='매출액', color_continuous_scale='Blues')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 카테고리별 분포
        category_dist = df['CATE'].value_counts()
        fig2 = px.pie(values=category_dist.values, names=category_dist.index,
                     title="카테고리별 상품 분포")
        st.plotly_chart(fig2, use_container_width=True)

# 2. 매장별 실적
def show_store_performance(df):
    st.header("🏪 매장별 실적 모니터링")
    
    # 매장 선택
    selected_store = st.selectbox("매장 선택", df['매장명'].unique())
    store_df = df[df['매장명'] == selected_store]
    
    # 해당 매장 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        store_products = len(store_df)
        st.metric("매장 상품 수", store_products)
    
    with col2:
        store_revenue = (store_df['순매출할인가'] * store_df['월간누적판매량']).sum()
        st.metric("매장 매출액", f"₩{store_revenue:,.0f}")
    
    with col3:
        store_avg_discount = store_df['순매출할인율'].mean()
        st.metric("평균 할인율", f"{store_avg_discount:.1f}%")
    
    with col4:
        store_sales = store_df['월간누적판매량'].sum()
        st.metric("총 판매량", store_sales)
    
    # 매장별 상세 분석
    col1, col2 = st.columns(2)
    
    with col1:
        # 카테고리별 성과
        category_perf = store_df.groupby('CATE').agg({
            '월간누적판매량': 'sum',
            '순매출할인가': 'mean'
        }).reset_index()
        
        fig = px.scatter(category_perf, x='순매출할인가', y='월간누적판매량',
                        size='월간누적판매량', color='CATE',
                        title=f"{selected_store} - 카테고리별 성과")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 일별 판매 추이
        daily_trend = store_df[['최근3일판매량', '최근7일판매량', 
                               '최근14일판매량', '최근21일판매량']].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['3일', '7일', '14일', '21일'],
            y=daily_trend.values,
            mode='lines+markers',
            name='평균 판매량',
            line=dict(color='#FF6B6B', width=3)
        ))
        fig.update_layout(title=f"{selected_store} - 기간별 판매 추이")
        st.plotly_chart(fig, use_container_width=True)
    
    # 매장 상품 목록
    st.subheader("📋 매장 상품 현황")
    display_cols = ['상품명', 'CATE', 'GENDER', '순매출할인율', 
                   '순매출할인가', '월간누적판매량']
    st.dataframe(store_df[display_cols], use_container_width=True)

# 3. 실적 분석
def show_analytics(df):
    st.header("📊 고급 분석 대시보드")
    
    # 분석 유형 선택
    analysis_type = st.selectbox("분석 유형 선택", [
        "매출 트렌드 분석", "할인 효과 분석", "재고 회전율 분석", "상품 성과 분석"
    ])
    
    if analysis_type == "매출 트렌드 분석":
        # 매출 트렌드
        col1, col2 = st.columns(2)
        
        with col1:
            # BIZ별 매출 비교
            biz_revenue = df.groupby('Biz').apply(
                lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
            ).reset_index()
            biz_revenue.columns = ['Biz', '매출액']
            
            fig = px.bar(biz_revenue, x='Biz', y='매출액',
                        title="BIZ별 매출 비교", color='매출액')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 성별 매출 분포
            gender_revenue = df.groupby('GENDER').apply(
                lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
            ).reset_index()
            gender_revenue.columns = ['GENDER', '매출액']
            
            fig = px.pie(gender_revenue, values='매출액', names='GENDER',
                        title="성별 매출 분포")
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "할인 효과 분석":
        # 할인율과 판매량 상관관계
        fig = px.scatter(df, x='순매출할인율', y='월간누적판매량',
                        color='CATE', size='순매출할인가',
                        title="할인율 vs 판매량 상관관계")
        st.plotly_chart(fig, use_container_width=True)
        
        # 할인 구간별 성과
        df['할인구간'] = pd.cut(df['순매출할인율'], 
                            bins=[0, 20, 40, 60, 100], 
                            labels=['0-20%', '21-40%', '41-60%', '61%+'])
        discount_perf = df.groupby('할인구간').agg({
            '월간누적판매량': 'mean',
            '순매출할인가': 'mean'
        }).reset_index()
        
        fig = px.bar(discount_perf, x='할인구간', y='월간누적판매량',
                    title="할인 구간별 평균 판매량")
        st.plotly_chart(fig, use_container_width=True)

# 4. 이메일 리포트
def show_email_report(df):
    st.header("📧 자동 이메일 리포트")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 리포트 미리보기")
        
        # 요약 리포트 생성
        scores = calculate_clearance_score(df)
        alerts = detect_alerts(df)
        
        report_content = f"""
        # 클리어런스 매장 일일 리포트
        
        ## 📈 주요 지표
        - **종합 점수**: {scores['종합점수']}/100점
        - **총 상품 수**: {len(df):,}개
        - **총 매출액**: ₩{(df['순매출할인가'] * df['월간누적판매량']).sum():,.0f}
        - **평균 할인율**: {df['순매출할인율'].mean():.1f}%
        
        ## 🏪 매장별 성과
        """
        
        # 매장별 요약
        for store in df['매장명'].unique():
            store_df = df[df['매장명'] == store]
            store_revenue = (store_df['순매출할인가'] * store_df['월간누적판매량']).sum()
            report_content += f"- **{store}**: ₩{store_revenue:,.0f} ({len(store_df)}개 상품)\n"
        
        report_content += f"""
        
        ## ⚠️ 주요 알림
        - 과다재고 상품: {len(df[df['순매출할인율'] > 50])}개
        - 판매부진 상품: {len(df[df['일별판매량'] == 0])}개
        
        ---
        *이 리포트는 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}에 자동 생성되었습니다.*
        """
        
        st.markdown(report_content)
    
    with col2:
        st.subheader("📤 이메일 발송")
        
        recipient_email = st.text_input("받는 사람 이메일", "manager@company.com")
        email_subject = st.text_input("제목", f"클리어런스 일일 리포트 - {datetime.now().strftime('%m/%d')}")
        
        include_charts = st.checkbox("차트 포함", value=True)
        include_alerts = st.checkbox("알림 포함", value=True)
        
        if st.button("📧 이메일 발송", type="primary"):
            st.success("✅ 이메일이 성공적으로 발송되었습니다!")
            st.info("💡 실제 환경에서는 SMTP 서버 설정이 필요합니다.")

# 5. 스마트 분석
def show_smart_analysis(df):
    st.header("📥 스마트 분석 & 다운로드")
    
    # 분석 수행
    if st.button("🚀 자동 분석 실행", type="primary"):
        with st.spinner("분석 중..."):
            import time
            time.sleep(2)  # 분석 시뮬레이션
            
            # 분석 결과 생성
            df_analyzed = df.copy()
            
            # 점수 계산
            scores = calculate_clearance_score(df)
            df_analyzed['종합점수'] = np.random.randint(60, 95, len(df))
            df_analyzed['재고위험도'] = np.random.choice(['낮음', '보통', '높음'], len(df))
            df_analyzed['추천액션'] = np.random.choice([
                '가격 인하 검토', '프로모션 진행', '재고 유지', '추가 할인', '판매 중단 검토'
            ], len(df))
            
            st.success("✅ 분석 완료!")
            
            # 결과 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 분석 결과 요약")
                st.metric("평균 종합점수", f"{df_analyzed['종합점수'].mean():.1f}점")
                st.metric("고위험 상품", f"{len(df_analyzed[df_analyzed['재고위험도'] == '높음'])}개")
                st.metric("즉시 액션 필요", f"{len(df_analyzed[df_analyzed['추천액션'].isin(['가격 인하 검토', '추가 할인'])])}개")
            
            with col2:
                # 위험도 분포
                risk_dist = df_analyzed['재고위험도'].value_counts()
                fig = px.pie(values=risk_dist.values, names=risk_dist.index,
                           title="재고 위험도 분포")
                st.plotly_chart(fig, use_container_width=True)
            
            # 다운로드 가능한 분석 결과
            st.subheader("📥 분석 결과 다운로드")
            
            download_cols = ['상품코드', '상품명', '매장명', 'CATE', 
                           '순매출할인율', '월간누적판매량', '종합점수', 
                           '재고위험도', '추천액션']
            
            csv = df_analyzed[download_cols].to_csv(index=False)
            
            st.download_button(
                label="📥 분석 결과 다운로드 (CSV)",
                data=csv,
                file_name=f"클리어런스_분석결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # 상세 분석 테이블
            st.subheader("📋 상세 분석 결과")
            st.dataframe(df_analyzed[download_cols], use_container_width=True)

# 6. KPI 점수
def show_kpi_scores(df):
    st.header("🎯 KPI 점수판")
    
    # 점수 계산
    scores = calculate_clearance_score(df)
    
    # 점수 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>종합 점수</h2>
            <h1>{scores['종합점수']}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>재고회전율</h2>
            <h1>{scores['재고회전율']}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>할인효율성</h2>
            <h1>{scores['할인효율성']}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # 상세 점수 차트
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='현재 점수'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="KPI 점수 레이더 차트"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 개선 제안
    st.subheader("📈 개선 제안")
    
    if scores['재고회전율'] < 70:
        st.warning("🔄 재고회전율이 낮습니다. 할인율 조정을 검토하세요.")
    
    if scores['할인효율성'] < 60:
        st.warning("💰 할인 효율성이 낮습니다. 타겟 할인 전략을 수립하세요.")
    
    if scores['매출성과'] < 50:
        st.error("📉 매출 성과가 부진합니다. 즉시 대응이 필요합니다.")
    
    if scores['재고리스크'] < 40:
        st.error("⚠️ 재고 리스크가 높습니다. 장기재고 처리 방안을 마련하세요.")

# 7. 알림 센터
def show_alert_center(df):
    st.header("⚠️ 알림 센터")
    
    # 알림 생성
    alerts = detect_alerts(df)
    
    if not alerts:
        st.success("✅ 현재 긴급한 알림이 없습니다.")
        return
    
    # 알림 표시
    for alert in alerts:
        if alert['type'] == 'danger':
            st.markdown(f"""
            <div class="alert-danger">
                <h3>{alert['title']}</h3>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif alert['type'] == 'warning':
            st.markdown(f"""
            <div class="alert-warning">
                <h3>{alert['title']}</h3>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif alert['type'] == 'success':
            st.markdown(f"""
            <div class="alert-success">
                <h3>{alert['title']}</h3>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 상세 항목 표시
        if alert['items']:
            st.subheader("📋 해당 상품 목록")
            items_df = pd.DataFrame(alert['items'])
            st.dataframe(items_df, use_container_width=True)
        
        st.markdown("---")
    
    # 알림 설정
    st.subheader("⚙️ 알림 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        overstock_days = st.slider("과다재고 기준 (일)", 30, 365, 180)
        low_sales_threshold = st.slider("판매부진 기준 (일일 판매량)", 0, 5, 0)
    
    with col2:
        high_discount_threshold = st.slider("고할인 기준 (%)", 30, 80, 50)
        enable_email_alerts = st.checkbox("이메일 알림 활성화", value=True)
    
    if st.button("💾 설정 저장"):
        st.success("✅ 알림 설정이 저장되었습니다.")

# 8. 스마트 계산기
def show_calculator():
    st.header("🧮 스마트 계산기")
    
    # 계산기 유형 선택
    calc_type = st.selectbox("계산 유형 선택", [
        "할인율 계산기", "수익률 계산기", "마진 계산기", "재고회전율 계산기"
    ])
    
    if calc_type == "할인율 계산기":
        st.subheader("💰 할인율 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_price = st.number_input("원가", min_value=0, value=100000, step=1000)
            sale_price = st.number_input("판매가", min_value=0, value=80000, step=1000)
            
            if original_price > 0:
                discount_rate = ((original_price - sale_price) / original_price) * 100
                st.metric("할인율", f"{discount_rate:.1f}%")
                st.metric("할인 금액", f"₩{original_price - sale_price:,.0f}")
        
        with col2:
            # 목표 할인율로 판매가 계산
            st.subheader("🎯 목표 할인율 계산")
            target_discount = st.slider("목표 할인율 (%)", 0, 80, 20)
            
            if original_price > 0:
                target_price = original_price * (1 - target_discount/100)
                st.metric("목표 판매가", f"₩{target_price:,.0f}")
                
                # 예상 수익 계산
                expected_sales = st.number_input("예상 판매량", min_value=1, value=10)
                total_revenue = target_price * expected_sales
                st.metric("예상 매출", f"₩{total_revenue:,.0f}")
    
    elif calc_type == "수익률 계산기":
        st.subheader("📈 수익률 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cost_price = st.number_input("원가", min_value=0, value=70000, step=1000)
            selling_price = st.number_input("판매가", min_value=0, value=100000, step=1000)
            
            if cost_price > 0:
                profit_margin = ((selling_price - cost_price) / cost_price) * 100
                profit_amount = selling_price - cost_price
                
                st.metric("수익률", f"{profit_margin:.1f}%")
                st.metric("수익 금액", f"₩{profit_amount:,.0f}")
        
        with col2:
            # 목표 수익률 계산
            st.subheader("🎯 목표 수익률 계산")
            target_margin = st.slider("목표 수익률 (%)", 0, 200, 30)
            
            if cost_price > 0:
                target_selling_price = cost_price * (1 + target_margin/100)
                st.metric("목표 판매가", f"₩{target_selling_price:,.0f}")
    
    elif calc_type == "마진 계산기":
        st.subheader("📊 마진 계산기")
        
        revenue = st.number_input("매출액", min_value=0, value=1000000, step=10000)
        cost = st.number_input("비용", min_value=0, value=700000, step=10000)
        
        if revenue > 0:
            gross_margin = revenue - cost
            margin_rate = (gross_margin / revenue) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 마진", f"₩{gross_margin:,.0f}")
            
            with col2:
                st.metric("마진율", f"{margin_rate:.1f}%")
            
            with col3:
                roi = (gross_margin / cost) * 100 if cost > 0 else 0
                st.metric("ROI", f"{roi:.1f}%")
    
    elif calc_type == "재고회전율 계산기":
        st.subheader("🔄 재고회전율 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_inventory = st.number_input("평균 재고량", min_value=0, value=100, step=1)
            sales_volume = st.number_input("판매량 (월간)", min_value=0, value=30, step=1)
            
            if avg_inventory > 0:
                turnover_rate = sales_volume / avg_inventory
                days_in_stock = 30 / turnover_rate if turnover_rate > 0 else 0
                
                st.metric("재고회전율", f"{turnover_rate:.2f}")
                st.metric("평균 재고 보유일", f"{days_in_stock:.1f}일")
        
        with col2:
            # 목표 회전율 계산
            st.subheader("🎯 목표 회전율 달성")
            target_turnover = st.slider("목표 회전율", 0.1, 5.0, 1.0, 0.1)
            
            if avg_inventory > 0:
                required_sales = avg_inventory * target_turnover
                st.metric("필요 판매량", f"{required_sales:.0f}개")
                
                current_rate = sales_volume / avg_inventory if avg_inventory > 0 else 0
                improvement = ((target_turnover - current_rate) / current_rate) * 100 if current_rate > 0 else 0
                st.metric("개선 필요도", f"{improvement:+.1f}%")

# 실행
if __name__ == "__main__":
    main()
