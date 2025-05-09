import streamlit as st
from transformers import pipeline
import time

# Configure the page with retro gaming theme
st.set_page_config(
    page_title="ARDIAN ESG ANALYZER",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for retro gaming aesthetic - Black and White only
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono:wght@400;700&display=swap');
    
    /* Global styles */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Headers with pixel art style */
    h1, h2, h3 {
        font-family: 'VT323', monospace !important;
        color: #000000 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 8px solid #000000;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    h1 {
        font-size: 48px !important;
        text-align: center;
        border: 8px solid #000000;
        padding: 20px;
        box-shadow: 8px 8px 0px #000000;
        background-color: #FFFFFF;
        margin-bottom: 30px;
    }
    
    /* Retro buttons */
    .stButton > button {
        font-family: 'Space Mono', monospace !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
    }
    
    .stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #000000 !important;
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        font-family: 'Space Mono', monospace !important;
        border: 4px solid #000000 !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        padding: 10px !important;
    }
    
    /* Containers */
    .pixel-container {
        border: 4px solid #000000;
        padding: 20px;
        margin: 20px 0;
        background-color: #FFFFFF;
        box-shadow: 4px 4px 0px #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Load the custom CSS
load_css()

# Title
st.markdown("<h1>🕹️ ARDIAN ESG ANALYZER 🕹️</h1>", unsafe_allow_html=True)

# Introduction
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="pixel-container">
        <h3 style="text-align: center;">ARDIAN MISSION BRIEFING</h3>
        <p style="font-family: 'Space Mono', monospace; text-align: center;">
        Paste sustainability report text<br>
        Let AI analyze the content<br>
        Get instant insights<br>
        <br>
        PRESS START TO BEGIN!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Text input section
st.markdown("<h2>📄 INPUT REPORT TEXT</h2>", unsafe_allow_html=True)

report_text = st.text_area(
    "Paste your sustainability report text here:",
    height=300,
    placeholder="Copy and paste the text from your sustainability report...",
    key="report_input"
)

# Initialize the AI models
@st.cache_resource
def load_models():
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        return summarizer
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        # Fallback to a simple extraction
        return None

# Generate summary
def generate_summary(text, summarizer):
    if summarizer is None:
        # Simple fallback - return first few sentences
        sentences = text.split('.')[:5]
        return '. '.join(sentences) + '.'
    
    try:
        # Split text into chunks
        max_chunk = 1024
        chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
        summaries = []
        
        for chunk in chunks[:3]:  # Limit to first 3 chunks
            if len(chunk.strip()) > 100:
                summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summaries.append(summary[0]['summary_text'])
        
        return " ".join(summaries)
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

# Analysis section
if report_text:
    st.markdown("<h2>🔍 ANALYSIS CONSOLE</h2>", unsafe_allow_html=True)
    
    if st.button("🎮 START ANALYSIS", use_container_width=True):
        with st.spinner("PROCESSING... PLEASE WAIT"):
            # Load models
            summarizer = load_models()
            
            # Store input text
            st.session_state.input_text = report_text
            
            # Generate summary
            st.session_state.summary = generate_summary(report_text[:5000], summarizer)
            st.session_state.analysis_complete = True
    
    # Display results
    if st.session_state.analysis_complete:
        st.markdown("<h2>📊 ANALYSIS RESULTS</h2>", unsafe_allow_html=True)
        
        # Summary
        st.markdown("""
        <div class="pixel-container">
            <h3>EXECUTIVE SUMMARY</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area(
            "Summary",
            value=st.session_state.summary,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Key metrics (mock)
        st.markdown("<h3>🎯 KEY METRICS DETECTED</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="pixel-container">
                <h4>ENVIRONMENT</h4>
                <p>Analysis pending...</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Download option
        st.markdown("<h2>💾 EXPORT OPTIONS</h2>", unsafe_allow_html=True)
        
        st.download_button(
            label="📄 DOWNLOAD SUMMARY",
            data=st.session_state.summary,
            file_name="ardian_esg_summary.txt",
            mime="text/plain"
        )

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 4px solid #000000;">
    <p style="font-family: 'VT323', monospace; font-size: 24px;">
    🕹️ ARDIAN ESG ANALYZER v1.0 🕹️<br>
    <span style="font-size: 16px;">POWERED BY ARDIAN | BUILT WITH AI</span>
    </p>
</div>
""", unsafe_allow_html=True)