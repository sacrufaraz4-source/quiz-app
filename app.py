import streamlit as st
import random
import time
from questions import questions

TOTAL_TIME = 60

# ---------------- AUTO REFRESH (TIMER FIX) ----------------
st.experimental_set_query_params(t=time.time())

# ---------------- SESSION STATE ----------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.name = ""
    random.shuffle(questions)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.big-title {text-align:center; font-size:42px; font-weight:bold;}
.card {
    background: linear-gradient(135deg,#1f3b4d,#2e5b6e);
    padding:25px;
    border-radius:20px;
    color:white;
}
.stButton>button {
    width:100%;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="big-title">🧠 QUIZ APP ULTRA</div>', unsafe_allow_html=True)

# ---------------- NAME INPUT ----------------
if st.session_state.name == "":
    st.session_state.name = st.text_input("Enter your name:")

    if st.button("Start Quiz"):
        if st.session_state.name.strip() == "":
            st.warning("Enter name first")
        else:
            st.session_state.start_time = time.time()
            st.rerun()

    st.stop()

# ---------------- TIMER ----------------
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(TOTAL_TIME - elapsed, 0)

# auto refresh every second
st.empty()
time.sleep(1)
st.rerun()

st.progress(remaining / TOTAL_TIME)
st.write(f"⏱ Time left: {remaining}s")

if remaining == 0:
    st.error("⏰ Time's up!")
    st.session_state.q_index = len(questions)

# ---------------- QUIZ ----------------
if st.session_state.q_index < len(questions):

    q = questions[st.session_state.q_index]

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader(f"Question {st.session_state.q_index + 1} / {len(questions)}")
    st.write(q["question"])

    choice = st.radio(
        "Choose answer:",
        q["options"],
        key=f"q_{st.session_state.q_index}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Submit"):
            if choice == q["answer"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct: {q['answer']}")

            st.session_state.q_index += 1
            st.rerun()

    with col2:
        if st.button("⏭ Skip"):
            st.session_state.q_index += 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # progress
    st.progress(st.session_state.q_index / len(questions))

# ---------------- RESULT ----------------
else:
    st.balloons()

    st.success(
        f"🎉 {st.session_state.name}, Score: {st.session_state.score}/{len(questions)}"
    )

    if st.button("🔄 Restart"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.name = ""
        random.shuffle(questions)
        st.rerun()