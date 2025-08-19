import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="클리어런스 매장 관리",
    page_icon="🏪",
    layout="wide"
)

# 샘플 데이터 생성
@st.cache_data
def load_sample_data():
    n_products = 50
    
    data = {
        '매장명': ['나이키일산', '브이엠플라스연수', '모다아울렛대전'] * 17,
        'Biz': ['AP', 'FW', 'EQ'] * 17,
        '상품코드': [f'PRD{i+1:03d}' for i in range(50)],
        '상품명': [f'상품_{i+1}' for i in range(50)],
        'CATE': ['신발', '운동화', '라이프스타일', '농구화', '캐주얼'] * 10,
        'GENDER': ['UNISEX', 'MEN', 'WOMEN'] * 17,
        '소비자': np.random.randint(50000, 300000, 50),
        '순매출할인율': np.random.randint(15, 60, 50),
        '순매출할인가': np.random.randint(35000, 180000, 50),
        '월간누적판매량': np.random.randint(5, 100, 50),
        '일별판매량': np.random.randint(1, 10, 50)
    }
    return pd.DataFrame(data)

# 메인 함수
def main():
    st.title("🏪 클리어런스 매장 관리 시스템")
    
    # 사이드바
    st.sidebar.title("메뉴")
    menu = st.sidebar.selectbox("선택하세요", [
        "📈 대시보드",
        "🏪 매장별 실적", 
        "📊 분석",
        "🧮 계산기"
    ])
    
    # 데이터 로드
    df = load_sample_data()
    st.sidebar.success(f"✅ 데이터 로드 완료 ({len(df)}개 상품)")
    
    # 메뉴별 페이지
    if menu == "📈 대시보드":
        show_dashboard(df)
    elif menu == "🏪 매장별 실적":
        show_store_performance(df)
    elif menu == "📊 분석":
        show_analytics(df)
    elif menu == "🧮 계산기":
        show_calculator()

def show_dashboard(df):
    st.header("📈 종합 대시보드")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 상품 수", len(df))
    with col2:
        total_revenue = (df['순매출할인가'] * df['월간누적판매량']).sum()
        st.metric("총 매출액", f"₩{total_revenue:,.0f}")
    with col3:
        avg_discount = df['순매출할인율'].mean()
        st.metric("평균 할인율", f"{avg_discount:.1f}%")
    with col4:
        total_sales = df['월간누적판매량'].sum()
        st.metric("총 판매량", f"{total_sales:,}")
    
    # 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # 매장별 매출
        store_revenue = df.groupby('매장명').apply(
            lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
        ).reset_index()
        store_revenue.columns = ['매장명', '매출액']
        
        fig = px.bar(store_revenue, x='매장명', y='매출액', title="매장별 매출")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 카테고리별 분포
        category_dist = df['CATE'].value_counts()
        fig = px.pie(values=category_dist.values, names=category_dist.index, title="카테고리 분포")
        st.plotly_chart(fig, use_container_width=True)

def show_store_performance(df):
    st.header("🏪 매장별 실적")
    
    # 매장 선택
    selected_store = st.selectbox("매장 선택", df['매장명'].unique())
    store_df = df[df['매장명'] == selected_store]
    
    # 매장 지표
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("매장 상품 수", len(store_df))
    with col2:
        store_revenue = (store_df['순매출할인가'] * store_df['월간누적판매량']).sum()
        st.metric("매장 매출액", f"₩{store_revenue:,.0f}")
    with col3:
        store_avg_discount = store_df['순매출할인율'].mean()
        st.metric("평균 할인율", f"{store_avg_discount:.1f}%")
    
    # 매장 상품 목록
    st.subheader("상품 목록")
    display_cols = ['상품명', 'CATE', 'GENDER', '순매출할인율', '순매출할인가', '월간누적판매량']
    st.dataframe(store_df[display_cols], use_container_width=True)

def show_analytics(df):
    st.header("📊 분석")
    
    # 할인율 vs 판매량
    fig = px.scatter(df, x='순매출할인율', y='월간누적판매량', 
                    color='CATE', title="할인율 vs 판매량")
    st.plotly_chart(fig, use_container_width=True)
    
    # BIZ별 성과
    biz_perf = df.groupby('Biz').agg({
        '월간누적판매량': 'sum',
        '순매출할인가': 'mean'
    }).reset_index()
    
    fig = px.bar(biz_perf, x='Biz', y='월간누적판매량', title="BIZ별 총 판매량")
    st.plotly_chart(fig, use_container_width=True)

def show_calculator():
    st.header("🧮 할인율 계산기")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("할인율 계산")
        original_price = st.number_input("원가", min_value=0, value=100000)
        sale_price = st.number_input("판매가", min_value=0, value=80000)
        
        if original_price > 0:
            discount_rate = ((original_price - sale_price) / original_price) * 100
            st.metric("할인율", f"{discount_rate:.1f}%")
    
    with col2:
        st.subheader("목표 할인율")
        target_discount = st.slider("목표 할인율 (%)", 0, 80, 20)
        
        if original_price > 0:
            target_price = original_price * (1 - target_discount/100)
            st.metric("목표 판매가", f"₩{target_price:,.0f}")

if __name__ == "__main__":
    main()
