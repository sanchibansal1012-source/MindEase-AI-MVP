import streamlit as st
from openai import OpenAI
import datetime

# 🌿 Initialize OpenAI client
client = OpenAI(api_key="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")   #  ← paste your key here

# 🌸 Page setup
st.set_page_config(page_title="MindEase", page_icon="🌿", layout="centered")

# ----------- Sidebar Navigation -----------
page = st.sidebar.radio("🌼 Navigate", ["AI Companion", "Mood Tracker", "Journal"])
st.sidebar.markdown("---")
st.sidebar.markdown("💚 *MindEase – a mental wellness space*")

# ----------- 1️⃣ AI Companion -----------
if page == "AI Companion":
    st.title("🌿 MindEase")
    st.subheader("Your AI-Powered Mental Health Companion 💖")

    st.markdown(
        "Welcome to **MindEase**, your safe space to share feelings and gain mindful support."
    )

    user_input = st.text_area("How are you feeling today?", height=120)

    if st.button("Reflect with MindEase"):
        if user_input.strip():
            with st.spinner("MindEase is listening with care... 🌸"):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a kind, empathetic mental-health coach who "
                                "offers comfort, perspective, and gentle self-care ideas."
                            ),
                        },
                        {"role": "user", "content": user_input},
                    ],
                    temperature=0.8,
                )
                ai_reply = response.choices[0].message.content
                st.markdown("### 💬 MindEase says:")
                st.write(ai_reply)
        else:
            st.warning("Please share a thought first 🌿")

# ----------- 2️⃣ Mood Tracker -----------
elif page == "Mood Tracker":
    st.title("📈 Mood Tracker")
    st.write("Log how you feel each day and see patterns over time.")

    mood = st.slider("How’s your mood today?", 0, 10, 5)
    note = st.text_input("One word or phrase describing your feeling:")

    if "mood_log" not in st.session_state:
        st.session_state["mood_log"] = []

    if st.button("Save Mood"):
        today = datetime.date.today().strftime("%d %b %Y")
        st.session_state["mood_log"].append({"date": today, "mood": mood, "note": note})
        st.success("Mood saved for today 🌼")

    if st.session_state["mood_log"]:
        st.write("### 🌸 Mood History")
        for entry in reversed(st.session_state["mood_log"]):
            st.write(f"**{entry['date']}** – Mood: {entry['mood']} /10 · *{entry['note']}*")

# ----------- 3️⃣ Journal -----------
elif page == "Journal":
    st.title("📓 Daily Journal")
    st.write("Reflect on your day and let MindEase help summarize or uplift you.")

    entry = st.text_area("Write your journal entry here...", height=200)

    if "journal_entries" not in st.session_state:
        st.session_state["journal_entries"] = []

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Entry"):
            if entry.strip():
                date = datetime.date.today().strftime("%d %b %Y")
                st.session_state["journal_entries"].append({"date": date, "entry": entry})
                st.success("Journal saved 🌿")
            else:
                st.warning("Write something first 🌸")

    with col2:
        if st.button("Ask AI for Reflection"):
            if entry.strip():
                with st.spinner("MindEase is reflecting with you..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a mindful coach. Summarize and respond to the "
                                    "user’s journal entry with kindness and perspective."
                                ),
                            },
                            {"role": "user", "content": entry},
                        ],
                    )
                    reflection = response.choices[0].message.content
                    st.markdown("### 💫 Reflection")
                    st.write(reflection)
            else:
                st.warning("Write something to reflect on 🌿")

    if st.session_state["journal_entries"]:
        st.markdown("---")
        st.write("### 🪶 Past Entries")
        for j in reversed(st.session_state["journal_entries"]):
            st.markdown(f"**{j['date']}**\n\n{j['entry']}")
