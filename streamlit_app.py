import streamlit as st

st.set_page_config(page_title="AI Forensics System", layout="wide")

st.title("🔍 AI-Assisted Digital Forensics Investigation")
st.subheader("Case: Corporate Data Breach (Group 5)")

st.markdown("Ask questions like an investigator or use the buttons below.")

# -----------------------------
# Simulated Database
# -----------------------------
login_logs = """
[09:12] Login attempt from IP 185.23.45.12 (Unknown - Russia)
[09:13] Failed login (x5) - Lee Sungmin
[09:15] Successful login - Lee Sungmin
[09:17] Privilege escalation detected
"""

file_logs = """
Accessed: HR_Salary.xlsx
Accessed: Employee_Data.csv
Accessed: Confidential_Report.pdf
[09:40] Files compressed into archive.zip
"""

network_logs = """
[10:05] Large outbound transfer detected (500MB)
Destination IP: 185.23.45.12
Protocol: FTP
Status: Completed
"""

employee_interview = """
Lee Sungmin:
"I received an email asking me to verify my account.
I clicked the link and entered my password."

Kim Jisoo:
"No unusual activity noticed."

Park Minho:
"There was a spike in outbound traffic that morning."
"""

timeline = """
09:12 – Suspicious login attempt
09:15 – Account compromised (Lee Sungmin)
09:17 – Privilege escalation
09:30 – Sensitive files accessed
09:40 – Files compressed
10:05 – Data exfiltration (500MB)
"""

analysis = """
Evidence suggests an EXTERNAL ATTACKER.

- Login from foreign IP
- Phishing attack used
- Compromised employee credentials
- Data exfiltrated via FTP

Conclusion:
The breach was caused by a phishing attack targeting Lee Sungmin.
"""

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📂 Evidence Panel")

option = st.sidebar.radio(
    "Select Evidence:",
    [
        "Chat Query",
        "Login Logs",
        "File Access Logs",
        "Network Logs",
        "Employee Interviews",
        "Attack Timeline",
        "Final Analysis"
    ]
)

# -----------------------------
# Chat Simulation
# -----------------------------
if option == "Chat Query":
    user_input = st.text_input("Ask a question:")

    if user_input:
        query = user_input.lower()

        if "login" in query:
            st.code(login_logs)
        elif "file" in query:
            st.code(file_logs)
        elif "network" in query or "transfer" in query:
            st.code(network_logs)
        elif "employee" in query or "interview" in query:
            st.code(employee_interview)
        elif "timeline" in query:
            st.code(timeline)
        elif "who" in query or "attacker" in query:
            st.success(analysis)
        else:
            st.warning("No relevant data found. Try another query.")

# -----------------------------
# Direct Panels
# -----------------------------
elif option == "Login Logs":
    st.code(login_logs)

elif option == "File Access Logs":
    st.code(file_logs)

elif option == "Network Logs":
    st.code(network_logs)

elif option == "Employee Interviews":
    st.code(employee_interview)

elif option == "Attack Timeline":
    st.code(timeline)

elif option == "Final Analysis":
    st.success(analysis)
