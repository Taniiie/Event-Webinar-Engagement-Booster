# Pro Event & Webinar Engagement Booster

A professional-grade, AI-powered platform for maximizing event and webinar engagement. Built with **Streamlit**, this application provides organizers with powerful analytics tools and participants with an interactive, gamified experience.

---

## Features

### For Organizers (Authenticated Access)
| Feature | Description |
|---|---|
| **Executive Dashboard** | Real-time metrics for registrations, attendance rates, and engagement scores with interactive Plotly charts. |
| **Campaign Manager** | AI-driven email campaign builder with personalized templates, open-rate predictions, and audience segmentation. |
| **Live Operations** | Launch polls, manage Q&A queues, and monitor live chat during events in real-time. |
| **Advanced Analytics** | ROI prediction, sentiment analysis, topic extraction, and AI-powered attendee clustering. |

### For Participants
| Feature | Description |
|---|---|
| **Overview Dashboard** | Personalized view of event metrics and upcoming sessions. |
| **Gamification Hub** | Earn points through quizzes, unlock badges, and compete on a global leaderboard. |
| **Live Access** | Vote in polls, ask questions in Q&A sessions, and chat with other attendees. |
| **AI Networking** | Smart match-making based on shared interests with compatibility scores. |

### Core AI Capabilities
- **Engagement Prediction** — Forecast attendee engagement using machine learning.
- **Churn Analysis** — Identify at-risk registrants before they drop off.
- **Sentiment Analysis** — Real-time sentiment scoring of chat and feedback.
- **Content Recommendations** — Personalized session suggestions based on interests.
- **ROI Prediction** — Estimate event revenue and return on investment.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Plotly, Custom CSS |
| AI/ML | Scikit-learn, TextBlob, NumPy |
| Data | Pandas, JSON |
| Design | Enterprise SaaS (Indigo + Slate palette) |

---

## Project Structure

```
├── main_app.py              # Main application entry point
├── ai_components.py         # AI/ML modules (prediction, clustering, sentiment)
├── gamification_engine.py   # Gamification logic (points, badges, leaderboard)
├── live_interaction.py      # Real-time interaction manager (polls, Q&A, chat)
├── style.css                # Professional SaaS theme
├── attendees.csv            # Sample attendee data
├── events.csv               # Sample event schedule
├── user_activities.json     # Persistent user activity data
└── requirements.txt         # Python dependencies
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/Taniiie/Event-Webinar-Engagement-Booster.git
cd Event-Webinar-Engagement-Booster

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main_app.py
```

The application will open at `http://localhost:8501`.

---

## Usage

### Participant Mode (Default)
1. Open the app — you start in **Participant** mode.
2. Select your identity from the sidebar dropdown.
3. Browse **Overview**, **My Activity**, **Live Access**, and **Marketplace** tabs.

### Organizer Mode
1. Open the sidebar and switch the view to **Organizer**.
2. Enter the admin access code: `admin123`
3. Access the full management suite: **Executive Dashboard**, **Engagement Center**, **Live Operations**, **Campaign Manager**, and **Advanced Analytics**.

---

## Screenshots

### Participant Overview
Clean, data-driven dashboard tailored for attendees.

### Organizer Executive Dashboard
Full management suite with real-time metrics and AI-powered insights.

---

## Dependencies

```
streamlit
pandas
numpy
plotly
scikit-learn
textblob
streamlit-option-menu
openai
```

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Author

Built with precision by **Taniiie** — [GitHub Profile](https://github.com/Taniiie)
