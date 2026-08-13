import streamlit as st

def load_custom_css():
    """
    Injects custom CSS to fix low-contrast/invisible text issues,
    enforces readable font colors across light/dark themes, and styles tabs.
    """
    st.markdown(
        """
        <style>
        /* Force explicit high-contrast font colors for all standard elements */
        html, body, [class*="css"], .stMarkdown, p, span, label {
            color: #1F2937 !important; /* Dark slate charcoal */
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        /* Main Header Title Styling */
        .main-title {
            color: #1B4D3E !important; /* Deep Forest Green */
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            line-height: 1.2 !important;
        }

        /* Subtitle / Description Styling */
        .subtitle-text {
            color: #4B5563 !important; /* Medium dark grey */
            font-size: 1.05rem !important;
            font-weight: 500 !important;
            margin-top: 6px !important;
            margin-bottom: 24px !important;
        }

        /* Streamlit Navigation Tabs Styling */
        button[data-baseweb="tab"] div p {
            color: #1B4D3E !important; /* Deep Green for unselected tabs */
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }

        /* Selected Active Tab Styling */
        button[data-baseweb="tab"][aria-selected="true"] div p {
            color: #059669 !important; /* Emerald Green highlight */
            font-weight: 700 !important;
        }

        /* Sidebar Text Contrast */
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label {
            color: #1F2937 !important;
        }

        /* Card container styling for search results & remedies */
        .info-card {
            background-color: #F8FAFC;
            border-left: 4px solid #1B4D3E;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* Disclaimer Banner */
        .disclaimer-box {
            background-color: #FEF3C7;
            border-left: 4px solid #D97706;
            padding: 12px 16px;
            border-radius: 6px;
            color: #92400E !important;
            font-size: 0.88rem;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .disclaimer-box p {
            color: #92400E !important;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    """
    Renders the primary header banner with the logo, title, and subtitle.
    """
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
    """
    Renders a standard medical safety disclaimer banner required for health applications.
    """
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>⚠️ Medical Disclaimer:</strong> Ayurveda Setu provides information for educational and holistic guidance purposes based on classical Ayurvedic principles. It is not a substitute for professional medical diagnosis, treatment, or advice. Always consult a qualified Vaidya or healthcare provider regarding serious medical conditions.
        </div>
        """,
        unsafe_allow_html=True
    )

def render_card(title, content, tag=None):
    """
    Helper component to render formatted info cards for search results or remedies.
    """
    tag_html = f"<span style='background:#E0E7FF; color:#3730A3; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:600; float:right;'>{tag}</span>" if tag else ""
    st.markdown(
        f"""
        <div class="info-card">
            {tag_html}
            <h4 style="color: #1B4D3E !important; margin-top:0; margin-bottom:8px;">{title}</h4>
            <p style="margin:0; font-size:0.95rem;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )