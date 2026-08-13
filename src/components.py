import streamlit as st

def load_custom_css():
    """
    Injects CSS to ensure maximum visibility, crisp text contrast, and styled cards.
    """
    st.markdown(
        """
        <style>
        /* Force background to clean white */
        .stApp {
            background-color: #FFFFFF !important;
        }

        /* Force crisp dark text for all body elements, headers, and labels */
        html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
            color: #111827 !important; /* Dark charcoal */
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        /* Sidebar Styling & Visibility Fix */
        section[data-testid="stSidebar"] {
            background-color: #F3F4F6 !important;
        }
        section[data-testid="stSidebar"] *, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label {
            color: #111827 !important;
            font-weight: 500 !important;
        }

        /* Main Header Title */
        .main-title {
            color: #1B4D3E !important; /* Deep Forest Green */
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            line-height: 1.2 !important;
        }

        /* Subtitle */
        .subtitle-text {
            color: #374151 !important; /* Charcoal Grey */
            font-size: 1.05rem !important;
            font-weight: 500 !important;
            margin-top: 6px !important;
            margin-bottom: 20px !important;
        }

        /* Streamlit Tab Buttons */
        button[data-baseweb="tab"] div p {
            color: #1B4D3E !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] div p {
            color: #059669 !important; /* Bright Emerald */
            font-weight: 700 !important;
        }

        /* Input Fields visibility */
        input, select, textarea {
            color: #111827 !important;
            background-color: #FFFFFF !important;
            border: 1px solid #D1D5DB !important;
        }

        /* Card Container Styling */
        .info-card {
            background-color: #F9FAFB !important;
            border: 1px solid #E5E7EB !important;
            border-left: 5px solid #1B4D3E !important;
            padding: 18px !important;
            border-radius: 8px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* Disclaimer Banner */
        .disclaimer-box {
            background-color: #FEF3C7 !important;
            border-left: 5px solid #D97706 !important;
            padding: 14px 18px !important;
            border-radius: 6px !important;
            margin-top: 20px !important;
            margin-bottom: 20px !important;
        }
        .disclaimer-box p, .disclaimer-box strong {
            color: #92400E !important;
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    col1, col2 = st.columns([0.07, 0.93])
    with col1:
        st.markdown("<h1 style='margin:0; padding:0; line-height:1;'>🌿</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<h1 class="main-title">Ayurveda Setu: Traditional Knowledge Digital Library</h1>', 
            unsafe_allow_html=True
        )
    st.markdown(
        '<p class="subtitle-text">Digitized classical medicinal knowledge grounded with responsible AI</p>', 
        unsafe_allow_html=True
    )

def render_disclaimer():
    st.markdown(
        """
        <div class="disclaimer-box">
            <p><strong>⚠️ Medical Disclaimer:</strong> Ayurveda Setu provides information for educational and holistic guidance purposes based on classical Ayurvedic principles. It is not a substitute for professional medical diagnosis, treatment, or advice. Always consult a qualified Vaidya or healthcare provider regarding serious medical conditions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_card(title, content, tag=None):
    tag_html = f"<span style='background:#E0E7FF; color:#3730A3; padding:3px 10px; border-radius:12px; font-size:0.8rem; font-weight:700; float:right;'>{tag}</span>" if tag else ""
    st.markdown(
        f"""
        <div class="info-card">
            {tag_html}
            <h3 style="color: #1B4D3E !important; margin-top:0; margin-bottom:10px; font-weight:700;">{title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )