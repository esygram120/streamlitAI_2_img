# Streamlit + Google Gemini LLM

import streamlit as st
import google.generativeai as genai
from PIL import Image
import numpy as np

with st.sidebar:
    # session_state 초기화
    if "image" not in st.session_state:
        st.session_state.image = None
    
    "[홈으로 돌아가기](http://localhost:8080/)"
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    # 이미지 파일 업로드
    img_file_buffer = st.file_uploader("이미지 파일 업로드", type=["png", "jpg", "jpeg"])

    # 이미지 파일 읽어오기
    if img_file_buffer != None:
        image = Image.open(img_file_buffer)
        img_array = np.array(image)
    
        st.session_state.image = image

st.title("🚀 이미지 파일처리 서비스 💬")
st.caption("Streamlit + Google Gemini LLM 을 연동했습니다.")
st.caption("이미지 파일을 업로드한 후, 이미지에서 궁금한 점을 질문해주세요.")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 이미지 화면에 그리기
if st.session_state.image != None:
    st.image(
        image,
        caption=f"You amazing image has shape {img_array.shape[0:2]}",
        use_column_width=True,
    )

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"][-1])

if prompt := st.chat_input():
    if not gemini_api_key:
        st.info("Google Gemini API 키를 입력하고 서비스를 이용해주세요.")
        st.stop()

    genai.configure(api_key=gemini_api_key)
    # gemini-pro-vision 모델 설정
    model = genai.GenerativeModel('gemini-pro-vision')

    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    st.chat_message("user").write(prompt)

    # prompt와 함께 이미지를 같이 모델에 전달
    response = model.generate_content([prompt, image])
    msg = response.text
    
    st.session_state.messages.append({"role": "model", "parts": [msg]})
    st.chat_message("model").write(msg)