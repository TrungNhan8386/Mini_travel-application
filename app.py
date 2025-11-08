# app.py
import os
import json
import hashlib
import datetime as dt
from pathlib import Path
import requests
import streamlit as st

# =========================
# Basic config
# =========================
st.set_page_config(page_title="Smart Itinerary (Streamlit + Ollama)", page_icon="🗺️", layout="centered")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

DEFAULT_MODEL = os.getenv("MODEL_NAME", "llama3.2:1b")
DEFAULT_OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # paste Pinggy/ngrok link here if remote

# =========================
# Utilities: users & chats
# =========================
def _hash_pw(pw: str) -> str:
    # Keep simple (SHA-256) to avoid bcrypt 72-byte limit issues
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def _load_users() -> dict:
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def _save_users(users: dict) -> None:
    USERS_FILE.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

def _user_chat_file(username: str) -> Path:
    return DATA_DIR / f"chats_{username}.json"

def load_chat(username: str) -> list:
    fp = _user_chat_file(username)
    if fp.exists():
        try:
            return json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_chat(username: str, messages: list) -> None:
    fp = _user_chat_file(username)
    fp.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")

# =========================
# Ollama client
# =========================
def health_check(base_url: str) -> tuple[bool, str]:
    try:
        # tags endpoint is light-weight; if 200 => healthy
        r = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=10)
        return (r.status_code == 200, f"HTTP {r.status_code}")
    except Exception as e:
        return (False, f"Error: {e}")

def generate_itinerary(base_url: str, model: str, prompt: str) -> str:
    """
    Calls Ollama /api/generate with {model, prompt, stream: false}.
    """
    url = f"{base_url.rstrip('/')}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # API returns {"response": "..."} or streams; we asked non-stream
    return data.get("response", "").strip()

# =========================
# Prompt builder
# =========================
def build_prompt(origin: str, destination: str, start_date: dt.date, end_date: dt.date,
                 interests: list[str], pace: str) -> str:
    days = (end_date - start_date).days + 1
    lines = []

    lines.append(
        f"Create a clean, well-formatted day-by-day itinerary from {origin} to {destination}.\n"
        f"Dates: {start_date.isoformat()} to {end_date.isoformat()} ({days} days)\n"
        f"Interests: {', '.join(interests) if interests else 'general'}\n"
        f"Pace: {pace}\n"
        "\nFORMAT RULES (IMPORTANT):\n"
        "- Output must be **very clearly structured**.\n"
        "- For each day, use exactly this layout:\n"
        "  Day X – YYYY-MM-DD\n"
        "  Morning:\n"
        "    • one sentence (< 25 words)\n"
        "  Afternoon:\n"
        "    • one sentence (< 25 words)\n"
        "  Evening:\n"
        "    • one sentence (< 25 words)\n"
        "- Make sure each section is on **its own line**.\n"
        "- Do NOT merge multiple periods into one paragraph.\n"
        "- Keep all descriptions concise, factual, and easy to scan.\n"
        "- After each sentence is a new line.\n"
        "- Sort sentence by date and time"
    )

    current = start_date
    for i in range(days):
        day_no = i + 1
        lines.append(
            f"\nDay {day_no} – {current.strftime('%Y-%m-%d')}\n"
            "Morning:\n"
            "Afternoon:\n"
            "Evening:"
        )
        current += dt.timedelta(days=1)

    return "\n".join(lines)


# =========================
# UI: Auth
# =========================
def auth_ui():
    st.subheader("Login")
    tab_login, tab_register = st.tabs(["Sign in", "Register"])

    with tab_login:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pw")
        if st.button("Sign in", type="primary"):
            users = _load_users()
            if u in users and users[u]["pw"] == _hash_pw(p):
                st.session_state["user"] = u
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab_register:
        u2 = st.text_input("New username", key="reg_user")
        p2 = st.text_input("New password", type="password", key="reg_pw")
        if st.button("Create account"):
            if not u2 or not p2:
                st.warning("Fill both fields.")
            else:
                users = _load_users()
                if u2 in users:
                    st.error("Username already exists.")
                else:
                    users[u2] = {"pw": _hash_pw(p2), "created": dt.datetime.now().isoformat()}
                    _save_users(users)
                    st.success("Account created. Please sign in.")

# =========================
# UI: Main app
# =========================
def app_ui(username: str):
    st.title("🗺️ Smart Itinerary (Streamlit + Ollama)")
    with st.expander("Server settings", expanded=False):
        st.write("Paste your Pinggy/ngrok base URL if running on Colab/Kaggle; else keep localhost.")
        base_url = st.text_input("OLLAMA_BASE_URL", value=DEFAULT_OLLAMA_BASE)
        model = st.text_input("MODEL_NAME", value=DEFAULT_MODEL)
        ok, msg = health_check(base_url)
        st.markdown(f"Health: **{'OK' if ok else 'DOWN'}** ({msg})")
        st.session_state["ollama_base"] = base_url
        st.session_state["ollama_model"] = model

    with st.form("form_inputs"):
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Origin city", placeholder="Ho Chi Minh City")
            start_date = st.date_input("Start date", value=dt.date.today())
            interests = st.multiselect(
                "Interests",
                ["food", "museums", "nature", "nightlife", "shopping", "history", "architecture", "family"],
                default=["food", "museums"]
            )
        with col2:
            destination = st.text_input("Destination city", placeholder="Da Nang")
            end_date = st.date_input("End date", value=dt.date.today() + dt.timedelta(days=1))
            pace = st.selectbox("Pace", ["relaxed", "normal", "tight"], index=1)

        submitted = st.form_submit_button("Generate itinerary", type="primary")

    # Initialize chat history
    if "chat" not in st.session_state:
        st.session_state.chat = load_chat(username)

    # History viewer
    with st.expander("Chat history", expanded=False):
        if st.session_state.chat:
            for i, item in enumerate(st.session_state.chat):
                st.markdown(f"**{item['role'].capitalize()}** — {item['time']}")
                st.code(item["content"])
                if i < len(st.session_state.chat) - 1:
                    st.divider()
        else:
            st.info("No history yet.")

    if submitted:
        if not origin or not destination:
            st.warning("Please fill origin and destination.")
            return
        if end_date < start_date:
            st.error("End date must be after or equal to start date.")
            return

        prompt = build_prompt(origin, destination, start_date, end_date, interests, pace)

        with st.spinner("Calling model..."):
            try:
                resp = generate_itinerary(
                    st.session_state["ollama_base"], st.session_state["ollama_model"], prompt
                )
            except Exception as e:
                st.error(f"Generation failed: {e}")
                return

        # Save conversation turn
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat.append({"role": "user", "time": now, "content": prompt})
        st.session_state.chat.append({"role": "assistant", "time": now, "content": resp})
        save_chat(username, st.session_state.chat)

        st.subheader("Itinerary")
        st.markdown(resp)

    st.divider()
    colx1, colx2, colx3 = st.columns(3)
    if colx1.button("Export history to JSON"):
        fp = DATA_DIR / f"export_chat_{username}.json"
        fp.write_text(json.dumps(st.session_state.chat, ensure_ascii=False, indent=2), encoding="utf-8")
        st.success(f"Saved: {fp}")
    if colx2.button("Clear history"):
        st.session_state.chat = []
        save_chat(username, [])
        st.toast("History cleared.")
    if colx3.button("Sign out"):
        st.session_state.pop("user", None)
        st.rerun()

# =========================
# Entry
# =========================
def main():
    # Persisted user session
    user = st.session_state.get("user")
    if not user:
        auth_ui()
    else:
        app_ui(user)

if __name__ == "__main__":
    main()
