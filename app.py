import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import openai

# 환경 변수에서 Google Sheets API 인증 정보 가져오기
credentials_dict = {
    "type": st.secrets["gcp"]["type"],
    "project_id": st.secrets["gcp"]["project_id"],
    "private_key_id": st.secrets["gcp"]["private_key_id"],
    "private_key": st.secrets["gcp"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["gcp"]["client_email"],
    "client_id": st.secrets["gcp"]["client_id"],
    "auth_uri": st.secrets["gcp"]["auth_uri"],
    "token_uri": st.secrets["gcp"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp"]["client_x509_cert_url"],
}

# Google Sheets API 인증 설정
creds = Credentials.from_service_account_info(credentials_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Google Sheets 연결
SHEET_ID = "1jl8a3dCdOav4IJO_268EMjMxmiabyAENvjMcseM_u5I"
sheet = client.open_by_key(SHEET_ID).worksheet("UserProfile")

# Streamlit 앱 시작
st.title("📚 AI 학습 보조 시스템")
st.sidebar.title("메뉴")
menu = st.sidebar.radio("선택하세요", ["홈", "학습 목표 설정", "학습 대시보드", "실습 과제", "AI 챗봇"])

# 1️⃣ 학습 목표 설정
if menu == "학습 목표 설정":
    st.subheader("🎯 학습 목표 설정")
    name = st.text_input("이름을 입력하세요")
    ai_level = st.selectbox("현재 AI 지식 수준", ["초급", "중급", "고급"])
    goal = st.text_area("학습 목표를 작성하세요")
    
    if st.button("제출"):
        try:
            sheet.append_row([name, ai_level, goal])
            st.success("학습 목표가 저장되었습니다!")
        except Exception as e:
            st.error(f"⚠️ 데이터 저장 오류: {e}")

# 2️⃣ 학습 대시보드
elif menu == "학습 대시보드":
    st.subheader("📊 나의 학습 진행 현황")
    try:
        data = sheet.get_all_records()
        if data:
            for user in data:
                st.write(f"👤 {user['이름']} | 📖 AI 수준: {user['AI 수준']} | 🎯 목표: {user['목표']}")
        else:
            st.warning("등록된 학습자가 없습니다.")
    except Exception as e:
        st.error(f"⚠️ 데이터 불러오기 오류: {e}")

# 3️⃣ 실습 과제 및 AI 피드백
elif menu == "실습 과제":
    st.subheader("📝 실습 과제 제출 & AI 피드백")
    task = "이번 주 과제: 'AI를 활용한 마케팅 자동화 프롬프트 작성'"
    st.write(task)
    
    answer = st.text_area("프롬프트를 작성하세요")
    
    if st.button("AI 피드백 받기"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"프롬프트 평가: {answer}"}]
            )
            feedback = response["choices"][0]["message"]["content"]
            
            sheet.append_row(["과제 제출", answer, feedback])
            st.write(f"📝 AI 피드백: {feedback}")
        except Exception as e:
            st.error(f"⚠️ AI 피드백 오류: {e}")

# 4️⃣ AI 챗봇 (Q&A)
elif menu == "AI 챗봇":
    st.subheader("💬 AI 챗봇")
    query = st.text_input("질문을 입력하세요")
    
    if st.button("질문하기"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": query}]
            )
            answer = response["choices"][0]["message"]["content"]
            st.write(f"🤖 AI 응답: {answer}")
        except Exception as e:
            st.error(f"⚠️ AI 응답 오류: {e}")
