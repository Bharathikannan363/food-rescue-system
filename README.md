# Food Rescue & Redistribution System

A full-stack, modular, role-based web application connecting **Food Donors, NGOs, Volunteers, and Administrators** to eliminate food waste and deliver surplus meals to people in need.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, React Router DOM, Axios, Recharts, Leaflet & React-Leaflet, Lucide Icons
- **Backend**: Python Flask, Flask-SQLAlchemy ORM, Flask-JWT-Extended, Flask-CORS, Werkzeug Password Hashing
- **Database**: SQLite (`database/food_rescue.db`)
- **Authentication**: Username, Password, 5-digit CAPTCHA Code, JWT Authentication with Role-Based Route Guards
- **Tracking & Maps**: HTML5 Geolocation API (`navigator.geolocation.watchPosition`), Leaflet OpenStreetMap Tiles
- **Notifications**: In-App Notification Center & Mock SMS Dispatcher (with optional Twilio integration)

---

## 🚀 Quick Setup & Local Running Instructions

### 1. Backend Server Setup

```bash
cd backend
python seed.py        # Initializes SQLite database & populates demo accounts
python run.py         # Launches Flask REST API server 
```

### 2. Frontend Web Application Setup

```bash
cd frontend
npm install           # Installs React, Vite, Leaflet, Recharts, Lucide dependencies
npm run dev           # Starts Vite Development Server on http://localhost:3000
```

---

## 🔄 End-to-End Workflow Demonstration

1. **Donor** logs in and posts surplus food with photo preview and pickup map pin.
2. **NGO** browses available food, completes **FSSAI Quality Check**, and submits food request.
3. **Donor** reviews NGO request and clicks **ACCEPT**.
4. **Admin** assigns approved volunteer to the accepted request.
5. **Volunteer** accepts assignment, broadcasts live GPS position, updates delivery status (*Picked Up → Out for Delivery*), and uploads proof photo.
6. **NGO** verifies delivered food proof and submits beneficiary count (`Mark as Done NGO OK`).
7. **Admin** analytics and CSV monthly reports update automatically with audit action logs recorded.
