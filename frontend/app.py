import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Personal Finance Chatbot", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cards and styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
    }
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
    }
    .chat-message {
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        background: #f8f9fa;
        color: #1a237e;
    }
    .user-message {
        background: #e3f2fd;
        border-left-color: #1976d2;
        color: #1a237e;
    }
    .bot-message {
        background: #f1f8e9;
        border-left-color: #388e3c;
        color: #1a237e;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header"><h1>🤖 AI Personal Finance Chatbot</h1><p>Your intelligent financial advisor powered by advanced AI</p></div>', unsafe_allow_html=True)

# Sidebar for user settings
with st.sidebar:
    st.header("⚙️ Settings")
    user_type = st.selectbox("👤 I am a...", ["Student", "Professional"])
    
    st.header("🌐 Language")
    language_options = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi"]
    language = st.selectbox("Select your language", language_options)
    language_api = language.lower() if language != "English" else "english"
    
    

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "💰 Budget & Goals", "📊 AI Reports", "💾 Sessions"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💬 Financial Chat Assistant")
    st.markdown("Ask me anything about your finances, and I'll provide expert advice!")
    
    user_input = st.text_input("💭 Your financial question:", placeholder="e.g., How should I budget my salary?")

    if st.button("📤 Send Message", use_container_width=True) and user_input:
        with st.spinner("🤔 Thinking..."):
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": user_input, "user_type": user_type.lower(), "language": language_api}
            ).json()["response"]
            st.session_state["chat_history"].append(("You", user_input))
            st.session_state["chat_history"].append(("Bot", response))

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat history with cards
    if st.session_state["chat_history"]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💬 Conversation History")
        
        for sender, msg in st.session_state["chat_history"]:
            if sender == "You":
                st.markdown(f'<div class="chat-message user-message"><strong>👤 You:</strong> {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Assistant:</strong> {msg}</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_history"] = []
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💰 Financial Data Input")
    
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("💵 Monthly Income", min_value=0.0, help="Enter your total monthly income")
        goal = st.text_input("🎯 Financial Goal", placeholder="e.g., Emergency Fund, Car, House")
    
    with col2:
        expenses = st.number_input("💸 Monthly Expenses", min_value=0.0, help="Enter your total monthly expenses")
        goal_amount = st.number_input("💎 Goal Amount", min_value=0.0, help="Target amount for your goal")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Financial metrics display
    if income > 0 or expenses > 0:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Financial Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        with col1:
            st.markdown(f'<div class="metric-card"><h4>💵 Income</h4><h3>${income:,.2f}</h3></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card"><h4>💸 Expenses</h4><h3>${expenses:,.2f}</h3></div>', unsafe_allow_html=True)
        
        with col3:
            color_class = "success-card" if savings > 0 else "warning-card"
            st.markdown(f'<div class="{color_class}"><h4>💰 Net Savings</h4><h3>${savings:,.2f}</h3></div>', unsafe_allow_html=True)
        
        with col4:
            rate_color = "success-card" if savings_rate >= 20 else "info-card" if savings_rate >= 10 else "warning-card"
            st.markdown(f'<div class="{rate_color}"><h4>📈 Savings Rate</h4><h3>{savings_rate:.1f}%</h3></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔍 Financial Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Get Budget Summary", use_container_width=True):
            with st.spinner("Analyzing your budget..."):
                summary = requests.post(
                    "http://localhost:8000/budget-summary",
                    json={"income": income, "expenses": expenses}
                ).json()["summary"]
                st.markdown(f'<div class="success-card">{summary}</div>', unsafe_allow_html=True)

    with col2:
        if st.button("🎯 Calculate Goal Savings", use_container_width=True):
            with st.spinner("Calculating savings needed..."):
                result = requests.post(
                    "http://localhost:8000/goal-calculation",
                    json={"goal": goal, "goal_amount": goal_amount, "income": income, "expenses": expenses}
                ).json()["monthly_amount"]
                st.markdown(f'<div class="info-card">You need to save: <strong>${result:.2f} per month</strong> for your goal.</div>', unsafe_allow_html=True)

    with col3:
        if st.button("💡 Spending Insights", use_container_width=True):
            with st.spinner("Analyzing spending patterns..."):
                insights = requests.post(
                    "http://localhost:8000/spending-insights",
                    json={"income": income, "expenses": expenses}
                ).json()["insights"]
                st.markdown(f'<div class="warning-card">{insights}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🤖 AI-Powered Financial Reports")
    st.write("Generate comprehensive financial analysis using IBM Granite 3.0-1B AI")

    # Add information about report formats
    st.markdown("""
    <div class="info-card">
    <h4>📊 Report Options:</h4>
    <ul>
    <li><strong>📱 Online Report</strong>: View your analysis directly in the browser</li>
    <li><strong>📄 Word Report</strong>: Download a professionally formatted .docx document with:
        <ul>
        <li>Executive summary and financial snapshot</li>
        <li>Detailed AI analysis with recommendations</li>
        <li>Action plan checklist</li>
        <li>Professional formatting ready for sharing</li>
        </ul>
    </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for the report buttons
    col1, col2 = st.columns(2)

    with col1:
        generate_report = st.button("📊 View Report Online", use_container_width=True)

    with col2:
        download_report = st.button("📄 Download Word Report", use_container_width=True)

    # Handle online report generation
    if generate_report:
        if income > 0 or expenses > 0 or goal:
            chat_history_str = "\n".join([f"{sender}: {msg}" for sender, msg in st.session_state["chat_history"]])
            report_data = {
                "user_type": user_type.lower(),
                "income": income,
                "expenses": expenses,
                "goal": goal,
                "goal_amount": goal_amount,
                "chat_history": chat_history_str
            }
            
            with st.spinner("🧠 Generating comprehensive financial analysis..."):
                try:
                    resp = requests.post("http://localhost:8000/generate-comprehensive-report", json=report_data, timeout=120).json()
                    if resp.get("status") == "success":
                        st.markdown('<div class="success-card"><h4>📊 Comprehensive Financial Report Generated!</h4></div>', unsafe_allow_html=True)
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.text_area("📋 Report Content", resp["report"], height=400)
                        st.markdown(f'<div class="info-card">Generated by: <strong>{resp.get("model", "AI Assistant")}</strong></div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="warning-card">Report generation failed: {resp.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
                except requests.exceptions.ReadTimeout:
                    st.markdown('<div class="warning-card">⏱️ Report generation is taking longer than expected. Please try again - the system will use a faster analysis method.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="warning-card">Error connecting to AI report service: {e}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-card">Please provide some financial data (income, expenses, or goals) to generate a meaningful report.</div>', unsafe_allow_html=True)

    # Handle Word document download
    if download_report:
        if income > 0 or expenses > 0 or goal:
            chat_history_str = "\n".join([f"{sender}: {msg}" for sender, msg in st.session_state["chat_history"]])
            report_data = {
                "user_type": user_type.lower(),
                "income": income,
                "expenses": expenses,
                "goal": goal,
                "goal_amount": goal_amount,
                "chat_history": chat_history_str
            }
            
            with st.spinner("📝 Generating downloadable Word report..."):
                try:
                    # Make request to get Word document
                    response = requests.post(
                        "http://localhost:8000/generate-word-report", 
                        json=report_data, 
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        # Create download button
                        st.markdown('<div class="success-card"><h4>📄 Word Report Generated Successfully!</h4></div>', unsafe_allow_html=True)
                        st.download_button(
                            label="💾 Download Financial Report.docx",
                            data=response.content,
                            file_name=f"financial_report_{user_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                        st.markdown('<div class="info-card">✅ Your comprehensive financial report is ready for download!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-card">Failed to generate Word document. Please try again.</div>', unsafe_allow_html=True)
                        
                except requests.exceptions.ReadTimeout:
                    st.markdown('<div class="warning-card">⏱️ Document generation is taking longer than expected. Please try again.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="warning-card">Error generating Word document: {e}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-card">Please provide some financial data (income, expenses, or goals) to generate a meaningful report.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("💾 Session Management")
    st.write("Save and load your financial sessions for future reference")
    
    # Save session section
    st.subheader("💾 Save Current Session")
    
    if st.button("🔒 Save Current Session", use_container_width=True):
        chat_history_str = "\n".join([f"{sender}: {msg}" for sender, msg in st.session_state["chat_history"]])
        save_data = {
            "user_type": user_type.lower(),
            "chat_history": chat_history_str,
            "income": income,
            "expenses": expenses,
            "goal": goal,
            "goal_amount": goal_amount
        }
        
        with st.spinner("Saving session..."):
            try:
                resp = requests.post("http://localhost:8000/save-session", json=save_data).json()
                if "session_id" in resp:
                    st.markdown(f'<div class="success-card"><h4>✅ Session Saved Successfully!</h4><p>Session ID: <strong>{resp["session_id"]}</strong></p><p>Keep this ID to load your session later.</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-card">Error saving session: {resp.get("status", "Unknown error")}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-card">Error saving session: {e}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load session section
    st.subheader("📂 Load Saved Session")
    
    col1, col2 = st.columns(2)
    
    with col1:
        session_id_input = st.text_input("🔢 Enter Session ID to Load:")
        
        if st.button("📥 Load Session", use_container_width=True) and session_id_input:
            try:
                session_id = int(session_id_input)
                with st.spinner("Loading session..."):
                    resp = requests.get(f"http://localhost:8000/get-session/{session_id}").json()
                    if "session" in resp:
                        session = resp["session"]
                        st.markdown(f'''
                        <div class="success-card">
                        <h4>� Session Loaded Successfully!</h4>
                        <p><strong>User Type:</strong> {session['user_type']}</p>
                        <p><strong>Goal:</strong> {session['goal']}</p>
                        <p><strong>Goal Amount:</strong> ${session['goal_amount']:,.2f}</p>
                        <p><strong>Income:</strong> ${session['income']:,.2f}</p>
                        <p><strong>Expenses:</strong> ${session['expenses']:,.2f}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        with st.expander("💬 View Chat History"):
                            st.text_area("Chat History", session['chat_history'], height=200)
                    else:
                        st.markdown(f'<div class="warning-card">Session not found: {resp.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
            except ValueError:
                st.markdown('<div class="warning-card">Please enter a valid session ID (numbers only)</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-card">Error loading session: {e}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🧠 Analyze Saved Session", use_container_width=True) and session_id_input:
            try:
                session_id = int(session_id_input)
                with st.spinner("🧠 Generating AI analysis of your financial session..."):
                    resp = requests.post("http://localhost:8000/analyze-my-finances", json={"session_id": session_id}, timeout=120).json()
                    if resp.get("status") == "success":
                        st.markdown('<div class="success-card"><h4>🧠 AI Financial Analysis Complete!</h4></div>', unsafe_allow_html=True)
                        st.text_area("🔍 Financial Analysis", resp["analysis"], height=400)
                        st.markdown(f'<div class="info-card">Analysis by: <strong>{resp.get("model", "AI Assistant")}</strong></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="warning-card">Analysis failed: {resp.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
            except ValueError:
                st.markdown('<div class="warning-card">Please enter a valid session ID</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-card">Error during analysis: {e}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 <strong>AI Personal Finance Chatbot</strong></p>
    <p>Powered by IBM Granite 3.0-1B & Groq API | Multilingual Support | Professional Reports</p>
    <p><em>This tool provides informational content only and should not be considered as professional financial advice.</em></p>
</div>
""", unsafe_allow_html=True)
