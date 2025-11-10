# app.py
import streamlit as st
from generator2 import generate_draft, export_to_word

st.set_page_config(page_title="LFTFIELD AI Agents", layout="wide")

# Updated Questions with better structure
BRAND_QUESTIONS = [
    {
        "id": "company_overview",
        "question": "What is the company name and what does it do?",
        "placeholder": "e.g., Markhor - A brand representing Pakistani military values, operating in the defense sector...",
        "help": "Provide company name, industry, and what the company does"
    },
    {
        "id": "brand_wheel",
        "question": "Complete the Brand Wheel (5 components):",
        "placeholder": """Attributes (3-5): Power, Discipline, Resilience...
Benefits (3-5): Enhanced national pride, quality assurance...
Values (3-5): Honor, Commitment, Excellence...
Personality (3-5): Authoritative, Inspirational, Bold...
Essence (1 phrase): "Strength in Unity" """,
        "help": "This framework helps define your brand identity comprehensively"
    },
    {
        "id": "target_personas",
        "question": "Describe 2-3 target audience personas in detail:",
        "placeholder": """Persona 1: The Veteran
- Demographics: Age 45-60, High School Diploma, Urban, $40K-$70K income
- Background: Retired military personnel
- Goals: Maintain connection with military life
- Challenges: Reintegrating into civilian life
- Motivations: Inspire younger generations

Persona 2: The Young Patriot
- Demographics: Age 18-30, Bachelor's degree, Urban/Suburban, $20K-$40K
- ...""",
        "help": "Include demographics, background, goals, challenges, and motivations"
    },
    {
        "id": "competitors",
        "question": "Who are 2-3 main competitors and what can you learn from them?",
        "placeholder": """Competitor 1: Pakistan Army Welfare Trust
- What they offer: Housing, healthcare, educational services
- Strengths: Government backing, extensive network
- Key learning: Community support enhances loyalty

Competitor 2: Armed Forces Foundation
- ...""",
        "help": "Analyze competitors to understand the competitive landscape"
    },
    {
        "id": "positioning",
        "question": "Complete your positioning statement:",
        "placeholder": "[Brand]'s [offering] is the only [category] that [unique benefit].\ne.g., Markhor's products are the only military-inspired goods that instill national pride while supporting local economy.",
        "help": "Use the formula: [Brand]'s [offering] is the only [category] that [benefit]"
    },
    {
        "id": "brand_story",
        "question": "Tell your brand story (2-3 paragraphs):",
        "placeholder": "What inspired your brand? What problem do you solve? What emotional connection should it create? Include customer pain points you address.",
        "help": "This should spark an emotional reaction and explain your purpose"
    },
    {
        "id": "brand_values",
        "question": "What are your 3-5 core brand values with descriptions?",
        "placeholder": """Honor: We uphold the highest standards of integrity...
Commitment: We are dedicated to serving our community...
Excellence: We strive for highest quality...""",
        "help": "Avoid clichés like 'honest' or 'transparent' - be specific and meaningful"
    },
    {
        "id": "brand_mission",
        "question": "What is your brand mission?",
        "placeholder": "Where is your brand heading? What do you aim to achieve? (2-3 sentences)",
        "help": "Describe your long-term vision and goals"
    },
    {
        "id": "touchpoints",
        "question": "List 5-8 brand touchpoints (where customers interact with you):",
        "placeholder": "Website, Social Media, Events, Retail Outlets, Customer Service, Mobile App, Packaging, Email...",
        "help": "All places where customers come in contact with your brand"
    },
    {
        "id": "brand_messaging",
        "question": "What are your 3-5 key brand messages?",
        "placeholder": """"Embrace the Spirit of the Military"
"Strength in Every Purchase"
"Support Local, Honor Tradition"
...""",
        "help": "These are core messages you'll communicate consistently"
    },
    {
        "id": "tone_of_voice",
        "question": "Define your Tone of Voice (3-5 characteristics with do's and don'ts):",
        "placeholder": """Authoritative - Speaks with confidence | Do: Use clear, strong language | Don't: Show uncertainty
Inspirational - Motivates audience | Do: Share success stories | Don't: Be overly critical
Respectful - Acknowledges sacrifices | Do: Show appreciation | Don't: Trivialize experiences
...""",
        "help": "How your brand should communicate with the audience"
    },
    {
        "id": "additional_context",
        "question": "Any additional context about your industry, market, or company? (Optional)",
        "placeholder": "Any other relevant information that would help create comprehensive brand guidelines...",
        "help": "Optional: Any extra details that might be helpful",
        "required": False
    }
]

DIGITAL_QUESTIONS = [
    {
        "id": "company_background",
        "question": "Provide company background and existing marketing challenges:",
        "placeholder": "Company overview, industry position, current challenges (e.g., low brand awareness, limited digital presence, lead generation issues)...",
        "section": "Introduction"
    },
    {
        "id": "products_services",
        "question": "List all products/services with brief descriptions:",
        "placeholder": """Product 1: Early Childhood Diploma - Comprehensive training for ages 2.5-6, target: aspiring teachers
Product 2: Toddler Assistants Course - 6-week intro course, target: career changers
...""",
        "section": "Introduction"
    },
    {
        "id": "marketing_goals",
        "question": "What are 3-5 SMART marketing goals?",
        "placeholder": """Goal 1: Increase website traffic by 50% in 6 months through SEO and content marketing
Goal 2: Generate 100 qualified leads per month by end of Q2 through landing pages
Goal 3: Boost social media engagement by 30% in 4 months through consistent posting
...""",
        "section": "Introduction",
        "help": "Specific, Measurable, Achievable, Relevant, Time-bound"
    },
    {
        "id": "swot",
        "question": "Complete SWOT Analysis:",
        "placeholder": """Strengths: Experienced leadership, MACTE accreditation, comprehensive curriculum, high-quality instruction...
Weaknesses: Limited digital presence, low brand awareness, new endeavor, no lead generation yet...
Opportunities: Growing Montessori education demand, digital marketing leverage, partnerships...
Threats: Strong competition, economic factors, changing educational trends, regulatory changes...""",
        "section": "SWOT Analysis",
        "help": "List 3-5 items for each category"
    },
    {
        "id": "competitive_analysis",
        "question": "Describe 2-3 main competitors and key learnings:",
        "placeholder": """Competitor 1: Canadian Montessori Teacher Education Institute
- Location: Mississauga, Ontario | MACTE accredited
- Offers: Early Childhood, Infant & Toddler, Elementary diplomas
- Strengths: Small class sizes, experienced faculty, flexible scheduling
- Learning: Personalized instruction attracts adult learners

Competitor 2: ...""",
        "section": "Market Analysis"
    },
    {
        "id": "target_customers",
        "question": "Describe 2-3 detailed customer personas:",
        "placeholder": """Persona 1: Aspiring Montessori Educator
- Demographics: 25-35, Bachelor's in ECE, Urban areas, limited budget
- Background: Recent grad, passionate about ECE, some teaching experience
- Goals: Get Montessori certification, enhance skills, secure position
- Challenges: Limited finances, balancing work/study, finding in-person training
- Motivations: Make impact on children, committed to Montessori philosophy

Persona 2: Career Changer
- Demographics: 35-45, Bachelor's in non-education field, suburban, has kids
- ...""",
        "section": "Market Analysis"
    },
    {
        "id": "buying_cycle",
        "question": "Describe the customer buying cycle:",
        "placeholder": """Awareness: Discover through social media, referrals, Google search - triggered by career change or child's birth
Consideration: Compare programs, read reviews, attend webinars (weeks to months)
Decision: Apply after researching accreditation and career outcomes
Post-Enrollment: Engage with content, join community, become advocates""",
        "section": "Market Analysis"
    },
    {
        "id": "usp",
        "question": "What is your Unique Selling Proposition?",
        "placeholder": "e.g., Only MACTE-accredited in-person Montessori training with 30+ years of expertise, focusing on pure Montessori philosophy",
        "section": "Brand Positioning"
    },
    {
        "id": "brand_relevance",
        "question": "How is your brand currently perceived vs. how you want it perceived?",
        "placeholder": """Current: Niche institution known for dedication to pure Montessori, experienced leadership, supportive environment
Desired: Premier Montessori training destination, innovative yet traditional, accessible, community-oriented, recognized leader""",
        "section": "Brand Positioning"
    },
    {
        "id": "website_status",
        "question": "Website status and needs:",
        "placeholder": "e.g., Basic site exists, needs SEO optimization, mobile improvements, better CTAs, lead capture forms",
        "section": "Current Status"
    },
    {
        "id": "social_media_status",
        "question": "Social media presence and needs:",
        "placeholder": "e.g., Active on Facebook & Instagram but inconsistent posting, need content calendar and engagement strategy",
        "section": "Current Status"
    },
    {
        "id": "email_status",
        "question": "Email marketing status and needs:",
        "placeholder": "e.g., Have 500 subscribers on Mailchimp, need segmentation, automation, and regular newsletters",
        "section": "Current Status"
    },
    {
        "id": "other_channels",
        "question": "SEO, blog, and other channel status:",
        "placeholder": "SEO: Not optimized, need keyword research | Blog: Have blog but irregular posts | Other: Plan to do webinars, no paid ads yet",
        "section": "Current Status"
    },
    {
        "id": "marketing_budget",
        "question": "What is the monthly/annual marketing budget?",
        "placeholder": "e.g., $5,000/month total, willing to allocate $2,000 for paid ads, rest for content creation and tools",
        "section": "Budget"
    },
    {
        "id": "friction_points",
        "question": "Any organizational, process, or resource challenges? (Optional)",
        "placeholder": "e.g., Small team (2 people), limited design resources, slow content approval process, outdated CRM system",
        "section": "Budget",
        "required": False
    },
    {
        "id": "additional_context",
        "question": "Any additional context or specific requirements? (Optional)",
        "placeholder": "Timeline expectations, upcoming launches, specific campaigns planned, industry regulations, etc.",
        "section": "Additional",
        "required": False
    }
]

QUESTIONS = {
    "brand": BRAND_QUESTIONS,
    "digital": DIGITAL_QUESTIONS
}

# App
st.title("🚀 LFTFIELD Marketing Agent Platform")
st.caption("Phase 1 MVP – Internal Draft Generator")

agent = st.selectbox("Select Agent", ["Brand Strategy & Guideline", "Digital Marketing Strategy"])

agent_key = "brand" if "Brand" in agent else "digital"
questions = QUESTIONS[agent_key]

# Session state
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "draft" not in st.session_state:
    st.session_state.draft = None

# Q&A Flow
st.subheader(f"{agent} – Answer Questions")

# Show question count
required_count = sum(1 for q in questions if q.get("required", True))
total_count = len(questions)
optional_count = total_count - required_count

st.info(f"📋 **{required_count} required questions** | {optional_count} optional questions | {total_count} total")

# Group questions by section for digital strategy
if agent_key == "digital":
    sections = {}
    for q in questions:
        section = q.get("section", "General")
        if section not in sections:
            sections[section] = []
        sections[section].append(q)
    
    # Display questions by section
    for section_name, section_questions in sections.items():
        with st.expander(f"📁 {section_name} ({len(section_questions)} questions)", expanded=True):
            for q in section_questions:
                is_required = q.get("required", True)
                label = f"{q['question']} {'*' if is_required else '(Optional)'}"
                
                default = st.session_state.answers.get(q["id"], "")
                ans = st.text_area(
                    label,
                    value=default,
                    key=q["id"],
                    height=150,
                    placeholder=q.get("placeholder", ""),
                    help=q.get("help", None)
                )
                st.session_state.answers[q["id"]] = ans
else:
    # Brand questions - simpler display
    for q in questions:
        is_required = q.get("required", True)
        label = f"{q['question']} {'*' if is_required else '(Optional)'}"
        
        default = st.session_state.answers.get(q["id"], "")
        ans = st.text_area(
            label,
            value=default,
            key=q["id"],
            height=150,
            placeholder=q.get("placeholder", ""),
            help=q.get("help", None)
        )
        st.session_state.answers[q["id"]] = ans

# Validate required fields
def validate_answers():
    missing = []
    for q in questions:
        if q.get("required", True):
            if q["id"] not in st.session_state.answers or not st.session_state.answers[q["id"]].strip():
                missing.append(q["question"])
    return missing

# Generate Button
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("✨ Generate Draft", type="primary", use_container_width=True):
        missing = validate_answers()
        if missing:
            st.error(f"⚠️ Please answer all required questions:\n\n" + "\n".join([f"• {q}" for q in missing]))
        else:
            with st.spinner("🤖 Generating draft using RAG + GPT-4o-mini..."):
                try:
                    draft = generate_draft(agent_key, st.session_state.answers)
                    st.session_state.draft = draft
                    st.success("✅ Draft generated successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error generating draft: {e}")
                    st.exception(e)

with col2:
    if st.button("🔄 Reset Form", use_container_width=True):
        st.session_state.answers = {}
        st.session_state.draft = None
        st.rerun()

# Show Draft
if st.session_state.draft:
    st.divider()
    st.subheader("📄 Generated Draft")
    
    # Preview tab and edit tab
    tab1, tab2 = st.tabs(["📖 Preview", "✏️ Edit"])
    
    with tab1:
        st.markdown(st.session_state.draft)
    
    with tab2:
        edited = st.text_area(
            "Edit Draft (Markdown)", 
            value=st.session_state.draft, 
            height=600,
            help="You can edit the markdown directly here. Changes will be reflected in the downloaded document."
        )
        
        if edited != st.session_state.draft:
            if st.button("💾 Save Edits"):
                st.session_state.draft = edited
                st.success("✅ Edits saved!")
    
    # Export section
    st.divider()
    st.subheader("📥 Export Document")
    
    # Get client name from first answer
    client_name = st.session_state.answers.get("company_overview", "Client")
    if "\n" in client_name:
        client_name = client_name.split("\n")[0]
    client_name = client_name[:50]  # Truncate if too long
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            word_buffer = export_to_word(st.session_state.draft, client_name)
            st.download_button(
                label="📄 Download as Word (.docx)",
                data=word_buffer,
                file_name=f"{client_name.replace(' ', '_')}_Strategy.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error creating Word document: {e}")
    
    with col2:
        st.download_button(
            label="📑 Download as PDF",
            data="PDF export coming in Phase 2",
            file_name="strategy.pdf",
            disabled=True,
            use_container_width=True
        )
    
    with col3:
        # Copy to clipboard (markdown)
        st.download_button(
            label="📋 Download Markdown",
            data=st.session_state.draft,
            file_name=f"{client_name.replace(' ', '_')}_Strategy.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Feedback section
    st.divider()
    st.subheader("💬 Feedback")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Excellent Draft", use_container_width=True):
            st.success("✅ Thank you! Feedback recorded.")
    with col2:
        if st.button("😐 Needs Improvement", use_container_width=True):
            st.warning("⚠️ Feedback recorded. We'll work on improving the output.")
    with col3:
        if st.button("👎 Poor Quality", use_container_width=True):
            st.error("❌ Feedback recorded. Please report specific issues to the team.")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **LFTFIELD Marketing Agent Platform**
    
    Phase 1 MVP for internal use by LFTFIELD team.
    
    **Features:**
    - Brand Strategy & Guideline Generator
    - Digital Marketing Strategy Generator
    - RAG-powered with template examples
    - Export to Word format
    
    **How to use:**
    1. Select an agent type
    2. Answer all required questions (*)
    3. Click "Generate Draft"
    4. Review, edit if needed
    5. Download as Word document
    
    **Tips:**
    - Provide detailed answers for better results
    - Use the placeholders as examples
    - Optional questions can improve quality
    - You can edit the markdown before exporting
    """)
    
    st.divider()
    
    st.header("📊 Stats")
    if agent_key == "brand":
        st.metric("Questions", f"{len(BRAND_QUESTIONS)} total")
        st.metric("Required", f"{sum(1 for q in BRAND_QUESTIONS if q.get('required', True))}")
    else:
        st.metric("Questions", f"{len(DIGITAL_QUESTIONS)} total")
        st.metric("Required", f"{sum(1 for q in DIGITAL_QUESTIONS if q.get('required', True))}")
    
    if st.session_state.answers:
        answered = sum(1 for v in st.session_state.answers.values() if v.strip())
        st.metric("Answered", f"{answered}/{len(questions)}")
    
    st.divider()
    
    st.caption("Built by LFTFIELD Inc. © 2025")