report_content += f"""
        
        ## 📈 성과 분석
        
        | KPI | 점수 | 평가 |
        |-----|------|------|
        | 재고회전율 | {scores['재고회전율']}/100 | {'우수' if scores['재고회전율'] >= 70 else '보통' if scores['재고회전율'] >= 50 else '개선필요'} |
        | 할인효율성 | {scores['할인효율성']}/100 | {'우수' if scores['할인효율성'] >= 70 else '보통' if scores['할인효율성'] >= 50 else '개선필요'} |
        | 매출성과 | {scores['매출성과']}/100 | {'우수' if scores['매출성과'] >= 70 else '보통' if scores['매출성과'] >= 50 else '개선필요'} |
        | 재고리스크 | {scores['재고리스크']}/100 | {'양호' if scores['재고리스크'] >= 70 else '보통' if scores['재고리스크'] >= 50 else '위험'} |
        
        ## 💡 권장 액션
        """
        
        # 권장 액션 생성
        actions = []
        if scores['재고회전율'] < 60:
            actions.append("📦 재고회전율 개선: 할인율 조정 검토")
        if scores['할인효율성'] < 50:
            actions.append("💰 할인 전략 재수립: 타겟 할인율 최적화")
        if len(alerts) > 0:
            actions.append("⚠️ 긴급 알림 대응: 과다재고/판매부진 상품 처리")
        if not actions:
            actions.append("✅ 현재 성과 양호: 현 상태 유지")
        
        for i, action in enumerate(actions, 1):
            report_content += f"{i}. {action}\n"
        
        report_content += """
        
        ---
        
        *이 리포트는 클리어런스 매장 관리 시스템에서 자동 생성되었습니다.*
        """
        
        st.markdown(report_content)
    
    with col2:
        st.subheader("📤 이메일 발송 설정")
        
        # 이메일 설정
        recipient_email = st.text_input("받는 사람", "manager@company.com")
        cc_email = st.text_input("참조 (CC)", "")
        email_subject = st.text_input("제목", f"클리어런스 일일 리포트 - {datetime.now().strftime('%m/%d')}")
        
        # 리포트 옵션
        st.subheader("📋 포함 내용")
        include_charts = st.checkbox("차트 포함", value=True)
        include_alerts = st.checkbox("알림 포함", value=True)
        include_kpi = st.checkbox("KPI 점수 포함", value=True)
        include_store_detail = st.checkbox("매장별 상세", value=False)
        
        # 발송 주기 설정
        st.subheader("🕒 발송 설정")
        send_frequency = st.selectbox("발송 주기", ["수동", "매일", "주간", "월간"])
        send_time = st.time_input("발송 시간", value=datetime.now().time())
        
        # 발송 버튼
        if st.button("📧 이메일 발송", type="primary"):
            with st.spinner("이메일 전송 중..."):
                import time
                time.sleep(2)  # 발송 시뮬레이션
            st.success("✅ 이메일이 성공적으로 발송되었습니다!")
            st.balloons()
            
        if st.button("📥 리포트 다운로드"):
            # 리포트를 텍스트 파일로 다운로드
            st.download_button(
                label="📄 리포트 다운로드 (TXT)",
                data=report_content,
                file_name=f"클리어런스_리포트_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# 5. 스마트 분석
def show_smart_analysis(df):
    st.header("📥 스마트 분석 & 자동 다운로드")
    
    # 분석 실행 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 AI 스마트 분석 실행", type="primary", use_container_width=True):
            with st.spinner("🤖 AI가 데이터를 분석 중입니다..."):
                import time
                time.sleep(3)  # 분석 시뮬레이션
                
                # 분석 결과 생성
                df_analyzed = df.copy()
                
                # AI 점수 계산 (시뮬레이션)
                np.random.seed(42)
                df_analyzed['AI_종합점수'] = np.random.randint(45, 98, len(df))
                df_analyzed['재고위험도'] = np.random.choice(['낮음', '보통', '높음'], len(df), p=[0.4, 0.4, 0.2])
                df_analyzed['수익성등급'] = np.random.choice(['A', 'B', 'C', 'D'], len(df), p=[0.2, 0.3, 0.3, 0.2])
                
                # 추천 액션 생성
                def generate_action(row):
                    if row['AI_종합점수'] >= 80:
                        return "현상 유지"
                    elif row['순매출할인율'] < 30 and row['월간누적판매량'] < 20:
                        return "가격 인하 검토"
                    elif row['월간누적판매량'] == 0:
                        return "판매 중단 검토"
                    elif row['순매출할인율'] > 60:
                        return "추가 프로모션"
                    else:
                        return "모니터링 강화"
                
                df_analyzed['AI_추천액션'] = df_analyzed.apply(generate_action, axis=1)
                
                # 수익성 예측 (시뮬레이션)
                df_analyzed['예상수익성'] = df_analyzed['AI_종합점수'] * np.random.uniform(0.8, 1.2, len(df))
                
                st.success("✅ AI 분석 완료!")
                
                # 분석 결과 요약
                st.subheader("🎯 AI 분석 결과 요약")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_ai_score = df_analyzed['AI_종합점수'].mean()
                    st.metric("평균 AI 점수", f"{avg_ai_score:.1f}점")
                
                with col2:
                    high_risk = len(df_analyzed[df_analyzed['재고위험도'] == '높음'])
                    st.metric("고위험 상품", f"{high_risk}개")
                
                with col3:
                    action_needed = len(df_analyzed[df_analyzed['AI_추천액션'].isin(['가격 인하 검토', '추가 프로모션', '판매 중단 검토'])])
                    st.metric("즉시 액션 필요", f"{action_needed}개")
                
                with col4:
                    grade_a = len(df_analyzed[df_analyzed['수익성등급'] == 'A'])
                    st.metric("A등급 상품", f"{grade_a}개")
                
                # 시각화
                col1, col2 = st.columns(2)
                
                with col1:
                    # AI 점수 분포
                    fig = px.histogram(df_analyzed, x='AI_종합점수', nbins=20,
                                     title="AI 종합점수 분포",
                                     color_discrete_sequence=['#FF6B6B'])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # 위험도 분포
                    risk_dist = df_analyzed['재고위험도'].value_counts()
                    fig = px.pie(values=risk_dist.values, names=risk_dist.index,
                               title="재고 위험도 분포",
                               color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347'])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # 액션 분석
                st.subheader("📋 AI 추천 액션 분석")
                action_counts = df_analyzed['AI_추천액션'].value_counts()
                
                fig = px.bar(x=action_counts.index, y=action_counts.values,
                           title="추천 액션별 상품 수",
                           color=action_counts.values,
                           color_continuous_scale='viridis')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # 다운로드 가능한 분석 결과
                st.subheader("📥 AI 분석 결과 다운로드")
                
                download_cols = ['상품코드', '상품명', '매장명', 'CATE', 'GENDER',
                               '순매출할인율', '순매출할인가', '월간누적판매량', 
                               'AI_종합점수', '재고위험도', '수익성등급', 
                               'AI_추천액션', '예상수익성']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = df_analyzed[download_cols].to_csv(index=False)
                    st.download_button(
                        label="📄 CSV 분석 결과 다운로드",
                        data=csv_data,
                        file_name=f"AI_클리어런스_분석_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # 고위험 상품만 다운로드
                    high_risk_df = df_analyzed[df_analyzed['재고위험도'] == '높음']
                    if len(high_risk_df) > 0:
                        high_risk_csv = high_risk_df[download_cols].to_csv(index=False)
                        st.download_button(
                            label="⚠️ 고위험 상품만 다운로드",
                            data=high_risk_csv,
                            file_name=f"고위험_상품_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                # 상세 분석 테이블
                st.subheader("🔍 상세 AI 분석 결과")
                
                # 테이블 필터링
                col1, col2, col3 = st.columns(3)
                with col1:
                    risk_filter = st.selectbox("위험도 필터", ['전체'] + list(df_analyzed['재고위험도'].unique()))
                with col2:
                    grade_filter = st.selectbox("수익성등급 필터", ['전체'] + list(df_analyzed['수익성등급'].unique()))
                with col3:
                    action_filter = st.selectbox("추천액션 필터", ['전체'] + list(df_analyzed['AI_추천액션'].unique()))
                
                # 필터 적용
                filtered_df = df_analyzed.copy()
                if risk_filter != '전체':
                    filtered_df = filtered_df[filtered_df['재고위험도'] == risk_filter]
                if grade_filter != '전체':
                    filtered_df = filtered_df[filtered_df['수익성등급'] == grade_filter]
                if action_filter != '전체':
                    filtered_df = filtered_df[filtered_df['AI_추천액션'] == action_filter]
                
                st.dataframe(filtered_df[download_cols], use_container_width=True, height=400)
    
    # 분석 안내
    st.markdown("---")
    st.info("""
    ### 🤖 AI 스마트 분석 기능
    
    **포함된 분석:**
    - 🎯 AI 종합점수 (45-98점 자동 계산)
    - ⚠️ 재고위험도 (낮음/보통/높음 자동 분류)
    - 💰 수익성등급 (A/B/C/D 자동 등급화)
    - 📋 맞춤형 추천액션 (5가지 액션 플랜)
    - 📈 예상수익성 예측
    
    **다운로드 옵션:**
    - 📄 CSV 파일 (전체 분석 결과)
    - ⚠️ 고위험 상품 파일 (즉시 대응 필요)
    """)

# 6. KPI 점수
def show_kpi_scores(df):
    st.header("🎯 KPI 성과 점수판")
    
    # 점수 계산
    scores = calculate_clearance_score(df)
    
    # 종합 점수 대형 표시
    st.markdown("### 📊 종합 성과")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        score_class = get_score_class(scores['종합점수'])
        st.markdown(f"""
        <div class="kpi-score {score_class}">
            <h1>종합 점수</h1>
            <h1 style="font-size: 4rem; margin: 0;">{scores['종합점수']}</h1>
            <h2>/100점</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 개별 KPI 점수들
    st.markdown("### 📈 세부 KPI 점수")
    
    col1, col2, col3, col4 = st.columns(4)
    
    kpi_items = [
        ('재고회전율', scores['재고회전율'], '🔄'),
        ('할인효율성', scores['할인효율성'], '💰'),
        ('매출성과', scores['매출성과'], '📈'),
        ('재고리스크', scores['재고리스크'], '⚠️')
    ]
    
    cols = [col1, col2, col3, col4]
    
    for i, (name, score, icon) in enumerate(kpi_items):
        with cols[i]:
            score_class = get_score_class(score)
            st.markdown(f"""
            <div class="kpi-score {score_class}">
                <h3>{icon} {name}</h3>
                <h2 style="font-size: 2.5rem; margin: 0.5rem 0;">{score}</h2>
                <h4>/100</h4>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 레이더 차트
    st.subheader("🕸️ KPI 레이더 차트")
    
    categories = list(scores.keys())
    values = list(scores.values())
    
    # 레이더 차트 생성
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='현재 점수',
        line_color='rgb(255, 107, 107)',
        fillcolor='rgba(255, 107, 107, 0.2)'
    ))
    
    # 목표 점수 (80점) 추가
    target_values = [80] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill='toself',
        name='목표 점수 (80점)',
        line_color='rgb(78, 205, 196)',
        fillcolor='rgba(78, 205, 196, 0.1)',
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )),
        showlegend=True,
        title="KPI 성과 레이더 차트",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 점수별 등급 기준
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 점수 등급 기준")
        st.markdown("""
        | 점수 범위 | 등급 | 상태 |
        |-----------|------|------|
        | 80-100점 | 🟢 우수 | 목표 달성 |
        | 60-79점 | 🟡 양호 | 개선 여지 있음 |
        | 40-59점 | 🟠 보통 | 관심 필요 |
        | 0-39점 | 🔴 주의 | 즉시 개선 필요 |
        """)
    
    with col2:
        st.subheader("💡 개선 제안")
        
        suggestions = []
        
        if scores['재고회전율'] < 70:
            suggestions.append("🔄 **재고회전율 개선**: 느린 회전 상품의 할인율 조정 검토")
            
        if scores['할인효율성'] < 60:
            suggestions.append("💰 **할인 전략 최적화**: 카테고리별 차별화된 할인 정책 수립")
            
        if scores['매출성과'] < 50:
            suggestions.append("📈 **매출 성과 향상**: 고수익 상품 집중 마케팅 및 진열 개선")
            
        if scores['재고리스크'] < 40:
            suggestions.append("⚠️ **재고 리스크 관리**: 장기재고 상품 처리 방안 마련")
        
        if not suggestions:
            suggestions.append("✅ **현재 성과 우수**: 현재 전략 유지 및 모니터링 지속")
        
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")

# 7. 알림 센터
def show_alert_center(df):
    st.header("⚠️ 스마트 알림 센터")
    
    # 알림 생성
    alerts = detect_alerts(df)
    
    # 알림 요약
    col1, col2, col3, col4 = st.columns(4)
    
    danger_count = len([a for a in alerts if a['type'] == 'danger'])
    warning_count = len([a for a in alerts if a['type'] == 'warning'])
    success_count = len([a for a in alerts if a['type'] == 'success'])
    total_alerts = len(alerts)
    
    with col1:
        st.metric("🔴 긴급 알림", danger_count)
    with col2:
        st.metric("🟡 주의 알림", warning_count)
    with col3:
        st.metric("🟢 기회 알림", success_count)
    with col4:
        st.metric("📊 전체 알림", total_alerts)
    
    st.markdown("---")
    
    if not alerts:
        st.success("✅ 현재 긴급한 알림이 없습니다. 모든 시스템이 정상 운영 중입니다.")
        
        # 건전성 체크
        st.subheader("🏥 시스템 건전성 체크")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 재고 건전성
            old_stock = len(df[(datetime.now() - pd.to_datetime(df['최근입고일자'])).dt.days > 90])
            st.metric("90일 이상 재고", f"{old_stock}개")
            
        with col2:
            # 판매 건전성
            zero_sales = len(df[df['일별판매량'] == 0])
            st.metric("무판매 상품", f"{zero_sales}개")
            
        with col3:
            # 가격 건전성
            high_discount = len(df[df['순매출할인율'] > 70])
            st.metric("고할인 상품", f"{high_discount}개")
        
        return
    
    # 알림 표시
    for i, alert in enumerate(alerts):
        if alert['type'] == 'danger':
            st.markdown(f"""
            <div class="alert-danger">
                <h3>{alert['title']}</h3>
                <p><strong>{alert['message']}</strong></p>
                <p>📊 해당 상품 수: <strong>{alert['count']}개</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
        elif alert['type'] == 'warning':
            st.markdown(f"""
            <div class="alert-warning">
                <h3>{alert['title']}</h3>
                <p><strong>{alert['message']}</strong></p>
                <p>📊 해당 상품 수: <strong>{alert['count']}개</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
        elif alert['type'] == 'success':
            st.markdown(f"""
            <div class="alert-success">
                <h3>{alert['title']}</h3>
                <p><strong>{alert['message']}</strong></p>
                <p>📊 해당 상품 수: <strong>{alert['count']}개</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # 각 알림에 대한 상세 데이터 표시
        if st.expander(f"📋 {alert['title']} 상세 보기"):
            if alert['type'] == 'danger':  # 과다재고
                df_alert = df.copy()
                df_alert['재고일수'] = (datetime.now() - pd.to_datetime(df_alert['최근입고일자'])).dt.days
                alert_items = df_alert[df_alert['재고일수'] > 180].head(10)
                cols_to_show = ['상품코드', '상품명', '매장명', 'CATE', '재고일수', '월간누적판매량']
                
            elif alert['type'] == 'warning':  # 판매부진
                alert_items = df[df['일별판매량'] == 0].head(10)
                cols_to_show = ['상품코드', '상품명', '매장명', 'CATE', '일별판매량', '월간누적판매량']
                
            else:  # 고수익 기회
                df_alert = df.copy()
                alert_items = df_alert[(df_alert['순매출할인율'] < 30) & (df_alert['월간누적판매량'] > 50)].head(10)
                cols_to_show = ['상품코드', '상품명', '매장명', 'CATE', '순매출할인율', '월간누적판매량']
            
            if len(alert_items) > 0:
                st.dataframe(alert_items[cols_to_show], use_container_width=True)
                
                # 알림별 액션 버튼
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📧 이메일 알림", key=f"email_{i}"):
                        st.success("이메일 알림이 발송되었습니다!")
                
                with col2:
                    if st.button(f"📥 데이터 다운로드", key=f"download_{i}"):
                        csv = alert_items.to_csv(index=False)
                        st.download_button(
                            label="CSV 다운로드",
                            data=csv,
                            file_name=f"알림_{alert['title']}_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            key=f"csv_{i}"
                        )
                
                with col3:
                    if st.button(f"✅ 처리 완료", key=f"complete_{i}"):
                        st.info("해당 알림이 처리 완료로 표시되었습니다.")
        
        st.markdown("---")

# 8. 스마트 계산기
def show_calculator():
    st.header("🧮 스마트 계산기")
    
    # 계산기 유형 선택
    calc_type = st.selectbox("🔧 계산 유형 선택", [
        "할인율 계산기", "수익률 계산기", "마진 계산기", "재고회전율 계산기", "손익분기점 계산기"
    ])
    
    if calc_type == "할인율 계산기":
        st.subheader("💰 할인율 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 기본 할인 계산")
            original_price = st.number_input("원가 (원)", min_value=0, value=100000, step=1000)
            sale_price = st.number_input("판매가 (원)", min_value=0, value=80000, step=1000)
            
            if original_price > 0:
                discount_rate = ((original_price - sale_price) / original_price) * 100
                discount_amount = original_price - sale_price
                savings_rate = (discount_amount / original_price) * 100
                
                st.metric("할인율", f"{discount_rate:.1f}%")
                st.metric("할인 금액", f"₩{discount_amount:,.0f}")
                st.metric("절약률", f"{savings_rate:.1f}%")
        
        with col2:
            st.markdown("#### 🎯 목표 할인율 계산")
            target_discount = st.slider("목표 할인율 (%)", 0, 80, 20)
            
            if original_price > 0:
                target_price = original_price * (1 - target_discount/100)
                target_discount_amount = original_price - target_price
                
                st.metric("목표 판매가", f"₩{target_price:,.0f}")
                st.metric("할인 금액", f"₩{target_discount_amount:,.0f}")
                
                # 예상 수익 계산
                expected_sales = st.number_input("예상 판매량", min_value=1, value=10, step=1)
                total_revenue = target_price * expected_sales
                total_discount = target_discount_amount * expected_sales
                
                st.metric("예상 매출", f"₩{total_revenue:,.0f}")
                st.metric("총 할인액", f"₩{total_discount:,.0f}")
    
    elif calc_type == "수익률 계산기":
        st.subheader("📈 수익률 계산기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💵 수익률 계산")
            cost_price = st.number_input("원가 (원)", min_value=0, value=70000, step=1000)
            selling_price = st.number_input("판매가 (원)", min_value=0, value=100000, step=1000)
            
            if cost_price > 0:
                profit_margin = ((selling_price - cost_price) / cost_price) * 100
                profit_amount = selling_price - cost_price
                markup_rate = ((selling_price - cost_price) / selling_price) * 100
                
                st.metric("수익률 (ROI)", f"{profit_margin:.1f}%")
                st.metric("수익 금액", f"₩{profit_amount:,.0f}")
                st.metric("마크업률", f"{markup_rate:.1f}%")
        
        with col2:
            st.markdown("#### 🎯 목표 수익률 계산")
            target_margin = st.slider("목표 수익률 (%)", 0, 200, 30)
            
            if cost_price > 0:
                target_selling_price = cost_price * (1 + target_margin/100)
                target_profit = target_selling_price - cost_price
                
                st.metric("목표 판매가", f"₩{import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import base64
from io import BytesIO

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
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .alert-danger {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 5px solid #dc3545;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 5px solid #ffc107;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
    }
    .kpi-score {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        color: white;
    }
    .score-excellent { background: linear-gradient(45deg, #28a745, #20c997); }
    .score-good { background: linear-gradient(45deg, #17a2b8, #6f42c1); }
    .score-fair { background: linear-gradient(45deg, #ffc107, #fd7e14); }
    .score-poor { background: linear-gradient(45deg, #dc3545, #e83e8c); }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 함수
@st.cache_data
def load_sample_data():
    n_products = 200
    stores = ['나이키일산', '브이엠플라스연수', '모다아울렛대전', '강남플래그십', '부산센텀시티']
    biz_types = ['AP', 'FW', 'EQ']
    silhouettes = ['로우탑', '러닝', '클래식', '하이탑', '캐주얼', '농구화', '트레이닝']
    categories = ['신발', '운동화', '라이프스타일', '농구화', '캐주얼', '런닝화', '트레킹화']
    genders = ['UNISEX', 'MEN', 'WOMEN', 'KIDS']
    sizes = ['240', '245', '250', '255', '260', '265', '270', '275', '280', '285', '290']
    
    np.random.seed(42)  # 일관된 데이터를 위해
    
    data = {
        '매장명': [stores[i % len(stores)] for i in range(n_products)],
        'Biz': [biz_types[i % len(biz_types)] for i in range(n_products)],
        '상품코드': [f'PRD{str(i+1).zfill(4)}' for i in range(n_products)],
        '상품명': [f'상품_{i+1}_{silhouettes[i % len(silhouettes)]}' for i in range(n_products)],
        '실루엣': [silhouettes[i % len(silhouettes)] for i in range(n_products)],
        'CATE': [categories[i % len(categories)] for i in range(n_products)],
        'GENDER': [genders[i % len(genders)] for i in range(n_products)],
        '사이즈': [sizes[i % len(sizes)] for i in range(n_products)],
        '소비자': np.random.randint(40000, 350000, n_products),
        '지정할인율': np.random.randint(5, 70, n_products),
        '지정할인가': np.random.randint(25000, 250000, n_products),
        '순매출할인율': np.random.randint(10, 80, n_products),
        '순매출할인가': np.random.randint(20000, 200000, n_products),
        '월간누적판매량': np.random.randint(0, 150, n_products),
        '일별판매량': np.random.randint(0, 8, n_products),
        '최근3일판매량': np.random.randint(0, 25, n_products),
        '최근7일판매량': np.random.randint(0, 55, n_products),
        '최근14일판매량': np.random.randint(0, 110, n_products),
        '최근21일판매량': np.random.randint(0, 165, n_products),
        '최근입고일자': pd.date_range('2023-01-01', periods=n_products, freq='3D').strftime('%Y-%m-%d')
    }
    return pd.DataFrame(data)

# 점수 계산 함수들
def calculate_clearance_score(df):
    """클리어런스 종합 점수 계산"""
    scores = {}
    
    # 1. 재고회전율 점수 (30%)
    df_calc = df.copy()
    df_calc['재고회전율'] = df_calc['월간누적판매량'] / (df_calc['월간누적판매량'] + 10)
    inventory_score = min(100, (df_calc['재고회전율'].mean() * 150)).round(1)
    
    # 2. 할인효율성 점수 (25%)
    df_calc['할인효율성'] = (df_calc['순매출할인율'] * df_calc['월간누적판매량']) / 100
    discount_score = min(100, (df_calc['할인효율성'].mean() * 1.5)).round(1)
    
    # 3. 매출성과 점수 (25%)
    revenue_score = min(100, (df_calc['순매출할인가'].mean() / 2000)).round(1)
    
    # 4. 재고리스크 점수 (20%)
    df_calc['재고일수'] = (datetime.now() - pd.to_datetime(df_calc['최근입고일자'])).dt.days
    risk_score = max(0, 100 - (df_calc['재고일수'].mean() / 365 * 50)).round(1)
    
    # 종합 점수
    total_score = (inventory_score * 0.3 + discount_score * 0.25 + 
                   revenue_score * 0.25 + risk_score * 0.2).round(1)
    
    return {
        '종합점수': total_score,
        '재고회전율': inventory_score,
        '할인효율성': discount_score,
        '매출성과': revenue_score,
        '재고리스크': risk_score
    }

def detect_alerts(df):
    """자동 알림 감지"""
    alerts = []
    
    # 과다재고 감지
    df_calc = df.copy()
    df_calc['재고일수'] = (datetime.now() - pd.to_datetime(df_calc['최근입고일자'])).dt.days
    overstock = df_calc[df_calc['재고일수'] > 180]
    if len(overstock) > 0:
        alerts.append({
            'type': 'danger',
            'title': '⚠️ 과다재고 경고',
            'message': f'{len(overstock)}개 상품이 180일 이상 재고 상태입니다.',
            'count': len(overstock)
        })
    
    # 품절위험 감지
    low_stock = df_calc[df_calc['일별판매량'] == 0]
    if len(low_stock) > 0:
        alerts.append({
            'type': 'warning',
            'title': '📉 판매부진 경고',
            'message': f'{len(low_stock)}개 상품의 일일 판매량이 0입니다.',
            'count': len(low_stock)
        })
    
    # 고수익 기회
    high_opportunity = df_calc[(df_calc['순매출할인율'] < 30) & (df_calc['월간누적판매량'] > 50)]
    if len(high_opportunity) > 0:
        alerts.append({
            'type': 'success',
            'title': '💰 고수익 기회',
            'message': f'{len(high_opportunity)}개 상품에서 추가 할인 여지가 있습니다.',
            'count': len(high_opportunity)
        })
    
    return alerts

def get_score_class(score):
    """점수에 따른 CSS 클래스 반환"""
    if score >= 80:
        return 'score-excellent'
    elif score >= 60:
        return 'score-good'
    elif score >= 40:
        return 'score-fair'
    else:
        return 'score-poor'

# 메인 애플리케이션
def main():
    st.markdown('<h1 class="main-header">🏪 클리어런스 매장 관리 시스템</h1>', unsafe_allow_html=True)
    
    # 사이드바 메뉴
    st.sidebar.title("📊 메뉴")
    
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
    
    # 현재 데이터 정보
    st.sidebar.info(f"📊 현재 데이터: {len(df)}개 상품")
    
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
        st.metric("총 매출액", f"₩{total_revenue:,.0f}", delta=f"+{total_revenue//1000000}M")
    
    with col3:
        avg_discount = df['순매출할인율'].mean()
        st.metric("평균 할인율", f"{avg_discount:.1f}%", delta=f"{avg_discount-40:.1f}%p")
    
    with col4:
        total_sales = df['월간누적판매량'].sum()
        st.metric("총 판매량", f"{total_sales:,}", delta=f"+{total_sales//100}")
    
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
                     color='매출액', 
                     color_continuous_scale='viridis')
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 카테고리별 분포
        category_dist = df['CATE'].value_counts()
        fig2 = px.pie(values=category_dist.values, names=category_dist.index,
                     title="카테고리별 상품 분포",
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # BIZ별 성과
        biz_perf = df.groupby('Biz').agg({
            '월간누적판매량': 'sum',
            '순매출할인가': 'mean'
        }).reset_index()
        
        fig3 = px.bar(biz_perf, x='Biz', y='월간누적판매량',
                     title="BIZ별 총 판매량", 
                     color='Biz',
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        fig3.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # 할인율 분포
        fig4 = px.histogram(df, x='순매출할인율', nbins=15,
                           title="할인율 분포",
                           color_discrete_sequence=['#FFA07A'])
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

# 2. 매장별 실적
def show_store_performance(df):
    st.header("🏪 매장별 실적 모니터링")
    
    # 매장 선택
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_store = st.selectbox("🏪 매장 선택", df['매장명'].unique())
    with col2:
        st.metric("선택 매장 상품 수", len(df[df['매장명'] == selected_store]))
    
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
    
    st.markdown("---")
    
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
                        title=f"{selected_store} - 카테고리별 성과",
                        hover_data=['CATE'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 일별 판매 추이
        daily_cols = ['최근3일판매량', '최근7일판매량', '최근14일판매량', '최근21일판매량']
        daily_trend = store_df[daily_cols].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['3일', '7일', '14일', '21일'],
            y=daily_trend.values,
            mode='lines+markers',
            name='평균 판매량',
            line=dict(color='#FF6B6B', width=4),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title=f"{selected_store} - 기간별 판매 추이",
            height=400,
            yaxis_title="판매량"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 매장 상품 목록
    st.subheader("📋 매장 상품 현황")
    
    # 필터링 옵션
    col1, col2, col3 = st.columns(3)
    with col1:
        cate_filter = st.selectbox("카테고리 필터", ['전체'] + list(store_df['CATE'].unique()))
    with col2:
        gender_filter = st.selectbox("성별 필터", ['전체'] + list(store_df['GENDER'].unique()))
    with col3:
        min_sales = st.number_input("최소 판매량", min_value=0, value=0)
    
    # 필터 적용
    filtered_store_df = store_df.copy()
    if cate_filter != '전체':
        filtered_store_df = filtered_store_df[filtered_store_df['CATE'] == cate_filter]
    if gender_filter != '전체':
        filtered_store_df = filtered_store_df[filtered_store_df['GENDER'] == gender_filter]
    filtered_store_df = filtered_store_df[filtered_store_df['월간누적판매량'] >= min_sales]
    
    display_cols = ['상품코드', '상품명', 'CATE', 'GENDER', '순매출할인율', 
                   '순매출할인가', '월간누적판매량', '일별판매량']
    st.dataframe(filtered_store_df[display_cols], use_container_width=True, height=300)
    
    # 다운로드 버튼
    csv = filtered_store_df.to_csv(index=False)
    st.download_button(
        label=f"📥 {selected_store} 데이터 다운로드",
        data=csv,
        file_name=f"{selected_store}_상품목록_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# 3. 실적 분석
def show_analytics(df):
    st.header("📊 고급 분석 대시보드")
    
    # 분석 유형 선택
    analysis_type = st.selectbox("🔍 분석 유형 선택", [
        "매출 트렌드 분석", "할인 효과 분석", "재고 회전율 분석", "상품 성과 분석", "시장 세그먼트 분석"
    ])
    
    if analysis_type == "매출 트렌드 분석":
        col1, col2 = st.columns(2)
        
        with col1:
            # BIZ별 매출 비교
            biz_revenue = df.groupby('Biz').apply(
                lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
            ).reset_index()
            biz_revenue.columns = ['Biz', '매출액']
            
            fig = px.bar(biz_revenue, x='Biz', y='매출액',
                        title="BIZ별 매출 비교", 
                        color='매출액',
                        color_continuous_scale='plasma')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 성별 매출 분포
            gender_revenue = df.groupby('GENDER').apply(
                lambda x: (x['순매출할인가'] * x['월간누적판매량']).sum()
            ).reset_index()
            gender_revenue.columns = ['GENDER', '매출액']
            
            fig = px.pie(gender_revenue, values='매출액', names='GENDER',
                        title="성별 매출 분포",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "할인 효과 분석":
        # 할인율과 판매량 상관관계
        fig = px.scatter(df, x='순매출할인율', y='월간누적판매량',
                        color='CATE', size='순매출할인가',
                        title="할인율 vs 판매량 상관관계",
                        hover_data=['상품명', '매장명'])
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # 상관계수 계산
        correlation = df['순매출할인율'].corr(df['월간누적판매량'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("상관계수", f"{correlation:.3f}")
        with col2:
            if correlation > 0.3:
                st.success("강한 양의 상관관계")
            elif correlation > 0.1:
                st.info("약한 양의 상관관계")
            elif correlation > -0.1:
                st.warning("상관관계 없음")
            else:
                st.error("음의 상관관계")
        with col3:
            st.metric("분석 샘플", f"{len(df)}개")
        
        # 할인 구간별 성과
        df_copy = df.copy()
        df_copy['할인구간'] = pd.cut(df_copy['순매출할인율'], 
                                bins=[0, 20, 40, 60, 100], 
                                labels=['0-20%', '21-40%', '41-60%', '61%+'])
        discount_perf = df_copy.groupby('할인구간').agg({
            '월간누적판매량': 'mean',
            '순매출할인가': 'mean'
        }).reset_index()
        
        fig = px.bar(discount_perf, x='할인구간', y='월간누적판매량',
                    title="할인 구간별 평균 판매량",
                    color='월간누적판매량',
                    color_continuous_scale='reds')
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
        
        total_revenue = (df['순매출할인가'] * df['월간누적판매량']).sum()
        avg_discount = df['순매출할인율'].mean()
        
        report_content = f"""
        # 📊 클리어런스 매장 일일 리포트
        
        **생성 일시**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}
        
        ## 🎯 핵심 지표
        
        | 지표 | 값 | 상태 |
        |------|----|----|
        | **종합 점수** | {scores['종합점수']}/100점 | {'🟢 우수' if scores['종합점수'] >= 70 else '🟡 보통' if scores['종합점수'] >= 50 else '🔴 주의'} |
        | **총 상품 수** | {len(df):,}개 | - |
        | **총 매출액** | ₩{total_revenue:,.0f} | - |
        | **평균 할인율** | {avg_discount:.1f}% | - |
        
        ## 🏪 매장별 성과
        """
        
        # 매장별 요약
        for store in df['매장명'].unique():
            store_df = df[df['매장명'] == store]
            store_revenue = (store_df['순매출할인가'] * store_df['월간누적판매량']).sum()
            report_content += f"- **{store}**: ₩{store_revenue:,.0f} ({len(store_df)}개 상품)\n"
        
        report_content += f"""
        
        ## ⚠️ 주요 알림 ({len(alerts)}건)
        """
        
        for alert in alerts:
            status_icon = "🔴" if alert['type'] == 'danger' else "🟡" if alert['type'] == 'warning' else "🟢"
            report_content += f"- {status_icon} {alert['title']}: {alert['count']}개 상품\n"
        
        report_content += f"""
        
        ## 📈 성과 분석
        
        | K
