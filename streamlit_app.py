import streamlit as st
from groq import Groq

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Forensics System",
    layout="wide"
)

# -----------------------------
# LOAD API KEY
# -----------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Missing GROQ_API_KEY in secrets.toml")
    st.stop()

# -----------------------------
# MODEL FALLBACK LIST
# -----------------------------
MODELS = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

# -----------------------------
# FORENSIC CONTEXT
# -----------------------------
context = """
Corporate Data Breach Investigation:

Login Logs:
- 09:12 Login attempt from IP 185.23.45.12 (Russia)
- Multiple failed attempts
- 09:15 Successful login (Lee Sungmin)
- Privilege escalation detected

File Access:
- HR_Salary.xlsx
- Employee_Data.csv
- Confidential_Report.pdf
- Files compressed into archive.zip

Network Activity:
- 10:05 Large outbound transfer (500MB)
- Destination IP: 185.23.45.12
- Protocol: FTP

Employee Interview:
- Lee Sungmin clicked phishing email and entered password
- IT admin observed unusual outbound traffic
- HR manager noticed nothing unusual

Timeline:
- 09:12 login attempt
- 09:15 compromise
- 09:17 privilege escalation
- 09:30 file access
- 09:40 compression
- 10:05 exfiltration

Conclusion:
External attacker used phishing to compromise credentials and steal data.
"""

# -----------------------------
# FALLBACK FUNCTION
# -----------------------------
def query_ai(user_input):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a digital forensics expert. Answer ONLY using provided evidence. Be clear and professional."
                    },
                    {
                        "role": "user",
                        "content": f"Case Data:\n{context}\n\nQuestion: {user_input}"
                    }
                ],
                temperature=0.3
            )

            return response.choices[0].message.content, model

        except Exception as e:
            continue

    return "⚠️ All AI models are currently unavailable. Based on evidence, this was a phishing-based external attack.", None

# -----------------------------
# UI
# -----------------------------
st.title("🔍 AI-Assisted Digital Forensics Investigation")
st.subheader("Corporate Data Breach (Group 5)")

# Sidebar
st.sidebar.title("📂 Evidence Panel")

option = st.sidebar.radio(
    "Select Section:",
    [
        "AI Chat Assistant",
        "Login Logs",
        "File Access Logs",
        "Network Logs",
        "Employee Interviews",
        "Attack Timeline",
        "Final Analysis"
    ]
)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# STATIC PANELS
# -----------------------------
if option == "Login Logs":
    st.code("""
[09:12] Login from 185.23.45.12 (Russia)
[09:13] Failed attempts (x5)
[09:15] Success - Lee Sungmin
[09:17] Privilege escalation
""")

elif option == "File Access Logs":
    st.code("""
HR_Salary.xlsx
Employee_Data.csv
Confidential_Report.pdf
[09:40] archive.zip created
""")

elif option == "Network Logs":
    st.code("""
[10:05] 500MB sent to 185.23.45.12 via FTP
""")

elif option == "Employee Interviews":
    st.code("""
Lee Sungmin: Clicked phishing email
IT Admin: Saw unusual traffic
HR: Nothing unusual
""")

elif option == "Attack Timeline":
    st.code("""
09:12 Login attempt
09:15 Compromise
09:17 Privilege escalation
09:30 File access
09:40 Compression
10:05 Exfiltration
""")

elif option == "Final Analysis":
    st.success("External phishing attack → credential theft → data exfiltration")

# -----------------------------
# AI CHAT
# -----------------------------
elif option == "AI Chat Assistant":

    st.markdown("### 💬 AI Forensic Assistant")

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your investigation question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing evidence..."):

                reply, model_used = query_ai(user_input)

                st.markdown(reply)

                if model_used:
                    st.caption(f"Model used: {model_used}")
                else:
                    st.caption("Fallback response (no model available)")

        st.session_state.messages.append({"role": "assistant", "content": reply})
