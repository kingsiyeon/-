import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 기본 설정 및 제목
st.set_page_config(page_title="오늘의 운세 챗봇 🔮", page_icon="🔮", layout="centered")
st.title("🔮 오늘의 운세 챗봇")
st.subheader("당신의 오늘 하루는 어떨까요? 무엇이든 물어보세요!")

# 2. Streamlit Secrets에서 API 키 확인 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 관리자 설정을 확인해 주세요.")
    st.stop()

@st.cache_resource
def init_genai_client():
    # 최신 google-genai SDK 공식 클라이언트 생성 방식
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    client = init_genai_client()
except Exception as e:
    st.error(f"⚠️ API 클라이언트 초기화 실패: {e}")
    st.stop()

# 3. 채팅 UI 표시용 기록 유지를 위한 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Gemini 멀티턴 대화(Chat) 세션 초기화 및 페르소나 주입
if "chat" not in st.session_state:
    system_prompt = (
        "당신은 친절하고 신비로우며 재치 있는 '오늘의 운세 전문가'입니다. "
        "사용자가 생년월일, 별자리, 띠, 혹은 특정 상황에 따른 오늘의 운세를 물어보면 정성껏 답변해 주세요. "
        "\n\n[답변 지침]\n"
        "1. 전반적으로 긍정적이고 희망찬 에너지를 전달하세요 (~랍니다, ~해보세요! 등의 부드러운 어조).\n"
        "2. 안 좋은 괘가 나오더라도 절망적인 예언 대신, '조심하면 좋은 점'과 '액막이 조언' 위주로 부드럽게 전달하세요.\n"
        "3. 행운의 컬러, 행운의 숫자, 혹은 오늘의 추천 음식을 함께 언급해 재미 요소를 더해주세요.\n"
        "4. 마지막에는 항상 '오늘 하루도 당신에게 행운이 가득하길 바랍니다! 🍀'와 같은 따뜻한 격려로 마무리하세요."
    )
    try:
        # SDK의 내장 대화(chats) 관리 도구를 사용하여 이전 대화 흐름을 자동 유지
        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.75
            )
        )
    except Exception as e:
        st.error(f"⚠️ 대화 세션 생성 실패: {e}")
        st.stop()

# 5. 기존 채팅 내역 화면에 렌더링
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 처리
if prompt := st.chat_input("예시: 95년생 돼지띠 오늘 운세 어때? / 오늘 면접이 있는데 행운의 컬러는?"):
    # 사용자 메시지 화면 출력 및 세션 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 응답 생성
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🌟 밤하늘의 별을 보며 운세를 읽어내는 중..."):
            try:
                # chat.send_message를 통해 대화 기록을 포함하여 API 요청
                response = st.session_state.chat.send_message(prompt)
                ai_text = response.text
                
                # 결과 반영 및 세션 저장
                response_placeholder.markdown(ai_text)
                st.session_state.messages.append({"role": "assistant", "content": ai_text})
                
            except Exception as e:
                # 상세 API 오류 및 네트워크 오류 예외 처리
                error_message = f"🔮 운세를 읽는 도중 신호가 흐려졌습니다. 잠시 후 다시 시도해 주세요.\n(에러 내용: {e})"
                response_placeholder.error(error_message)
