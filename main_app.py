import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import random
from streamlit_option_menu import option_menu

# Import custom modules
from gamification_engine import GamificationEngine
from ai_components import AIComponents
from live_interaction import LiveInteractionManager

# ==========================================
# 🚀 PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Pro Event Engagement Booster", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🎭 UI & STYLING
# ==========================================
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
try:
    local_css("style.css")
except Exception:
    st.warning("Custom CSS could not be loaded. Professional theme may be affected.")

# ==========================================
# 🛠️ SESSION STATE & ENGINES
# ==========================================
@st.cache_resource
def get_engines():
    return {
        'gamification': GamificationEngine(),
        'ai': AIComponents(),
        'live': LiveInteractionManager()
    }

engines = get_engines()

# Persistent state for live interactions
if 'live_mgr' not in st.session_state:
    st.session_state.live_mgr = engines['live']
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Participant" # Default to Participant for safety
if 'is_admin_authenticated' not in st.session_state:
    st.session_state.is_admin_authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = "Taniya" 

mgr = st.session_state.live_mgr

# ==========================================
# 📊 DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("attendees.csv")
        ev = pd.read_csv("events.csv")
        ev["StartDateTime"] = pd.to_datetime(ev["StartDateTime"])
        return df, ev
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

df, events_df = load_data()

def load_user_activities():
    try:
        with open("user_activities.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_user_activities(data):
    with open("user_activities.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

activities = load_user_activities()

# ==========================================
# 🌱 DATA SEEDING (Ensure demo looks good)
# ==========================================
def seed_data():
    changed = False
    for _, row in df.iterrows():
        name = row["Name"]
        if name not in activities:
            activities[name] = {
                "interests": row.get("Interests", "AI"),
                "days_before_registration": random.randint(1, 15),
                "activities": {
                    "event_registration": random.randint(1, 5),
                    "pre_event_quiz": random.randint(0, 3),
                    "social_share": random.randint(0, 2),
                    "event_attendance": 1 if row["Attended"] == "Yes" else 0
                }
            }
            changed = True
    if changed:
        save_user_activities(activities)

seed_data()

# ==========================================
# 🧭 NAVIGATION
# ==========================================
st.markdown('<h1 class="main-header">Pro Event Engagement Booster</h1>', unsafe_allow_html=True)

# Sidebar Navigation & Access Control
with st.sidebar:
    st.markdown("### User Persona")
    new_role = st.selectbox("Switch View:", ["Participant", "Organizer"], index=0 if st.session_state.user_role == "Participant" else 1)
    
    if new_role != st.session_state.user_role:
        st.session_state.user_role = new_role
        if new_role == "Participant":
            st.session_state.is_admin_authenticated = False
        st.rerun()

    if st.session_state.user_role == "Organizer":
        if not st.session_state.is_admin_authenticated:
            st.markdown("---")
            st.markdown("#### Admin Access")
            access_code = st.text_input("Enter Organizer Code:", type="password")
            if st.button("Authenticate"):
                if access_code == "admin123":
                    st.session_state.is_admin_authenticated = True
                    st.success("Access Granted")
                    st.rerun()
                else:
                    st.error("Invalid Code")
        else:
            st.success("Authenticated")
            if st.button("Logout Admin"):
                st.session_state.is_admin_authenticated = False
                st.rerun()
    
    if st.session_state.user_role == "Participant":
        st.session_state.current_user = st.selectbox("Identity:", df["Name"].tolist() if not df.empty else ["Guest"])
        st.info(f"Viewing as: {st.session_state.current_user}")

# Main Content Area
role_class = "role-organizer" if st.session_state.user_role == "Organizer" else "role-participant"
st.markdown(f'<div class="role-badge {role_class}">{st.session_state.user_role} Mode</div>', unsafe_allow_html=True)

# Navigation Mapping
if st.session_state.user_role == "Organizer":
    if not st.session_state.is_admin_authenticated:
        st.warning("Admin authentication required. Please use the sidebar to sign in.")
        st.stop()
    pages_map = {
        "Executive Dashboard": "dashboard",
        "Engagement Center": "engagement",
        "Live Operations": "live",
        "Campaign Manager": "comms",
        "Advanced Analytics": "analytics"
    }
    nav_icons = ["grid", "cpu", "activity", "send", "bar-chart-line"]
else:
    pages_map = {
        "Overview": "dashboard",
        "My Activity": "engagement",
        "Live Access": "live",
        "Marketplace": "analytics"
    }
    nav_icons = ["person", "award", "broadcast", "bag-check"]

selected_name = option_menu(
    menu_title=None,
    options=list(pages_map.keys()),
    icons=nav_icons,
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "5px", "background-color": "#FFFFFF", "border": "1px solid rgba(0,0,0,0.05)", "border-radius": "8px", "box-shadow": "none"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin":"2px", "color": "#64748B", "font-weight": "500"},
        "nav-link-selected": {"background-color": "#4F46E5", "color": "#FFFFFF", "font-weight": "600", "border-radius": "4px"},
    }
)

selected = pages_map[selected_name]

# ==========================================
# 📊 PAGE: DASHBOARD
# ==========================================
if selected == "dashboard":
    st.header("Reality Dashboard Overview")
    
    # Hero Summary
    total_reg = len(df)
    conf_att = len(df[df["Attended"] == "Yes"])
    campaigns = 7
    live_eng = 84
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registered", total_reg, "Active")
    with col2:
        st.metric("Confirmed Attendance", conf_att, f"{(conf_att/total_reg*100):.1f}% Rate")
    with col3:
        st.metric("Active Campaigns", campaigns, "3 Scheduled")
    with col4:
        st.metric("Live Engagement", f"{live_eng}%", "High")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Attendance & Engagement Trends")
        # Sample trend data
        dates = pd.date_range(end=datetime.now(), periods=10).strftime('%b %d')
        trend_df = pd.DataFrame({
            "Date": dates,
            "Engagement": [random.randint(60, 95) for _ in range(10)],
            "Attendance": [random.randint(40, 80) for _ in range(10)]
        })
        fig = px.area(trend_df, x="Date", y=["Engagement", "Attendance"], 
                      color_discrete_sequence=['#BC13FE', '#0047AB'],
                      template="plotly_white")
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("🎯 Segment Breakdown")
        segments = df['Interests'].str.split(';').explode().value_counts().head(5)
        fig_pie = px.pie(values=segments.values, names=segments.index, hole=.6,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🎮 PAGE: ENGAGEMENT HUB
# ==========================================
elif selected == "engagement":
    st.header("Gamification Hub")
    
    user = st.session_state.current_user
    user_data = df[df["Name"] == user].iloc[0] if user in df["Name"].values else None
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.markdown(f'<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        st.subheader(f"Welcome, {user}")
        u_acts = activities.get(user, {}).get("activities", {})
        points = engines['gamification'].calculate_user_points({"activities": u_acts})
        badges = engines['gamification'].check_badges({"activities": u_acts, "days_before_registration": 10})
        
        st.markdown(f"### {points} Points")
        st.markdown(f"**Badges Earned:** {len(badges)}")
        for b in badges:
            st.markdown(f" - {engines['gamification'].badges[b]['name']}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("📅 Event Countdown")
        next_ev = events_df.iloc[0]
        st.markdown(f"""
        <div class="glass-card" style="background: var(--secondary-gradient); color: white;">
            <h4>{next_ev['Event']}</h4>
            <p>Starts in: <b>{(next_ev['StartDateTime'] - datetime.now()).days} Days</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        tab_quiz, tab_net, tab_lb = st.tabs(["Engagement Quiz", "Networking", "Leaderboard"])
        
        with tab_quiz:
            st.subheader("Unlock Points with Mini-Quizzes")
            topic = st.selectbox("Choose a topic to test your knowledge:", ["AI", "SaaS", "Marketing"])
            q_list = engines['gamification'].generate_quiz_questions(topic)
            
            with st.form("quiz_form"):
                ans_list = []
                for i, q in enumerate(q_list[:2]):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    ans = st.radio("Select answer:", q['options'], key=f"q_{i}")
                    ans_list.append(ans)
                
                if st.form_submit_button("Submit Answers"):
                    correct = 0
                    for i, q in enumerate(q_list[:2]):
                        if q['options'].index(ans_list[i]) == q['correct']:
                            correct += 1
                    
                    if correct == 2:
                        st.success("Perfect! You earned 30 points!")
                        # Update points logic here...
                    else:
                        st.info(f"You got {correct}/2 correct! Keep learning.")

        with tab_net:
            st.subheader("People you should connect with")
            interests = user_data["Interests"] if user_data is not None else "AI"
            suggestions = engines['gamification'].suggest_connections(interests, activities)
            
            for s in suggestions[:3]:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <b>{s['name']}</b><br>
                            <small>Shared: {', '.join(s['common_interests'])}</small>
                        </div>
                        <div style="color: #0047AB; font-weight:bold;">{s['match_score']*100:.0f}% Match</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_lb:
            st.subheader("Global Leaderboard")
            lb = engines['gamification'].create_leaderboard(activities)
            lb_df = pd.DataFrame(lb).head(10)
            st.table(lb_df[['name', 'points', 'badges_count']])

# ==========================================
# ⚡ PAGE: LIVE ACTIVITY
# ==========================================
elif selected == "live":
    st.header("Real-Time Interaction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tl1, tl2 = st.tabs(["Active Polls", "Q&A Session"])
        
        with tl1:
            if st.session_state.user_role == "Organizer":
                with st.expander("➕ Create New Poll", expanded=False):
                    pq = st.text_input("Poll Question")
                    po = st.text_area("Options (one per line)")
                    if st.button("Launch Poll"):
                        opts = [o.strip() for o in po.split('\n') if o.strip()]
                        pid = mgr.create_poll(pq, opts)
                        st.success(f"Poll {pid} is now live!")
            
            if mgr.active_polls:
                for pid, pdata in mgr.active_polls.items():
                    st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                    st.write(f"**{pdata['question']}**")
                    choice = st.radio("Your vote:", pdata['options'], key=f"vote_{pid}")
                    if st.button("Submit Vote", key=f"btn_{pid}"):
                        mgr.submit_poll_response(pid, choice)
                        st.success("Vote recorded!")
                    
                    # Results Logic
                    res = mgr.get_poll_results(pid)
                    if res and res['total_responses'] > 0:
                        fig_res = px.bar(x=list(res['responses'].keys()), y=list(res['responses'].values()),
                                         color=list(res['responses'].keys()), color_discrete_sequence=px.colors.qualitative.Prism)
                        fig_res.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0))
                        st.plotly_chart(fig_res, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No active polls at the moment. Organizers can launch them above.")

        with tl2:
            st.subheader("Ask the Speakers")
            q_input = st.text_input("What is on your mind?")
            if st.button("Post Question"):
                if q_input:
                    mgr.add_qa_question(q_input, st.session_state.current_user)
                    st.success("Question submitted to the queue!")
            
            st.divider()
            st.subheader("Questions from Audience")
            q_queue = mgr.get_qa_queue(sort_by='votes')
            for q in q_queue:
                st.markdown(f"""
                <div class="glass-card">
                    <p><b>{q['user_name']}</b>: {q['question']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <small>{q['timestamp'].strftime('%H:%M')}</small>
                        <span>👍 {q['votes']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Upvote", key=f"up_{q['id']}"):
                    mgr.vote_qa_question(q['id'])
                    st.rerun()

    with col2:
        st.subheader("💬 Live Chat")
        st.markdown('<div class="glass-card" style="height: 400px; overflow-y: auto;">', unsafe_allow_html=True)
        msgs = mgr.get_chat_messages(limit=20)
        for m in reversed(msgs):
            cls = "user-message" if m['user_name'] != "Assistant" else "bot-message"
            st.markdown(f"""
            <div class="chat-message {cls}">
                <b>{m['user_name']}</b><br>{m['message']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        chat_msg = st.text_input("Send a message...", key="chat_input")
        if st.button("Send Chat") and chat_msg:
            mgr.add_chat_message(st.session_state.current_user, chat_msg)
            st.rerun()

# ==========================================
# 📧 PAGE: SMART COMMS
# ==========================================
elif selected == "comms":
    st.header("AI Campaign Manager")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Campaign Config")
        campaign = st.selectbox("Template:", ["Early Teaser", "Warm-up Reminder", "Last Call", "Survey"])
        segment = st.selectbox("Target Audience:", ["Highly Engaged", "At Risk", "All Participants"])
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("**AI Predictor**")
        st.write(f"Likely Open Rate: **{random.randint(45, 88)}%**")
        st.write(f"Estimated Conversion: **{random.randint(5, 15)}%**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Execute Campaign"):
            st.success("Campaign deployed to production!")

    with col2:
        st.subheader("Personalized Template Preview")
        # Logic to generate teaser
        fake_user = {"interests": "AI;SaaS"}
        teaser = engines['gamification'].generate_personalized_teaser(fake_user, {})
        
        st.markdown(f"""
        <div class="glass-card" style="border-left: 10px solid #BC13FE;">
            <p><b>Subject:</b> Your exclusive insight for the upcoming event!</p>
            <p>Hi [Attendee Name],</p>
            <p>{teaser}</p>
            <p>We saw your interest in <b>AI and SaaS</b>, and we've tailored the keynote just for you.</p>
            <p>Can't wait to see you there!</p>
            <hr>
            <small>Personalization Score: 94%</small>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 📈 PAGE: PRO ANALYTICS
# ==========================================
elif selected == "analytics":
    st.header("ROI & Event Intelligence")
    
    # Executive Summary Row
    e1, e2, e3 = st.columns(3)
    
    roi_data = engines['ai'].calculate_roi_prediction({
        'total_registrations': 150,
        'attendance_rate': 0.75,
        'avg_engagement_score': 0.68,
        'event_costs': 5000
    })

    with e1:
        st.metric("Estimated Revenue", f"${roi_data['estimated_revenue']:,.0f}")
    with e2:
        st.metric("ROI Percentage", f"{roi_data['roi_percentage']:.1f}%")
    with e3:
        st.metric("Churn Risk", "Low", "Trending Down")

    # Detailed Charts
    st.subheader("Sentiment Analysis & Topic Extraction")
    c_left, c_right = st.columns(2)
    
    with c_left:
        # Topic chart
        topics = engines['ai'].extract_key_topics(["AI", "SaaS", "Growth", "Engagement", "Webinar", "AI", "Cloud"])
        topic_counts = pd.Series(topics).value_counts()
        fig_topic = px.bar(x=topic_counts.index, y=topic_counts.values, 
                           title="Top Discussion Topics",
                           color_discrete_sequence=['#BC13FE'])
        st.plotly_chart(fig_topic, use_container_width=True)
    
    with c_right:
        # Sentiment Chart
        sentiments = {"Positive": 65, "Neutral": 25, "Negative": 10}
        fig_sent = px.funnel_area(names=list(sentiments.keys()), values=list(sentiments.values()),
                                  title="Audience Sentiment Distribution")
        st.plotly_chart(fig_sent, use_container_width=True)

    st.subheader("Attendee Segments (AI Clustering)")
    clusters = engines['ai'].cluster_attendees(activities)
    if clusters['clusters']:
        cols = st.columns(len(clusters['clusters']))
        for i, (name, members) in enumerate(clusters['clusters'].items()):
            with cols[i]:
                st.markdown(f"""
                <div class="glass-card">
                    <h4>{name}</h4>
                    <p style="font-size: 2rem; font-weight:800; color:#0047AB;">{len(members)}</p>
                    <small>Attendees in this segment</small>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 🏁 FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Powered by <b>NextGen AI</b> | Built for Professional Event Excellence</p>
    <p>© 2026 Event Booster | All Intelligence Localized</p>
</div>
""", unsafe_allow_html=True)
