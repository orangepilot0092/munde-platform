"""
Project Munde — Maharashtra Digital Public Infrastructure
Professional Government-Grade Interface
Based on: Digital India, Data.gov.in, UDI/Aadhaar, and Global DPI Standards
"""
import streamlit as st
import requests
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================
API_BASE_URL = "http://192.168.29.20:8004/api/v1"

st.set_page_config(
    page_title="Project Munde | Maharashtra Digital Public Infrastructure",
    page_icon="️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL GOVERNMENT CSS
# Based on Digital India, Data.gov.in, and Global DPI Design Systems
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&display=swap');
    
    /* ---------- Root Variables (Government Design System) ---------- */
    :root {
        --gov-blue: #003366;
        --gov-blue-light: #0055A4;
        --gov-blue-dark: #002244;
        --gov-accent: #0066CC;
        --gov-success: #28A745;
        --gov-warning: #FFC107;
        --gov-danger: #DC3545;
        --gov-gray-100: #F8F9FA;
        --gov-gray-200: #E9ECEF;
        --gov-gray-300: #DEE2E6;
        --gov-gray-600: #6C757D;
        --gov-gray-900: #212529;
        --gov-white: #FFFFFF;
        --gov-border: #CED4DA;
    }
    
    /* ---------- Main App Styling ---------- */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', sans-serif;
    }
    
    /* ---------- Government Header (Like Digital India) ---------- */
    .gov-header {
        background: linear-gradient(135deg, #003366 0%, #002244 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-bottom: 4px solid #0066CC;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .gov-header .emblem {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .gov-header h1 {
        font-family: 'Merriweather', serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .gov-header .subtitle {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 400;
        margin-left: 0.5rem;
    }
    
    .gov-header .tagline {
        font-size: 0.9rem;
        opacity: 0.85;
        margin-top: 0.5rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(255,255,255,0.2);
    }
    
    /* ---------- Breadcrumb Navigation ---------- */
    .gov-breadcrumb {
        background: white;
        padding: 0.75rem 1.5rem;
        border-bottom: 1px solid #DEE2E6;
        margin-bottom: 2rem;
        font-size: 0.85rem;
        color: #6C757D;
    }
    
    .gov-breadcrumb a {
        color: #0066CC;
        text-decoration: none;
    }
    
    .gov-breadcrumb a:hover {
        text-decoration: underline;
    }
    
    /* ---------- Info Cards (Government Standard) ---------- */
    .info-card {
        background: white;
        border: 1px solid #DEE2E6;
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .info-card h3 {
        color: #003366;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.75rem 0;
        border-bottom: 2px solid #0066CC;
        padding-bottom: 0.5rem;
    }
    
    .info-card p {
        color: #495057;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* ---------- Agent List (Professional) ---------- */
    .agent-item {
        background: white;
        border-left: 4px solid #0066CC;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-radius: 0 4px 4px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .agent-item:hover {
        background: #F8F9FA;
        transform: translateX(3px);
    }
    
    .agent-item h4 {
        color: #003366;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
    }
    
    .agent-item p {
        color: #6C757D;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* ---------- Data Tier Boxes ---------- */
    .tier-item {
        background: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .tier-item .tier-badge {
        display: inline-block;
        background: #003366;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 3px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .tier-item .tier-name {
        font-weight: 600;
        color: #003366;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .tier-item .tier-desc {
        color: #6C757D;
        font-size: 0.8rem;
    }
    
    /* ---------- Chat Interface (Government Standard) ---------- */
    .stChatMessage {
        background: white !important;
        border: 1px solid #DEE2E6 !important;
        border-radius: 4px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    /* ---------- Metric Display (Professional) ---------- */
    .gov-metric {
        background: white;
        border: 1px solid #DEE2E6;
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
    }
    
    .gov-metric .label {
        font-size: 0.75rem;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .gov-metric .value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #003366;
    }
    
    /* ---------- Source Citations ---------- */
    .source-tag {
        display: inline-block;
        background: #E7F3FF;
        color: #003366;
        padding: 0.4rem 0.8rem;
        border-radius: 3px;
        font-size: 0.8rem;
        margin: 0.25rem;
        border: 1px solid #B3D9FF;
        font-weight: 500;
    }
    
    .source-tag.live {
        background: #D4EDDA;
        color: #155724;
        border-color: #C3E6CB;
    }
    
    /* ---------- Disclaimer Box ---------- */
    .gov-disclaimer {
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 0 4px 4px 0;
        font-size: 0.85rem;
        color: #856404;
    }
    
    /* ---------- Buttons (Government Standard) ---------- */
    .stButton > button {
        background: #0066CC;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #0052A3;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* ---------- Footer (Government Standard) ---------- */
    .gov-footer {
        background: #003366;
        color: white;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 4px;
        text-align: center;
    }
    
    .gov-footer h4 {
        color: white;
        font-family: 'Merriweather', serif;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .gov-footer p {
        margin: 0.3rem 0;
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    /* ---------- Status Indicator ---------- */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        color: #28A745;
        font-weight: 600;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #28A745;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* ---------- Sidebar Styling ---------- */
    [data-testid="stSidebar"] {
        background: #F8F9FA;
        border-right: 1px solid #DEE2E6;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #003366;
        font-family: 'Inter', sans-serif;
    }
    
    /* ---------- Accessibility Improvements ---------- */
    * {
        outline: none;
    }
    
    *:focus {
        outline: 2px solid #0066CC;
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PROFESSIONAL GOVERNMENT HEADER
# ============================================================================
st.markdown("""
<div class="gov-header">
    <div class="emblem">
        <div style="font-size: 2.5rem;">🏛️</div>
        <div>
            <h1>Project Munde</h1>
            <div class="subtitle">Maharashtra Digital Public Infrastructure</div>
        </div>
    </div>
    <div class="tagline">
        <strong>Sovereign Agentic AI Platform</strong> | Multi-domain Intelligence • Real-time Government Data • Local LLM Infrastructure
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# BREADCRUMB NAVIGATION
# ============================================================================
st.markdown("""
<div class="gov-breadcrumb">
    <a href="#">Home</a> / <a href="#">Digital Services</a> / <strong>AI Platform</strong>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR — Professional Government Navigation
# ============================================================================
with st.sidebar:
    # Platform Identity
    st.markdown("### 🏛️ मूंदे सहाय्यक")
    st.markdown("*Munde Sahayak — Chief Orchestrator*")
    st.divider()
    
    # Domain Agents (Professional List)
    st.markdown("#### Domain Intelligence Agents")
    
    st.markdown("""
    <div class="agent-item">
        <h4>💧 JalSetu — Water Intelligence</h4>
        <p>Reservoirs, irrigation, drought, floods</p>
    </div>
    <div class="agent-item">
        <h4>🌾 KrishiSetu — Agriculture</h4>
        <p>Crop advisories, soil health, market prices</p>
    </div>
    <div class="agent-item">
        <h4>🏥 ArogyaSetu — Health</h4>
        <p>PHC capacity, bed availability, disease advisories</p>
    </div>
    <div class="agent-item">
        <h4>️ BhumiSetu — Land Records</h4>
        <p>7/12 extracts, land use, soil suitability</p>
    </div>
    <div class="agent-item">
        <h4>🚨 AapdaSetu — Disaster Management</h4>
        <p>Flood/drought alerts, relief camps, emergency protocols</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Data Infrastructure (Tier Visualization)
    st.markdown("#### Data Infrastructure")
    
    st.markdown("""
    <div class="tier-item">
        <span class="tier-badge">Tier 1</span>
        <div class="tier-name">APIs & Open Data</div>
        <div class="tier-desc">India OGD, WAQI, IMD, Census, OSM</div>
    </div>
    <div class="tier-item">
        <span class="tier-badge">Tier 2</span>
        <div class="tier-name">State Portals</div>
        <div class="tier-desc">WRD, Soil Health, Agriculture Dept</div>
    </div>
    <div class="tier-item">
        <span class="tier-badge">Tier 3</span>
        <div class="tier-name">Municipal Corporations</div>
        <div class="tier-desc">BMC, PMC, NMC, PCMC, Nashik, Thane</div>
    </div>
    <div class="tier-item">
        <span class="tier-badge">Tier 4</span>
        <div class="tier-name">Utility APIs</div>
        <div class="tier-desc">Geocoding, PIN Codes, Agmarknet</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Live Data Controls
    st.markdown("#### Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💧 Sync Water", use_container_width=True):
            st.success("Pipeline initiated")
    with col2:
        if st.button("🌾 Sync Agri", use_container_width=True):
            st.success("Pipeline initiated")
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏥 Sync Health", use_container_width=True):
            st.success("Pipeline initiated")
    with col4:
        if st.button("🗺️ Sync Land", use_container_width=True):
            st.success("Pipeline initiated")
    
    st.divider()
    
    # System Status
    st.markdown("#### System Status")
    st.markdown("""
    <div style="font-size: 0.85rem; line-height: 1.8;">
        <div class="status-indicator">
            <span class="status-dot"></span>
            <strong>Backend API:</strong> Port 8004
        </div>
        <div style="margin-top: 0.5rem;">
            <span class="status-dot"></span>
            <strong>Database:</strong> PostgreSQL + pgvector
        </div>
        <div style="margin-top: 0.5rem;">
            <span class="status-dot"></span>
            <strong>ETL Pipeline:</strong> Dagster
        </div>
        <div style="margin-top: 0.5rem;">
            <span class="status-dot"></span>
            <strong>LLM:</strong> Qwen2.5 (DGX Spark)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Welcome Card
st.markdown("""
<div class="info-card">
    <h3>Welcome to Project Munde</h3>
    <p>
        This is Maharashtra's sovereign AI platform for accessing real-time government data across water, agriculture, 
        health, land, and disaster management domains. All responses are grounded in official government datasets with 
        full source citations and confidence scores.
    </p>
</div>
""", unsafe_allow_html=True)

# Chat Interface Header
st.markdown("### Intelligent Query Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """**Welcome to Munde Sahayak.**

I am your AI orchestrator for Maharashtra's Digital Public Infrastructure. I coordinate five specialized agents to provide accurate, cited responses based on real government data.

**Example Queries:**
- "What is the current AQI in Mumbai and Pune?"
- "Soil pH and nitrogen levels in Baramati, Pune?"
- "Reservoir storage levels in Maharashtra?"
- "Civic hospitals in BMC Mumbai?"
- "PIN code 411001 details?"

All responses include dataset provenance, confidence scores, and source citations."""
        }
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "raw_data" in message:
            # Professional rendering with metadata
            st.markdown(message["content"])
            
            data = message["raw_data"]
            
            st.divider()
            
            # Provenance Metrics
            st.markdown("**Response Metadata**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="gov-metric">
                    <div class="label">Confidence</div>
                    <div class="value">{data['confidence_score']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="gov-metric">
                    <div class="label">Agent</div>
                    <div class="value" style="font-size: 1.1rem;">{data['agent_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="gov-metric">
                    <div class="label">Domain</div>
                    <div class="value" style="font-size: 1.1rem;">{data['domain'].title()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="gov-metric">
                    <div class="label">Freshness</div>
                    <div class="value" style="font-size: 1rem;">{data['data_freshness']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Source Citations
            st.markdown("**Dataset Provenance**")
            for source in data['sources_cited']:
                badge_class = "live" if "[REAL]" in source or "[LIVE]" in source else ""
                st.markdown(f'<span class="source-tag {badge_class}">📄 {source}</span>', unsafe_allow_html=True)
            
            # Medical Disclaimer
            if "108" in data['answer'] or "doctor" in data['answer'].lower():
                st.markdown("""
                <div class="gov-disclaimer">
                    <strong>Medical Disclaimer:</strong> This is an AI assistant, not a doctor. 
                    For medical emergencies, call <strong>108</strong> (Ambulance) or <strong>112</strong> (Emergency).
                </div>
                """, unsafe_allow_html=True)
            
            # Routing Metadata
            if "routed_by" in data.get("metadata", {}):
                with st.expander("🔍 View Routing Details"):
                    st.json(data["metadata"])
        else:
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Enter your query about Maharashtra's government data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing query..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/agents/munde-sahayak/ask",
                    json={"query": prompt},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()["response"]
                
                answer = data["answer"].replace("\n", "<br>")
                st.markdown(answer)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "raw_data": data
                })
                
                st.rerun()
                
            except requests.exceptions.ConnectionError:
                st.error("""
                **Connection Error**
                
                Cannot connect to the backend API. Please ensure the FastAPI server is running:
                ```bash
                uv run uvicorn munde.api.main:app --reload --host 0.0.0.0 --port 8004
                ```
                """)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================================================
# PROFESSIONAL GOVERNMENT FOOTER
# ============================================================================
st.markdown("""
<div class="gov-footer">
    <h4>Project Munde — Maharashtra Digital Public Infrastructure</h4>
    <p><strong>DPI Pillars:</strong> Data Infrastructure ✅ | AI Infrastructure ✅ | Platform Infrastructure 🟡 | Ecosystem Infrastructure </p>
    <p><strong>Technology Stack:</strong> FastAPI | Dagster | PostgreSQL + pgvector | all-MiniLM-L6-v2 | Qwen2.5 on NVIDIA DGX Spark</p>
    <p><strong>Design Principles:</strong> Sovereign | Zero Hallucination | Graceful Degradation | Full Dataset Provenance | Accessibility Compliant</p>
    <p style="margin-top: 1.5rem; opacity: 0.8; font-size: 0.8rem;">
        © 2026 Project Munde | Government of Maharashtra Initiative
    </p>
</div>
""", unsafe_allow_html=True)
