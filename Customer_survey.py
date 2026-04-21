import streamlit as st
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Supplier Experience Survey",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
body { background-color: #F3F4F6; color: #111827; }
.stApp { background-color: #F3F4F6; }
h1,h2,h3 { color: #1F4E79; }
p, div, span, label { color: #111827; }
[data-testid="stMarkdownContainer"] p { color: #111827 !important; }
.stTextInput input { border: 2px solid #1F4E79 !important; color: #111827 !important; background: #FFFFFF !important; }
.stTextArea textarea { border: 2px solid #1F4E79 !important; border-radius: 6px !important; color: #111827 !important; }
.stSelectbox [data-baseweb="select"] { border: 2px solid #1F4E79 !important; }
.stButton button { background-color: #1F4E79 !important; color: #FFFFFF !important; font-weight: 700 !important; border: none !important; font-size: 1rem !important; }
.stButton button p { color: #FFFFFF !important; }
.stRadio label { color: #111827 !important; font-weight: 500 !important; }
.stSlider label { color: #111827 !important; font-weight: 600 !important; }
.category-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.category-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1F4E79;
    margin-bottom: 4px;
}
.category-desc {
    font-size: 0.85rem;
    color: #6B7280;
    margin-bottom: 12px;
}
.score-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #6B7280;
    margin-top: -8px;
    margin-bottom: 8px;
}
.header-block {
    background: #1F4E79;
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 24px;
    text-align: center;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SURVEY CATEGORIES ──────────────────────────────────────
SURVEY_CATEGORIES = {
    "1 - Quality": {
        "icon": "⭐",
        "desc": "Product quality, accuracy, and conformance to your requirements",
        "questions": [
            "Products or services delivered meet your quality requirements",
            "Issues and non-conformances are resolved promptly and effectively",
            "The supplier proactively communicates quality concerns",
        ]
    },
    "2 - Delivery": {
        "icon": "🚚",
        "desc": "On-time delivery, lead times, and order fulfillment accuracy",
        "questions": [
            "Orders are delivered on time as promised",
            "Lead times are reasonable and consistently met",
            "Delivery quantities and documentation are accurate",
        ]
    },
    "3 - Cost": {
        "icon": "💰",
        "desc": "Pricing, value for money, and cost transparency",
        "questions": [
            "Pricing is competitive and fair for the value provided",
            "Invoicing is accurate and easy to reconcile",
            "The supplier proactively looks for cost reduction opportunities",
        ]
    },
    "4 - Execution & Responsiveness": {
        "icon": "⚡",
        "desc": "Communication speed, issue resolution, and follow-through",
        "questions": [
            "The supplier responds to requests and inquiries promptly",
            "Commitments and deadlines are consistently met",
            "Issues are escalated and resolved without requiring follow-up",
        ]
    },
    "5 - Inventory": {
        "icon": "📦",
        "desc": "Stock availability, lead time flexibility, and shortage management",
        "questions": [
            "Product is consistently available when needed",
            "The supplier proactively communicates potential shortages",
            "Inventory programs (VMI, consignment) meet your operational needs",
        ]
    },
    "6 - Business Continuity": {
        "icon": "🔄",
        "desc": "Reliability, contingency planning, and supply chain resilience",
        "questions": [
            "You are confident in the supplier's ability to maintain supply during disruptions",
            "The supplier has demonstrated strong contingency planning",
            "The supplier's financial stability gives you confidence in long-term supply",
        ]
    },
    "7 - Innovation": {
        "icon": "💡",
        "desc": "New ideas, continuous improvement, and strategic partnership",
        "questions": [
            "The supplier brings new ideas and improvements to your attention",
            "The supplier invests in capabilities that benefit your business",
            "You see this supplier as a long-term strategic partner",
        ]
    },
}

SCORE_LABELS = {1: "Poor", 2: "Below Average", 3: "Average", 4: "Good", 5: "Excellent"}





RESPONSES_FILE = "survey_responses.json"

def load_all_responses():
    """Load responses from shared JSON file"""
    try:
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_response(supplier, customer_name, customer_company, scores, comments, overall_avg):
    """Save response to shared JSON file"""
    response = {
        "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "submitted_at": datetime.datetime.now().isoformat(),
        "supplier": supplier,
        "customer_name": customer_name,
        "customer_company": customer_company,
        "overall_avg": overall_avg,
        "scores": scores,
        "comments": comments
    }
    existing = load_all_responses()
    existing.append(response)
    try:
        with open(RESPONSES_FILE, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        st.error(f"Could not save response: {e}")
    return response


# ══════════════════════════════════════════════════════════
# MAIN SURVEY FORM
# ══════════════════════════════════════════════════════════
def main():

    # Header
    st.markdown("""
<div class="header-block">
    <h2 style="color:#FFFFFF; margin:0; font-size:1.6rem;">📋 Supplier Experience Survey</h2>
    <p style="color:#BFDBFE; margin:8px 0 0 0; font-size:0.95rem;">Help us understand your experience with our suppliers</p>
</div>
""", unsafe_allow_html=True)

    # Check if already submitted
    if st.session_state.get("survey_submitted", False):
        st.success("✅ Thank you! Your survey has been submitted successfully.")
        st.markdown("""
<div style="background:#FFFFFF; border-radius:10px; padding:24px; text-align:center; border:1px solid #E5E7EB;">
    <div style="font-size:3rem; margin-bottom:12px;">🙏</div>
    <h3 style="color:#1F4E79;">Thank you for your feedback!</h3>
    <p style="color:#6B7280;">Your response has been received and will help us improve supplier performance.</p>
    <p style="color:#6B7280; font-size:0.85rem;">You may close this window.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Submit Another Response"):
            # Clear all slider states so next respondent starts fresh
            keys_to_delete = [k for k in st.session_state.keys()
                               if k.startswith("score_") or k.startswith("comment_")
                               or k in ["cust_name", "cust_company", "supplier_name", "overall_comment"]]
            for k in keys_to_delete:
                del st.session_state[k]
            st.session_state.survey_submitted = False
            st.rerun()
        return

    # Contact info
    st.markdown("### Your Information")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Your Name *", placeholder="First and Last Name", key="cust_name")
    with col2:
        customer_company = st.text_input("Your Company *", placeholder="Company Name", key="cust_company")

    supplier = st.text_input("Supplier You Are Rating *",
                               placeholder="e.g. Sterigenics, STERIS, Grainger...",
                               key="supplier_name")

    st.markdown("---")
    st.markdown("### Rate Your Experience")
    st.markdown('<p style="color:#6B7280; font-size:0.85rem; margin-bottom:16px;">Rate each area from 1 (Poor) to 5 (Excellent). Use the comments box to share specific feedback.</p>', unsafe_allow_html=True)

    # Collect scores
    category_scores = {}
    category_comments = {}

    for cat_name, cat_data in SURVEY_CATEGORIES.items():
        st.markdown(f"""
<div class="category-card">
    <div class="category-title">{cat_data['icon']} {cat_name}</div>
    <div class="category-desc">{cat_data['desc']}</div>
</div>
""", unsafe_allow_html=True)

        q_scores = []
        for q_idx, question in enumerate(cat_data["questions"]):
            score = st.select_slider(
                question,
                options=["— Not Rated —", 1, 2, 3, 4, 5],
                value="— Not Rated —",
                format_func=lambda x: f"{x} — {SCORE_LABELS[x]}" if isinstance(x, int) else x,
                key=f"score_{cat_name}_{q_idx}"
            )
            if score != "— Not Rated —":
                q_scores.append(score)

        if q_scores:
            avg = sum(q_scores) / len(q_scores)
        else:
            avg = 0
        category_scores[cat_name] = {"scores": q_scores, "avg": avg, "rated": len(q_scores)}

        comment = st.text_area(
            f"Comments on {cat_name.split(' - ')[1] if ' - ' in cat_name else cat_name} (optional)",
            height=70,
            placeholder="Share any specific feedback, examples, or suggestions...",
            key=f"comment_{cat_name}"
        )
        category_comments[cat_name] = comment
        st.markdown("---")

    # Overall comments
    st.markdown("### Overall Feedback")
    overall_comment = st.text_area(
        "Any additional comments or suggestions?",
        height=100,
        placeholder="Overall impressions, areas for improvement, strengths...",
        key="overall_comment"
    )
    if overall_comment:
        category_comments["Overall"] = overall_comment

    # Submit
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Submit Survey", use_container_width=True, key="submit_btn"):
        # Check if any questions were actually rated
        total_rated = sum(len(v["scores"]) for v in category_scores.values())
        if not customer_name.strip():
            st.error("Please enter your name.")
        elif not customer_company.strip():
            st.error("Please enter your company name.")
        elif not supplier.strip():
            st.error("Please enter the supplier you are rating.")
        elif total_rated == 0:
            st.error("Please rate at least one question before submitting.")
        else:
            overall_avg = sum(v["avg"] for v in category_scores.values()) / len(category_scores)
            save_response(supplier, customer_name, customer_company,
                         category_scores, category_comments, overall_avg)
            st.session_state.survey_submitted = True
            st.rerun()

    st.markdown('<p style="text-align:center; color:#9CA3AF; font-size:0.78rem; margin-top:16px;">Your responses are confidential and will be used to improve supplier performance.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()