import streamlit as st
import random
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="오늘의 운세",
    page_icon="🔮",
    layout="centered"
)

# 제목
st.title("🔮 오늘의 운세")
st.write("이름을 입력하고 오늘의 운세를 확인해보세요!")

# 이름 입력
name = st.text_input("이름 입력")

# 운세 리스트
fortunes = [
    "오늘은 좋은 일이 생길 가능성이 높습니다 😊",
    "새로운 기회를 만나게 될 수 있습니다 ✨",
    "행운이 가까이에 있습니다 🍀",
    "작은 실수가 있을 수 있으니 차분하게 행동하세요 😌",
    "주변 사람들과의 대화가 큰 도움이 됩니다 💬",
    "오늘은 휴식이 필요한 날입니다 ☕",
    "노력한 만큼 좋은 결과가 따라옵니다 🚀",
    "뜻밖의 즐거운 소식이 찾아올 수 있습니다 🎉"
]

# 버튼
if st.button("운세 보기"):
    if name.strip() == "":
        st.warning("이름을 입력해주세요!")
    else:
        # 날짜 기준으로 항상 같은 운세가 나오게 설정
        today = datetime.now().strftime("%Y-%m-%d")
        random.seed(name + today)

        fortune = random.choice(fortunes)

        st.success(f"{name}님의 오늘 운세")
        st.write(f"👉 {fortune}")
