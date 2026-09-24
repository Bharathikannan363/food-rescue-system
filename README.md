# Food Rescue & Redistribution System

A full-stack, modular, role-based web application connecting **Food Donors, NGOs, Volunteers, and Administrators** to eliminate food waste and deliver surplus meals to people in need.

---

## ✨ Key Features

- **Role-Based Portals** — separate dashboards and permissions for Donors, NGOs, Volunteers, and Admin (JWT + CAPTCHA + RBAC guards on every endpoint)
- **Expiry Validation (FSSAI-aligned)** — donations carry preparation & best-before times; every donation is flagged **FRESH / EXPIRING SOON (≤ 2 h) / EXPIRED** on read. Expired food is blocked from NGO requests and delivery confirmations *server-side*
- **Proximity Matcher** — the admin's assignment screen lists approved volunteers **ranked nearest-first** (haversine distance from each volunteer's latest live GPS ping to the donation pickup pin), with km shown markers, and manual override always possible. Pickup distance is recorded in the audit log
- **Enforced Delivery Workflow** — status transitions *Assigned → Accepted → Picked Up → Out for Delivery → Delivered* are validated server-side (no skipping or going backwards), with race protection on assignment acceptance
- **Resource Ownership Guards** — volunteers can only respond to / update / upload proof for their own assignments; NGOs can only confirm their own deliveries
- **Live Tracking & Proof** — HTML5 Geolocation broadcasting, Leaflet/OpenStreetMap live maps, delivery proof photo uploads, beneficiary-count confirmation ("Mark as Done NGO OK")
- **Analytics & Audit** — auto-computed impact metrics (deliveries, beneficiaries, food saved), monthly CSV report export, and audit logs that record actions including pickup distances

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, React Router DOM, Axios, Recharts, Leaflet & React-Leaflet, Lucide Icons
- **Backend**: Python Flask, Flask-SQLAlchemy ORM, Flask-JWT-Extended, Flask-CORS, Werkzeug Password Hashing
- **Database**: SQLite (`database/food_rescue.db`) — geospatial distances computed in Python (haversine)
- **Authentication**: Username, Password, 5-digit CAPTCHA Code, JWT Authentication with Role-Based Route Guards
- **Tracking & Maps**: HTML5 Geolocation API (`navigator.geolocation.watchPosition`), Leaflet OpenStreetMap Tiles
- **Notifications**: In-App Notification Center & Mock SMS Dispatcher (with optional Twilio integration)

---

## 🚀 Quick Setup & Local Running Instructions

### 1. Backend Server Setup

```bash
cd backend
python seed.py       
python run.py         
```

### 2. Frontend Web Application Setup

```bash
cd frontend
npm install          
npm run dev           
```

## 🔄 End-to-End Workflow Demonstration

1. **Donor** logs in and posts surplus food with photo preview, pickup map pin, and **best-before/expiry time**.
2. **NGO** browses available food with **FRESH / EXPIRING SOON / EXPIRED** badges, completes the **FSSAI Quality Check**, and submits a food request (expired donations are blocked).
3. **Donor** reviews the NGO request and clicks **ACCEPT**.
4. **Admin** opens the assignment screen — volunteers are **ranked nearest-first by live GPS distance** — and assigns a volunteer (manual override possible).
5. **Volunteer** accepts the assignment, broadcasts live GPS position, updates delivery status (*Picked Up → Out for Delivery → Delivered* — order enforced server-side), and uploads the proof photo.
6. **NGO** verifies the delivered food proof and submits the beneficiary count (`Mark as Done NGO OK`).
7. **Admin** analytics, CSV monthly reports, and audit logs (with recorded pickup distances) update automatically.

        ├── 📁 hooks/                    # useAuth, useGeolocation, useNotifications
        ├── 📁 routes/                   # AppRoutes (URL mapping & role guards)
        └── 📁 mock/                     # mockData.js (Fallback mock data)


