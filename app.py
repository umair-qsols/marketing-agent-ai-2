# app.py
import streamlit as st
from generator import generate_draft, export_to_word

st.set_page_config(page_title="LFTFIELD AI Agents", layout="wide")

# Load questions
QUESTIONS = {
    "brand": [
        "What is the company name?",
        "Describe the company's mission and vision.",
        "Who is the primary target audience? (age, job, pain points)",
        "What are the core brand values? (3-5)",
        "What makes this brand unique? (USP)",
        "Describe the desired brand personality (e.g., bold, warm, innovative).",
        "Do you have existing brand assets? (logo, colors, fonts)",
        "Any competitor brands to differentiate from?"
    ],
    "digital": [
        "Client/Company Name:",
        "Provide a brief company background and current marketing challenges.",
        "List all products/services you want to promote.",
        "What are the top 3 marketing goals? (e.g., leads, enrollments, traffic)",
        "Who is the ideal customer? (segment into 1-2 personas)",
        "Describe the typical buying journey.",
        "Who are 2-3 main competitors?",
        "What is the monthly marketing budget range?",
        "Any existing channels (website, social, email)? Status?"
    ]
}

# App
st.title("🚀 LFTFIELD Marketing Agent Platform")
st.caption("Phase 1 MVP – Internal Draft Generator")

agent = st.selectbox("Select Agent", ["Brand Strategy & Guideline", "Digital Marketing Strategy"])

agent_key = "brand" if "Brand" in agent else "digital"
questions = QUESTIONS[agent_key]

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "draft" not in st.session_state:
    st.session_state.draft = None

# Q&A Flow
st.subheader(f"{agent} – Answer Questions")

cols = st.columns(1)
with cols[0]:
    for i, q in enumerate(questions):
        key = f"q_{i}"
        default = st.session_state.answers.get(key, "")
        ans = st.text_area(q, value=default, key=key, height=100)
        st.session_state.answers[key] = ans

# Generate Button
if st.button("Generate Draft", type="primary"):
    with st.spinner("Generating draft using RAG + GPT-4o..."):
        try:
            draft = generate_draft(agent_key, st.session_state.answers)
            st.session_state.draft = draft
            st.success("Draft generated!")
        except Exception as e:
            st.error(f"Error: {e}")

# Show Draft
if st.session_state.draft:
    st.subheader("Draft Document")
    
    edited = st.text_area("Edit Draft (Markdown)", 
                          value=st.session_state.draft, 
                          height=600)
    
    col1, col2 = st.columns(2)
    
    client_name = st.session_state.answers.get("q_0", "Client").split("\n")[0]
    
    with col1:
        word_buffer = export_to_word(edited, client_name)
        st.download_button(
            label="Download as Word (.docx)",
            data=word_buffer,
            file_name=f"{client_name.replace(' ', '_')}_Strategy.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    with col2:
        st.download_button(
            label="Download as PDF (coming soon)",
            data="PDF export in Phase 2",
            file_name="strategy.pdf",
            disabled=True
        )

    # Feedback
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Good Draft"):
            st.success("Feedback recorded.")
    with col2:
        if st.button("👎 Needs Work"):
            st.warning("Feedback recorded. Improve in next iteration.")