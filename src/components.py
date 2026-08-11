import streamlit as st
import textwrap

def render_custom_css():
    """
    Injects custom CSS styling for high-contrast tab navigation and legible font rendering.
    """
    st.markdown("""
        <style>
        /* Base Page Background */
        .stApp {
            background-color: #f8fafc;
        }

        /* High-Contrast Streamlit Tabs Header */
        div[data-baseweb="tab-list"] {
            gap: 12px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 4px;
        }

        /* Unselected Tab Button */
        button[data-baseweb="tab"] {
            background-color: #edf2f7 !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px !important;
            margin: 0 !important;
        }

        /* Tab Text Color - Inactive */
        button[data-baseweb="tab"] p, 
        button[data-baseweb="tab"] div {
            color: #4a5568 !important;
            font-size: 1.05em !important;
            font-weight: 600 !important;
            opacity: 1 !important;
        }

        /* Active Tab Button */
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #1b3b18 !important;
        }

        /* Tab Text Color - Active */
        button[data-baseweb="tab"][aria-selected="true"] p, 
        button[data-baseweb="tab"][aria-selected="true"] div {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* Chat Messages Container */
        [data-testid="stChatMessage"] {
            color: #1a202c !important;
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }

        [data-testid="stChatMessage"] p, 
        [data-testid="stChatMessage"] li, 
        [data-testid="stChatMessage"] h1, 
        [data-testid="stChatMessage"] h2, 
        [data-testid="stChatMessage"] h3, 
        [data-testid="stChatMessage"] h4 {
            color: #1a202c !important;
        }

        [data-testid="stChatMessage"] h3, 
        [data-testid="stChatMessage"] h4 {
            color: #1b3b18 !important;
        }

        /* Plant Cards */
        .plant-card {
            background-color: #ffffff;
            border: 1px solid #cbd5e0;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            color: #2d3748 !important;
        }

        .safety-box {
            background-color: #fffaf0;
            border-left: 4px solid #dd6b20;
            padding: 10px 14px;
            border-radius: 4px;
            margin-top: 12px;
            font-size: 0.9em;
            color: #2d3748 !important;
        }

        .dosha-badge {
            background-color: #e2e8f0;
            color: #2d3748 !important;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 6px;
            font-weight: 600;
        }

        .use-tag {
            background-color: #edf2f7;
            color: #4a5568 !important;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.82em;
            margin-right: 4px;
            display: inline-block;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_plant_card(item: dict):
    """
    Renders an individual plant card with formatted tags and citations.
    """
    doshas_html = "".join([f'<span class="dosha-badge">{d}</span>' for d in item.get('dosha', [])])
    uses_html = "".join([f'<span class="use-tag">{use}</span>' for use in item.get('uses', [])])
    
    hist_html = ""
    if 'historical_note' in item and item['historical_note']:
        hist_html = f"""<p style="margin-top: 8px; margin-bottom: 4px; font-size: 0.9em; color: #2b6cb0;"><strong>📜 TKDL Prior Art Note:</strong> {item['historical_note']}</p>"""
    
    card_html = textwrap.dedent(f"""
<div class="plant-card">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<h3 style="margin: 0; color: #1b3b18; font-size: 1.25em;">{item['name']} <i style="font-size: 0.85em; color: #4a5568; font-weight: normal;">({item['sanskrit']})</i></h3>
<div>{doshas_html}</div>
</div>
<p style="color: #718096; font-style: italic; margin-top: 0; margin-bottom: 10px; font-size: 0.9em;">Botanical: {item['botanical']}</p>
<div style="margin-bottom: 10px;"><strong>Primary Uses:</strong><br/>{uses_html}</div>
<p style="margin-bottom: 4px; font-size: 0.92em;"><strong>Preparation:</strong> {item['preparation']}</p>
<p style="margin-bottom: 4px; font-size: 0.92em;"><strong>Classical Source:</strong> <code style="background-color: #edf2f7; padding: 2px 6px; border-radius: 4px; color: #1a202c;">{item['source_text']}</code></p>
{hist_html}
<div class="safety-box"><strong>⚠️ Safety & Caution:</strong> {item['safety_notes']}</div>
</div>
""").strip()

    st.markdown(card_html, unsafe_allow_html=True)