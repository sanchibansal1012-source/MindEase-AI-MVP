MindEase Full MVP App – Anonymous AI + Stranger Chat + Audio + Journaling

-------------------------------------------------------------------------

This is a COMPLETE copy‑paste Streamlit app (app.py) you can deploy on

Streamlit Cloud. No login. Anonymous users. Stranger chat with Firebase.

AI companion. Mood tracker. Journal. Clean UI.

------------------ IMPORTANT ----------------------

You MUST add these in Streamlit Cloud → Settings → Secrets:



OPENAI_API_KEY = "sk-..."

FIREBASE_DB_URL = "https://<your-project-id>-default-rtdb.firebaseio.com/"



----------------------------------------------------

import streamlit as st import requests import time import uuid from openai import OpenAI from streamlit_webrtc import webrtc_streamer, WebRtcMode import random import datetime

-----------------------------------------------------------------------------

Setup

-----------------------------------------------------------------------------

st.set_page_config(page_title="MindEase", page_icon="🌿", layout="wide") st.markdown( """ <style> body { background: #F8FAFD; } .main { background: #ffffff88; padding: 20px; border-radius: 14px; } </style> """, unsafe_allow_html=True, )

OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

Firebase

FIREBASE_DB_URL = st.secrets["FIREBASE_DB_URL"].rstrip("/")

Unique anonymous user id

if "uid" not in st.session_state: st.session_state.uid = str(uuid.uuid4())

Firebase helper

def fb_put(path, data): return requests.put(f"{FIREBASE_DB_URL}/{path}.json", json=data)

def fb_patch(path, data): return requests.patch(f"{FIREBASE_DB_URL}/{path}.json", json=data)

def fb_get(path): return requests.get(f"{FIREBASE_DB_URL}/{path}.json").json()

UI Sidebar

page = st.sidebar.radio("🌿 Navigation", ["AI Companion", "Stranger Chat", "Audio Call", "Mood Tracker", "Journal"])

-----------------------------------------------------------------------------

1. AI COMPANION

-----------------------------------------------------------------------------

if page == "AI Companion": st.title("💚 MindEase – Your AI Mental Wellness Companion") text = st.text_area("How are you feeling today?", height=150)

if st.button("Reflect 💬"):
    if text.strip():
        with st.spinner("MindEase is listening…"):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a warm, empathetic coach."},
                    {"role": "user", "content": text},
                ],
            )
            st.success("MindEase replied:")
            st.write(resp.choices[0].message.content)
    else:
        st.warning("Write something first.")

-----------------------------------------------------------------------------

2. STRANGER CHAT (Anonymous)

-----------------------------------------------------------------------------

if page == "Stranger Chat": st.title("🟣 Anonymous Stranger Chat") st.write("Connect anonymously with a random user.")

uid = st.session_state.uid

# Step 1: Try to match
if st.button("Find a Stranger 🔍"):
    fb_patch(f"queue/{uid}", {"uid": uid, "ts": time.time()})
    st.session_state.matching = True
    st.session_state.partner = None

# Poll queue
if st.session_state.get("matching"):
    st.write("Searching for a stranger…")
    time.sleep(1)
    queue = fb_get("queue")

    if queue:
        others = [k for k in queue.keys() if k != uid]
        if others:
            partner = random.choice(others)
            st.session_state.partner = partner
            fb_put(f"chats/{uid}_{partner}", {"messages": []})
            fb_patch(f"queue", {uid: None, partner: None})
            st.session_state.matching = False
            st.success("Connected! Scroll down.")

# Chat UI
partner = st.session_state.get("partner")
if partner:
    room = f"chats/{uid}_{partner}"
    st.subheader("Chat Room 🗨️")

    chat_data = fb_get(room)
    if chat_data and "messages" in chat_data:
        for msg in chat_data["messages"]:
            speaker = "You" if msg["uid"] == uid else "Stranger"
            st.write(f"**{speaker}:** {msg['text']}")

    new_msg = st.text_input("Type your message:")
    if st.button("Send"):
        chat = fb_get(room)
        if chat is None: chat = {"messages": []}
        chat["messages"].append({"uid": uid, "text": new_msg})
        fb_put(room, chat)

-----------------------------------------------------------------------------

3. AUDIO CALL

-----------------------------------------------------------------------------

if page == "Audio Call": st.title("🔊 Anonymous Audio Call") st.write("This uses WebRTC to allow microphone streaming.")

webrtc_streamer(
    key="audio-call",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    media_stream_constraints={"audio": True, "video": False},
)

-----------------------------------------------------------------------------

4. MOOD TRACKER

-----------------------------------------------------------------------------

if page == "Mood Tracker": st.title("📈 Mood Tracker")

mood = st.slider("How do you feel today?", 0, 10, 5)
note = st.text_input("One-word note:")

if "moods" not in st.session_state:
    st.session_state.moods = []

if st.button("Save Mood"):
    st.session_state.moods.append({
        "date": str(datetime.date.today()),
        "mood": mood,
        "note": note,
    })
    st.success("Saved!")

for m in reversed(st.session_state.moods):
    st.write(f"**{m['date']}** — Mood {m['mood']} / 10 — {m['note']}")

-----------------------------------------------------------------------------

5. JOURNAL

-----------------------------------------------------------------------------

if page == "Journal": st.title("📓 Daily Journal")

entry = st.text_area("Write your journal entry…", height=200)

if "journal" not in st.session_state:
    st.session_state.journal = []

col1, col2 = st.columns(2)
with col1:
    if st.button("Save Entry"):
        st.session_state.journal.append({
            "date": str(datetime.date.today()),
            "entry": entry,
        })
        st.success("Saved!")

with col2:
    if st.button("AI Reflection ✨"):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Reflect kindly on the user's journal."},
                {"role": "user", "content": entry},
            ],
        )
        st.write(resp.choices[0].message.content)

for j in reversed(st.session_state.journal):
    st.write(f"### {j['date']}")
    st.write(j["entry"])