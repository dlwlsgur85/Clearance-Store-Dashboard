import streamlit as st

# 가장 기본적인 테스트
st.title("🏪 테스트 페이지")
st.write("안녕하세요!")

# 기본 메트릭
col1, col2 = st.columns(2)
with col1:
    st.metric("테스트 1", "100")
with col2:
    st.metric("테스트 2", "200")

st.success("✅ 앱이 정상 작동합니다!")

# 사이드바
st.sidebar.title("메뉴")
st.sidebar.write("테스트 메뉴")

# 버튼 테스트
if st.button("테스트 버튼"):
    st.balloons()
    st.write("버튼이 클릭되었습니다!")

st.write("---")
st.write("이 페이지가 보인다면 Streamlit은 정상 작동합니다.")
