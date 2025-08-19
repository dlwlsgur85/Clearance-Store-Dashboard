import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="클리어런스 매장 관리 시스템",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 타이틀
st.title("🏪 클리어런스 매장 관리 시스템")
st.markdown("---")

# 사이드바
st.sidebar.header("📊 대시보드 설정")

# 파일 업로드
uploaded_file = st.sidebar.file_uploader(
    "CSV 파일 업로드",
    type=['csv'],
    help="20개 컬럼이 포함된 클리어런스 데이터를 업로드하세요"
)

# 샘플 데이터 생성 함수
@st.cache_data
def load_sample_data():
    # 100개 상품 데이터 생성
    n_products = 100
    
    # 기본 패턴 생성
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

# 데이터 로드
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ 파일이 성공적으로 업로드되었습니다!")
    except Exception as e:
        st.error(f"❌ 파일 업로드 중 오류가 발생했습니다: {e}")
        df = load_sample_data()
else:
    if st.sidebar.button("📊 샘플 데이터 로드"):
        df = load_sample_data()
        st.info("📋 샘플 데이터가 로드되었습니다.")
    else:
        st.info("👆 사이드바에서 CSV 파일을 업로드하거나 샘플 데이터를 로드하세요.")
        st.stop()

# 필터 섹션
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 데이터 필터")

# 매장 필터
stores = ['전체'] + list(df['매장명'].unique())
selected_store = st.sidebar.selectbox("매장 선택", stores)

# BIZ 필터
biz_options = ['전체'] + list(df['Biz'].unique())
selected_biz = st.sidebar.selectbox("BIZ 선택", biz_options)

# 카테고리 필터
categories = ['전체'] + list(df['CATE'].unique())
selected_category = st.sidebar.selectbox("카테고리 선택", categories)

# 데이터 필터링
filtered_df = df.copy()
if selected_store != '전체':
    filtered_df = filtered_df[filtered_df['매장명'] == selected_store]
if selected_biz != '전체':
    filtered_df = filtered_df[filtered_df['Biz'] == selected_biz]
if selected_category != '전체':
    filtered_df = filtered_df[filtered_df['CATE'] == selected_category]

# 메인 대시보드
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 상품 수", len(filtered_df), delta=None)

with col2:
    total_revenue = (filtered_df['순매출할인가'] * filtered_df['월간누적판매량']).sum()
    st.metric("총 매출액", f"₩{total_revenue:,.0f}", delta=None)

with col3:
    avg_discount = filtered_df['순매출할인율'].mean()
    st.metric("평균 할인율", f"{avg_discount:.1f}%", delta=None)

with col4:
    total_stock = filtered_df['월간누적판매량'].sum()
    st.metric("총 판매량", f"{total_stock:,}", delta=None)

st.markdown("---")

# 차트 섹션
col1, col2 = st.columns(2)

with col1:
    # 매장별 매출 현황
    store_revenue = filtered_df.groupby('매장명').apply(
        lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
    ).reset_index()
    store_revenue.columns = ['매장명', '매출액']
    
    fig1 = px.bar(
        store_revenue, 
        x='매장명', 
        y='매출액',
        title="매장별 매출 현황",
        color='매출액',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # 카테고리별 재고 현황
    category_stock = filtered_df.groupby('CATE')['월간누적판매량'].sum().reset_index()
    
    fig2 = px.pie(
        category_stock,
        values='월간누적판매량',
        names='CATE',
        title="카테고리별 판매량 분포"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # 할인율 분포
    fig3 = px.histogram(
        filtered_df,
        x='순매출할인율',
        nbins=20,
        title="할인율 분포",
        color_discrete_sequence=['#FF6B6B']
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # 일별 판매량 추이
    sales_trend = filtered_df[['최근3일판매량', '최근7일판매량', '최근14일판매량', '최근21일판매량']].mean()
    
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=['3일', '7일', '14일', '21일'],
        y=sales_trend.values,
        mode='lines+markers',
        name='평균 판매량',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    fig4.update_layout(
        title="기간별 평균 판매량 추이",
        xaxis_title="기간",
        yaxis_title="판매량",
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# 데이터 테이블
st.subheader("📋 상품 데이터")

# 검색 기능
search_term = st.text_input("🔍 상품명으로 검색")
if search_term:
    filtered_df = filtered_df[filtered_df['상품명'].str.contains(search_term, case=False, na=False)]

# 테이블 표시
display_columns = [
    '매장명', '상품명', 'CATE', 'GENDER', '소비자', 
    '순매출할인율', '순매출할인가', '월간누적판매량', '일별판매량'
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    height=400
)

# 데이터 다운로드
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 필터된 데이터 다운로드",
    data=csv,
    file_name=f"클리어런스_데이터_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# 푸터
st.markdown("---")
st.markdown("### 💡 사용법")
st.markdown("""
1. **파일 업로드**: 사이드바에서 20개 컬럼이 포함된 CSV 파일을 업로드하세요
2. **필터 적용**: 매장, BIZ, 카테고리별로 데이터를 필터링할 수 있습니다  
3. **차트 분석**: 매출 현황, 재고 분포, 할인율 등을 시각적으로 확인하세요
4. **데이터 검색**: 상품명으로 특정 제품을 검색할 수 있습니다
5. **데이터 다운로드**: 필터된 결과를 CSV 파일로 다운로드하세요
""")
