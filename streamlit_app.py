import streamlit as st
from groq import Groq

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Forensics System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# LOAD API KEY SECURELY
# -----------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ GROQ_API_KEY not found. Please add it to .streamlit/secrets.toml")
    st.stop()

# -----------------------------
# TITLE
# -----------------------------
st.title("🔍 AI-Assisted Digital Forensics Investigation")
st.subheader("Case: Corporate Data Breach (Group 5)")

# -----------------------------
# FORENSIC DATA (CONTROLLED CONTEXT)
# -----------------------------
context = """
Corporate Data Breach Investigation:

Login Logs:
- 09:12 Login attempt from IP 185.23.45.12 (foreign - Russia)
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
- 09:15 account compromised
- 09:17 privilege escalation
- 09:30 file access
- 09:40 compression
- 10:05 data exfiltration

Conclusion:
External attacker used phishing to steal credentials and exfiltrate sensitive company data.
"""

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
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

# -----------------------------
# SESSION STATE FOR CHAT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY STATIC PANELS
# -----------------------------
if option == "Login Logs":
    st.markdown("### 🔐 Login Activity")
    st.code("""
[09:12] Login attempt from 185.23.45.12 (Russia)
[09:13] Failed login attempts (x5)
[09:15] Successful login - Lee Sungmin
[09:17] Privilege escalation detected
""")

elif option == "File Access Logs":
    st.markdown("### 📁 Sensitive File Access")
    st.code("""
HR_Salary.xlsx
Employee_Data.csv
Confidential_Report.pdf
[09:40] Files compressed → archive.zip
""")

elif option == "Network Logs":
    st.markdown("### 🌐 Network Activity")
    st.code("""
[10:05] Outbound transfer: 500MB
Destination: 185.23.45.12
Protocol: FTP
Status: Completed
""")

elif option == "Employee Interviews":
    st.markdown("### 👤 Interview Records")
    st.code("""
Lee Sungmin:
"I clicked a verification email and entered my password."

IT Admin:
"There was unusual outbound traffic that morning."

HR Manager:
"No suspicious activity noticed."
""")

elif option == "Attack Timeline":
    st.markdown("### ⏱️ Timeline Reconstruction")
    st.code("""
09:12 – Suspicious login attempt
09:15 – Account compromised
09:17 – Privilege escalation
09:30 – Sensitive files accessed
09:40 – Files compressed
10:05 – Data exfiltration
""")

elif option == "Final Analysis":
    st.markdown("### 🧠 Investigation Conclusion")
    st.success("""
Evidence indicates an EXTERNAL attacker.

- Phishing attack compromised employee credentials
- Unauthorized access gained
- Sensitive HR and company data extracted
- Data exfiltrated via FTP to external IP

Conclusion:
This breach was caused by a phishing attack targeting an internal employee.
""")

# -----------------------------
# AI CHAT ASSISTANT
# -----------------------------
elif option == "AI Chat Assistant":

    st.markdown("### 💬 AI Forensic Assistant")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    user_input = st.chat_input("Ask your investigation question...")

    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # AI response
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a digital forensics expert. Answer ONLY using the provided case data. Be clear, logical, and professional."
                    },
                    {
                        "role": "user",
                        "content": f"Case Data:\n{context}\n\nQuestion: {user_input}"
                    }
                ]
            )

            ai_reply = response.choices[0].message.content

        except Exception as e:
            ai_reply = f"⚠️ Error: {str(e)}"

        # Save AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        with st.chat_message("assistant"):
            st.markdown(ai_reply)
