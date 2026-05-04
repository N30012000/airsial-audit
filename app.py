import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="AirSial Safety Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Airsial Green Theme
PRIMARY_GREEN = "#1E7E34"
LIGHT_GREEN = "#2FA34F"
DARK_GREEN = "#0F4620"
ACCENT_GREEN = "#00A86B"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
DARK_TEXT = "#1a1a1a"

# Custom CSS for Airsial theme
st.markdown(f"""
<style>
    /* Main theme */
    .main {{
        background-color: {LIGHT_GRAY};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {DARK_GREEN};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {PRIMARY_GREEN} !important;
    }}
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {{
        color: white !important;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        color: {PRIMARY_GREEN};
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {PRIMARY_GREEN};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }}
    
    .stButton > button:hover {{
        background-color: {DARK_GREEN};
    }}
    
    /* Form elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {{
        border-color: {PRIMARY_GREEN} !important;
    }}
    
    /* Form label */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stDateInput > label {{
        color: {DARK_GREEN} !important;
        font-weight: 600 !important;
    }}
    
    /* Radio buttons */
    .stRadio > label {{
        color: {DARK_GREEN} !important;
    }}
    
    /* Data tables */
    [data-testid="stDataFrame"] {{
        background-color: white;
    }}
    
    /* Success/Info messages */
    .stSuccess {{
        background-color: {ACCENT_GREEN} !important;
    }}
    
    .stInfo {{
        background-color: {LIGHT_GREEN} !important;
    }}
    
    .stWarning {{
        background-color: #F97316 !important;
    }}
    
    /* Dividers */
    hr {{
        border-color: {PRIMARY_GREEN} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
def init_session_state():
    if 'fsr_data' not in st.session_state:
        st.session_state.fsr_data = pd.DataFrame({
            'Date': ['29/04/2026', '26/04/2026', '20/04/2026', '13/04/2026', '27/03/2026'],
            'Flight': ['PF-145', 'PF-743', 'PF-742', 'PF-717', 'PF-723'],
            'Aircraft': ['AP-BOA', 'AP-BOS', 'AP-BOS', 'AP-BOS', 'AP-BOA'],
            'Category': ['Medical Emergency', 'Smoke', 'Medical', 'Medical/Delays', 'Medical Emergency'],
            'Incident': ['PAX fainted, hypoxia', 'PAX smoked in LAV', 'Chest pain complaint', 'PAX fainted pre-departure', 'Breathing difficulty'],
            'Action Taken': ['Oxygen administered', 'Security handed over', 'Offboarded safely', 'Medical team called', 'Oxygen provided']
        })

    if 'mor_data' not in st.session_state:
        st.session_state.mor_data = pd.DataFrame({
            'Date': ['23/03/2026', '15/03/2026', '08/03/2026', '01/03/2026', '13/08/2025'],
            'Flight': ['PF-768', 'PF-1785', 'PF-714', 'PF-717', 'PF-786'],
            'Aircraft': ['AP-BOR', 'AP-BPH', 'AP-BOA', 'AP-BOR', 'AP-BOC'],
            'Issue': ['Pressurization valve failure', 'FOD ingestion engine 2', 'Both PACKS failed', 'Near collision - TCAS', 'L1 door without disarm'],
            'Damage': ['None', 'None', 'None', 'None', 'None'],
            'Status': ['Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved']
        })

    if 'hira_data' not in st.session_state:
        st.session_state.hira_data = pd.DataFrame({
            'Date': ['25/04/2026', '20/04/2026', '15/04/2026', '10/04/2026', '18/12/2025'],
            'Reporter': ['Abdul Moied', 'Faheem Haris', 'Raza Haider', 'Adeeb Arshad', 'Safety Team'],
            'Department': ['Safety', 'Engineering', 'Engineering', 'Engineering', 'Operations'],
            'Hazard': ['Staff without PPE', 'Engines running during maintenance', 'GPU unattended', 'Waste cart fire', 'Unsupervised passengers'],
            'Risk Level': ['High', 'Medium', 'High', 'High', 'Medium'],
            'Status': ['Open', 'Closed', 'Open', 'Closed', 'Closed']
        })

    if 'bird_data' not in st.session_state:
        st.session_state.bird_data = pd.DataFrame({
            'Date': ['20/04/2026', '16/04/2026', '12/04/2026', '26/03/2026', '14/02/2026'],
            'Flight': ['PF-732', 'PF-741', 'PF-742', 'PF-142', 'PF-121'],
            'Aircraft': ['AP-BPF', 'AP-BPJ', 'AP-BPF', 'AP-BOA', 'AP-BOA'],
            'Phase': ['Climb', 'Descend', 'Takeoff/Climb', 'Takeoff', 'Takeoff'],
            'Parts Affected': ['Engine #2', 'None', 'Seat #2 left wing', 'None', 'Pitot (CAPT side)'],
            'Damage': ['None', 'None', 'None', 'None', 'None']
        })

init_session_state()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("✈️ AirSial Safety Dashboard")
    st.markdown("**Comprehensive Safety & Incident Reporting System** | Audit Ready")
with col2:
    st.markdown(f"""
    <div style='background-color: {PRIMARY_GREEN}; color: white; padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='margin: 0; color: white;'>🟢 AirSial</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar navigation
with st.sidebar:
    st.markdown(f"<h2 style='color: white;'>📋 Navigation</h2>", unsafe_allow_html=True)
    page = st.radio(
        "Select Section:",
        ["📊 Dashboard", "📝 FSR Reports", "🔧 MOR Reports", "⚠️ HIRA Assessments", "🐦 Bird Strikes"],
        key="page_nav"
    )

# DASHBOARD PAGE
if page == "📊 Dashboard":
    st.header("📊 Safety Overview Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total FSR Reports", len(st.session_state.fsr_data), "✈️")
    with col2:
        st.metric("Total MOR Reports", len(st.session_state.mor_data), "🔧")
    with col3:
        st.metric("HIRA Assessments", len(st.session_state.hira_data), "⚠️")
    with col4:
        st.metric("Bird Strikes", len(st.session_state.bird_data), "🐦")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 FSR by Category")
        if len(st.session_state.fsr_data) > 0:
            fsr_cat = st.session_state.fsr_data['Category'].value_counts()
            st.bar_chart(fsr_cat, color=PRIMARY_GREEN)
        else:
            st.info("No data yet")
    
    with col2:
        st.subheader("📊 MOR Status Distribution")
        if len(st.session_state.mor_data) > 0:
            mor_status = st.session_state.mor_data['Status'].value_counts()
            st.bar_chart(mor_status, color=LIGHT_GREEN)
        else:
            st.info("No data yet")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 HIRA Risk Distribution")
        if len(st.session_state.hira_data) > 0:
            hira_risk = st.session_state.hira_data['Risk Level'].value_counts()
            st.bar_chart(hira_risk, color=ACCENT_GREEN)
        else:
            st.info("No data yet")
    
    with col2:
        st.subheader("📊 Bird Strike by Phase")
        if len(st.session_state.bird_data) > 0:
            bird_phase = st.session_state.bird_data['Phase'].value_counts()
            st.bar_chart(bird_phase, color=PRIMARY_GREEN)
        else:
            st.info("No data yet")

# FSR REPORTS PAGE
elif page == "📝 FSR Reports":
    st.header("📝 Flight Safety Reports (FSR)")
    st.markdown("_In-flight incidents including medical emergencies, disruptive passengers, and safety concerns_")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        action = st.selectbox("Action:", ["📋 View Reports", "➕ Add New Report", "✏️ Edit/Delete Report"], key="fsr_action")
    with col2:
        if st.button("🔄 Refresh", key="fsr_refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    if action == "📋 View Reports":
        st.subheader("All FSR Reports")
        if len(st.session_state.fsr_data) > 0:
            st.dataframe(st.session_state.fsr_data, use_container_width=True, hide_index=True)
            
            csv = st.session_state.fsr_data.to_csv(index=False)
            st.download_button("📥 Download as CSV", csv, "fsr_reports.csv", "text/csv")
        else:
            st.info("No FSR reports yet. Create your first report!")
    
    elif action == "➕ Add New Report":
        st.subheader("Add New FSR Report")
        with st.form("add_fsr_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date of Incident")
                flight = st.text_input("✈️ Flight Number (e.g., PF-145)")
            with col2:
                aircraft = st.text_input("🛫 Aircraft Registration (e.g., AP-BOA)")
                category = st.selectbox("🏷️ Category", 
                    ["Medical Emergency", "Disruptive Passenger", "Smoke", "Engineering", "Delays", "Others"])
            
            incident = st.text_area("📝 Incident Description", height=100)
            action_taken = st.text_area("✅ Action Taken", height=100)
            
            if st.form_submit_button("➕ Add FSR Report", use_container_width=True):
                if flight.strip() and aircraft.strip() and incident.strip():
                    new_row = pd.DataFrame({
                        'Date': [date.strftime("%d/%m/%Y")],
                        'Flight': [flight.upper()],
                        'Aircraft': [aircraft.upper()],
                        'Category': [category],
                        'Incident': [incident],
                        'Action Taken': [action_taken]
                    })
                    st.session_state.fsr_data = pd.concat([new_row, st.session_state.fsr_data], ignore_index=True)
                    st.success("✅ FSR Report added successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields!")
    
    elif action == "✏️ Edit/Delete Report":
        st.subheader("Edit or Delete FSR Report")
        if len(st.session_state.fsr_data) > 0:
            report_idx = st.selectbox("Select Report to Edit:", 
                range(len(st.session_state.fsr_data)),
                format_func=lambda i: f"{st.session_state.fsr_data.iloc[i]['Date']} - {st.session_state.fsr_data.iloc[i]['Flight']}")
            
            selected = st.session_state.fsr_data.iloc[report_idx]
            
            st.markdown("**Current Report Details:**")
            st.info(f"**Date:** {selected['Date']} | **Flight:** {selected['Flight']} | **Aircraft:** {selected['Aircraft']}")
            
            with st.form("edit_fsr_form"):
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("📅 Date of Incident", value=pd.to_datetime(selected['Date'], format="%d/%m/%Y"))
                    flight = st.text_input("✈️ Flight Number", value=selected['Flight'])
                with col2:
                    aircraft = st.text_input("🛫 Aircraft Registration", value=selected['Aircraft'])
                    category = st.selectbox("🏷️ Category", 
                        ["Medical Emergency", "Disruptive Passenger", "Smoke", "Engineering", "Delays", "Others"],
                        index=["Medical Emergency", "Disruptive Passenger", "Smoke", "Engineering", "Delays", "Others"].index(selected['Category']))
                
                incident = st.text_area("📝 Incident Description", value=selected['Incident'], height=100)
                action_taken = st.text_area("✅ Action Taken", value=selected['Action Taken'], height=100)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        st.session_state.fsr_data.at[report_idx, 'Date'] = date.strftime("%d/%m/%Y")
                        st.session_state.fsr_data.at[report_idx, 'Flight'] = flight.upper()
                        st.session_state.fsr_data.at[report_idx, 'Aircraft'] = aircraft.upper()
                        st.session_state.fsr_data.at[report_idx, 'Category'] = category
                        st.session_state.fsr_data.at[report_idx, 'Incident'] = incident
                        st.session_state.fsr_data.at[report_idx, 'Action Taken'] = action_taken
                        st.success("✅ Report updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🗑️ Delete Report", use_container_width=True):
                        st.session_state.fsr_data = st.session_state.fsr_data.drop(report_idx).reset_index(drop=True)
                        st.warning("⚠️ Report deleted!")
                        st.rerun()
        else:
            st.info("No reports to edit yet. Add one first!")

# MOR REPORTS PAGE
elif page == "🔧 MOR Reports":
    st.header("🔧 Maintenance Occurrence Reports (MOR)")
    st.markdown("_Technical and mechanical incidents reported by flight crews and maintenance teams_")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        action = st.selectbox("Action:", ["📋 View Reports", "➕ Add New Report", "✏️ Edit/Delete Report"], key="mor_action")
    with col2:
        if st.button("🔄 Refresh", key="mor_refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    if action == "📋 View Reports":
        st.subheader("All MOR Reports")
        if len(st.session_state.mor_data) > 0:
            st.dataframe(st.session_state.mor_data, use_container_width=True, hide_index=True)
            
            csv = st.session_state.mor_data.to_csv(index=False)
            st.download_button("📥 Download as CSV", csv, "mor_reports.csv", "text/csv")
        else:
            st.info("No MOR reports yet. Create your first report!")
    
    elif action == "➕ Add New Report":
        st.subheader("Add New MOR Report")
        with st.form("add_mor_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date of Occurrence", key="mor_date")
                flight = st.text_input("✈️ Flight Number", key="mor_flight")
            with col2:
                aircraft = st.text_input("🛫 Aircraft Registration", key="mor_aircraft")
                issue = st.selectbox("🔴 Issue Type", 
                    ["Technical Fault", "Engine Issue", "Systems Failure", "TCAS Alert", "Navigation Issue", "Door Problem", "Other"], key="mor_issue")
            
            description = st.text_area("📝 Issue Description", key="mor_desc", height=100)
            damage = st.selectbox("💥 Aircraft Damage", ["None", "Minor", "Moderate", "Severe"], key="mor_damage")
            status = st.selectbox("📊 Status", ["Open", "In Progress", "Resolved"], key="mor_status")
            
            if st.form_submit_button("➕ Add MOR Report", use_container_width=True):
                if flight.strip() and aircraft.strip() and description.strip():
                    new_row = pd.DataFrame({
                        'Date': [date.strftime("%d/%m/%Y")],
                        'Flight': [flight.upper()],
                        'Aircraft': [aircraft.upper()],
                        'Issue': [issue],
                        'Damage': [damage],
                        'Status': [status]
                    })
                    st.session_state.mor_data = pd.concat([new_row, st.session_state.mor_data], ignore_index=True)
                    st.success("✅ MOR Report added successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields!")
    
    elif action == "✏️ Edit/Delete Report":
        st.subheader("Edit or Delete MOR Report")
        if len(st.session_state.mor_data) > 0:
            report_idx = st.selectbox("Select Report to Edit:", 
                range(len(st.session_state.mor_data)),
                format_func=lambda i: f"{st.session_state.mor_data.iloc[i]['Date']} - {st.session_state.mor_data.iloc[i]['Flight']}", key="mor_select")
            
            selected = st.session_state.mor_data.iloc[report_idx]
            
            st.markdown("**Current Report Details:**")
            st.info(f"**Date:** {selected['Date']} | **Flight:** {selected['Flight']} | **Aircraft:** {selected['Aircraft']}")
            
            with st.form("edit_mor_form"):
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("📅 Date of Occurrence", value=pd.to_datetime(selected['Date'], format="%d/%m/%Y"), key="mor_edit_date")
                    flight = st.text_input("✈️ Flight Number", value=selected['Flight'], key="mor_edit_flight")
                with col2:
                    aircraft = st.text_input("🛫 Aircraft Registration", value=selected['Aircraft'], key="mor_edit_aircraft")
                    issue = st.selectbox("🔴 Issue Type", 
                        ["Technical Fault", "Engine Issue", "Systems Failure", "TCAS Alert", "Navigation Issue", "Door Problem", "Other"],
                        index=["Technical Fault", "Engine Issue", "Systems Failure", "TCAS Alert", "Navigation Issue", "Door Problem", "Other"].index(selected['Issue']), key="mor_edit_issue")
                
                description = st.text_area("📝 Issue Description", value=selected['Issue'], key="mor_edit_desc", height=100)
                damage = st.selectbox("💥 Aircraft Damage", ["None", "Minor", "Moderate", "Severe"], index=["None", "Minor", "Moderate", "Severe"].index(selected['Damage']), key="mor_edit_damage")
                status = st.selectbox("📊 Status", ["Open", "In Progress", "Resolved"], index=["Open", "In Progress", "Resolved"].index(selected['Status']), key="mor_edit_status")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        st.session_state.mor_data.at[report_idx, 'Date'] = date.strftime("%d/%m/%Y")
                        st.session_state.mor_data.at[report_idx, 'Flight'] = flight.upper()
                        st.session_state.mor_data.at[report_idx, 'Aircraft'] = aircraft.upper()
                        st.session_state.mor_data.at[report_idx, 'Issue'] = issue
                        st.session_state.mor_data.at[report_idx, 'Damage'] = damage
                        st.session_state.mor_data.at[report_idx, 'Status'] = status
                        st.success("✅ Report updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🗑️ Delete Report", use_container_width=True):
                        st.session_state.mor_data = st.session_state.mor_data.drop(report_idx).reset_index(drop=True)
                        st.warning("⚠️ Report deleted!")
                        st.rerun()
        else:
            st.info("No reports to edit yet. Add one first!")

# HIRA PAGE
elif page == "⚠️ HIRA Assessments":
    st.header("⚠️ HIRA - Hazard Identification & Risk Assessment")
    st.markdown("_Safety hazards identified across operations with risk ratings and corrective actions_")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        action = st.selectbox("Action:", ["📋 View Reports", "➕ Add New Report", "✏️ Edit/Delete Report"], key="hira_action")
    with col2:
        if st.button("🔄 Refresh", key="hira_refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    if action == "📋 View Reports":
        st.subheader("All HIRA Assessments")
        if len(st.session_state.hira_data) > 0:
            st.dataframe(st.session_state.hira_data, use_container_width=True, hide_index=True)
            
            csv = st.session_state.hira_data.to_csv(index=False)
            st.download_button("📥 Download as CSV", csv, "hira_reports.csv", "text/csv")
        else:
            st.info("No HIRA assessments yet. Create your first assessment!")
    
    elif action == "➕ Add New Report":
        st.subheader("Add New HIRA Assessment")
        with st.form("add_hira_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date of Report", key="hira_date")
                reporter = st.text_input("👤 Reporter Name", key="hira_reporter")
            with col2:
                department = st.selectbox("🏢 Department", 
                    ["Flight Operations", "Engineering", "Safety", "Airport Services", "Cargo", "Other"], key="hira_dept")
                risk_level = st.selectbox("⚠️ Risk Level", ["Low", "Medium", "High"], key="hira_risk")
            
            hazard = st.text_area("📝 Hazard Description", key="hira_hazard", height=100)
            corrective_action = st.text_area("✅ Corrective Action Plan", key="hira_action_text", height=100)
            status = st.selectbox("📊 Status", ["Open", "In Progress", "Closed"], key="hira_status")
            
            if st.form_submit_button("➕ Add HIRA Assessment", use_container_width=True):
                if reporter.strip() and hazard.strip():
                    new_row = pd.DataFrame({
                        'Date': [date.strftime("%d/%m/%Y")],
                        'Reporter': [reporter],
                        'Department': [department],
                        'Hazard': [hazard],
                        'Risk Level': [risk_level],
                        'Status': [status]
                    })
                    st.session_state.hira_data = pd.concat([new_row, st.session_state.hira_data], ignore_index=True)
                    st.success("✅ HIRA Assessment added successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields!")
    
    elif action == "✏️ Edit/Delete Report":
        st.subheader("Edit or Delete HIRA Assessment")
        if len(st.session_state.hira_data) > 0:
            report_idx = st.selectbox("Select Assessment to Edit:", 
                range(len(st.session_state.hira_data)),
                format_func=lambda i: f"{st.session_state.hira_data.iloc[i]['Date']} - {st.session_state.hira_data.iloc[i]['Reporter']}", key="hira_select")
            
            selected = st.session_state.hira_data.iloc[report_idx]
            
            st.markdown("**Current Assessment Details:**")
            st.info(f"**Date:** {selected['Date']} | **Reporter:** {selected['Reporter']} | **Department:** {selected['Department']}")
            
            with st.form("edit_hira_form"):
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("📅 Date of Report", value=pd.to_datetime(selected['Date'], format="%d/%m/%Y"), key="hira_edit_date")
                    reporter = st.text_input("👤 Reporter Name", value=selected['Reporter'], key="hira_edit_reporter")
                with col2:
                    department = st.selectbox("🏢 Department", 
                        ["Flight Operations", "Engineering", "Safety", "Airport Services", "Cargo", "Other"],
                        index=["Flight Operations", "Engineering", "Safety", "Airport Services", "Cargo", "Other"].index(selected['Department']), key="hira_edit_dept")
                    risk_level = st.selectbox("⚠️ Risk Level", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(selected['Risk Level']), key="hira_edit_risk")
                
                hazard = st.text_area("📝 Hazard Description", value=selected['Hazard'], key="hira_edit_hazard", height=100)
                status = st.selectbox("📊 Status", ["Open", "In Progress", "Closed"], index=["Open", "In Progress", "Closed"].index(selected['Status']), key="hira_edit_status")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        st.session_state.hira_data.at[report_idx, 'Date'] = date.strftime("%d/%m/%Y")
                        st.session_state.hira_data.at[report_idx, 'Reporter'] = reporter
                        st.session_state.hira_data.at[report_idx, 'Department'] = department
                        st.session_state.hira_data.at[report_idx, 'Hazard'] = hazard
                        st.session_state.hira_data.at[report_idx, 'Risk Level'] = risk_level
                        st.session_state.hira_data.at[report_idx, 'Status'] = status
                        st.success("✅ Assessment updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🗑️ Delete Assessment", use_container_width=True):
                        st.session_state.hira_data = st.session_state.hira_data.drop(report_idx).reset_index(drop=True)
                        st.warning("⚠️ Assessment deleted!")
                        st.rerun()
        else:
            st.info("No assessments to edit yet. Add one first!")

# BIRD STRIKE PAGE
elif page == "🐦 Bird Strikes":
    st.header("🐦 Bird Strike Incidents")
    st.markdown("_All recorded bird strike events with aircraft damage assessment and operational phases_")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        action = st.selectbox("Action:", ["📋 View Reports", "➕ Add New Report", "✏️ Edit/Delete Report"], key="bird_action")
    with col2:
        if st.button("🔄 Refresh", key="bird_refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    if action == "📋 View Reports":
        st.subheader("All Bird Strike Reports")
        if len(st.session_state.bird_data) > 0:
            st.dataframe(st.session_state.bird_data, use_container_width=True, hide_index=True)
            
            csv = st.session_state.bird_data.to_csv(index=False)
            st.download_button("📥 Download as CSV", csv, "bird_strikes.csv", "text/csv")
        else:
            st.info("No bird strike reports yet. Create your first report!")
    
    elif action == "➕ Add New Report":
        st.subheader("Add New Bird Strike Report")
        with st.form("add_bird_form"):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("📅 Date of Occurrence", key="bird_date")
                flight = st.text_input("✈️ Flight Number", key="bird_flight")
            with col2:
                aircraft = st.text_input("🛫 Aircraft Registration", key="bird_aircraft")
                phase = st.selectbox("📍 Flight Phase", 
                    ["Takeoff", "Climb", "Descent", "Approach", "Landing", "Unknown"], key="bird_phase")
            
            parts = st.text_input("🔴 Aircraft Parts Affected", key="bird_parts")
            damage = st.selectbox("💥 Aircraft Damage", ["None", "Minor", "Moderate", "Severe"], key="bird_damage")
            remarks = st.text_area("📝 Remarks", key="bird_remarks", height=100)
            
            if st.form_submit_button("➕ Add Bird Strike Report", use_container_width=True):
                if flight.strip() and aircraft.strip():
                    new_row = pd.DataFrame({
                        'Date': [date.strftime("%d/%m/%Y")],
                        'Flight': [flight.upper()],
                        'Aircraft': [aircraft.upper()],
                        'Phase': [phase],
                        'Parts Affected': [parts],
                        'Damage': [damage]
                    })
                    st.session_state.bird_data = pd.concat([new_row, st.session_state.bird_data], ignore_index=True)
                    st.success("✅ Bird Strike Report added successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields!")
    
    elif action == "✏️ Edit/Delete Report":
        st.subheader("Edit or Delete Bird Strike Report")
        if len(st.session_state.bird_data) > 0:
            report_idx = st.selectbox("Select Report to Edit:", 
                range(len(st.session_state.bird_data)),
                format_func=lambda i: f"{st.session_state.bird_data.iloc[i]['Date']} - {st.session_state.bird_data.iloc[i]['Flight']}", key="bird_select")
            
            selected = st.session_state.bird_data.iloc[report_idx]
            
            st.markdown("**Current Report Details:**")
            st.info(f"**Date:** {selected['Date']} | **Flight:** {selected['Flight']} | **Aircraft:** {selected['Aircraft']}")
            
            with st.form("edit_bird_form"):
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("📅 Date of Occurrence", value=pd.to_datetime(selected['Date'], format="%d/%m/%Y"), key="bird_edit_date")
                    flight = st.text_input("✈️ Flight Number", value=selected['Flight'], key="bird_edit_flight")
                with col2:
                    aircraft = st.text_input("🛫 Aircraft Registration", value=selected['Aircraft'], key="bird_edit_aircraft")
                    phase = st.selectbox("📍 Flight Phase", 
                        ["Takeoff", "Climb", "Descent", "Approach", "Landing", "Unknown"],
                        index=["Takeoff", "Climb", "Descent", "Approach", "Landing", "Unknown"].index(selected['Phase']), key="bird_edit_phase")
                
                parts = st.text_input("🔴 Aircraft Parts Affected", value=selected['Parts Affected'], key="bird_edit_parts")
                damage = st.selectbox("💥 Aircraft Damage", ["None", "Minor", "Moderate", "Severe"], index=["None", "Minor", "Moderate", "Severe"].index(selected['Damage']), key="bird_edit_damage")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        st.session_state.bird_data.at[report_idx, 'Date'] = date.strftime("%d/%m/%Y")
                        st.session_state.bird_data.at[report_idx, 'Flight'] = flight.upper()
                        st.session_state.bird_data.at[report_idx, 'Aircraft'] = aircraft.upper()
                        st.session_state.bird_data.at[report_idx, 'Phase'] = phase
                        st.session_state.bird_data.at[report_idx, 'Parts Affected'] = parts
                        st.session_state.bird_data.at[report_idx, 'Damage'] = damage
                        st.success("✅ Report updated successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🗑️ Delete Report", use_container_width=True):
                        st.session_state.bird_data = st.session_state.bird_data.drop(report_idx).reset_index(drop=True)
                        st.warning("⚠️ Report deleted!")
                        st.rerun()
        else:
            st.info("No reports to edit yet. Add one first!")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {PRIMARY_GREEN};'>
    <p><strong>✈️ AirSial Aviation Safety Audit Dashboard</strong></p>
    <p>Data as of May 2026 | For Official Audits and Regulatory Compliance</p>
</div>
""", unsafe_allow_html=True)
