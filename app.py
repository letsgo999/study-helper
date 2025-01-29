import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import openai

# Google Sheets API 설정
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "google_sheets_credentials.json"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Google Sheets 연결 (스프레드시트 ID 변경 필요)
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"
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
        sheet.append_row([name, ai_level, goal])
        st.success("학습 목표가 저장되었습니다!")

# 2️⃣ 학습 대시보드
elif menu == "학습 대시보드":
    st.subheader("📊 나의 학습 진행 현황")
    data = sheet.get_all_records()
    
    if data:
        for user in data:
            st.write(f"👤 {user['이름']} | 📖 AI 수준: {user['AI 수준']} | 🎯 목표: {user['목표']}")
    else:
        st.warning("등록된 학습자가 없습니다.")

# 3️⃣ 실습 과제 및 AI 피드백
elif menu == "실습 과제":
    st.subheader("📝 실습 과제 제출 & AI 피드백")
    task = "이번 주 과제: 'AI를 활용한 마케팅 자동화 프롬프트 작성'"
    st.write(task)
    
    answer = st.text_area("프롬프트를 작성하세요")
    
    if st.button("AI 피드백 받기"):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"프롬프트 평가: {answer}"}]
        )
        feedback = response["choices"][0]["message"]["content"]
        
        sheet.append_row(["과제 제출", answer, feedback])
        
        st.write(f"📝 AI 피드백: {feedback}")

# 4️⃣ AI 챗봇 (Q&A)
elif menu == "AI 챗봇":
    st.subheader("💬 AI 챗봇")
    query = st.text_input("질문을 입력하세요")
    
    if st.button("질문하기"):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}]
        )
        answer = response["choices"][0]["message"]["content"]
        st.write(f"🤖 AI 응답: {answer}")
