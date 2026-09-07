# Food Rescue & Redistribution System

A full-stack, modular, role-based web application connecting **Food Donors, NGOs, Volunteers, and Administrators** to eliminate food waste and deliver surplus meals to people in need.

---

## ✨ Key Features

- **Role-Based Portals** — separate dashboards and permissions for Donors, NGOs, Volunteers, and Admin (JWT + CAPTCHA + RBAC guards on every endpoint)
- **Expiry Validation (FSSAI-aligned)** — donations carry preparation & best-before times; every donation is flagged **FRESH / EXPIRING SOON (≤ 2 h) / EXPIRED** on read. Expired food is blocked from NGO requests and delivery confirmations *server-side*
- **Proximity Matcher** — the admin's assignment screen lists approved volunteers **ranked nearest-first** (haversine distance from each volunteer's latest live GPS ping to the donation pickup pin), with km shown, `NO LIVE PING` / `NO LOCATION` markers, and manual override always possible. Pickup distance is recorded in the audit log
- **Enforced Delivery Workflow** — status transitions *Assigned → Accepted → Picked Up → Out for Delivery → Delivered* are validated server-side (no skipping or going backwards), with race protection on assignment acceptance
- **Resource Ownership Guards** — volunteers can only respond to / update / upload proof for their own assignments; NGOs can only confirm their own deliveries
- **Live Tracking & Proof** — HTML5 Geolocation broadcasting, Leaflet/OpenStreetMap live maps, delivery proof photo uploads, beneficiary-count confirmation ("Mark as Done NGO OK")
- **Analytics & Audit** — auto-computed impact metrics (deliveries, beneficiaries, food saved), monthly CSV report export, and audit logs that record actions including pickup distances

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS, React Router DOM, Axios, Recharts, Leaflet & React-Leaflet, Lucide Icons
- **Backend**: Python Flask, Flask-SQLAlchemy ORM, Flask-JWT-Extended, Flask-CORS, Werkzeug Password Hashing
- **Database**: SQLite (`database/food_rescue.db`) — geospatial distances computed in Python (haversine), no extra DB extensions needed
- **Authentication**: Username, Password, 5-digit CAPTCHA Code, JWT Authentication with Role-Based Route Guards
- **Tracking & Maps**: HTML5 Geolocation API (`navigator.geolocation.watchPosition`), Leaflet OpenStreetMap Tiles
- **Notifications**: In-App Notification Center & Mock SMS Dispatcher (with optional Twilio integration)

---

## 🚀 Quick Setup & Local Running Instructions

### 1. Backend Server Setup

```bash
cd backend
python seed.py        # Initializes SQLite database & populates demo accounts
python run.py         # Launches Flask REST API server on http://127.0.0.1:5000
```

### 2. Frontend Web Application Setup

```bash
cd frontend
npm install           # Installs React, Vite, Leaflet, Recharts, Lucide dependencies
npm run dev           # Starts Vite Development Server on http://localhost:3000
```

> Re-running `python seed.py` resets the database to the demo state. The seed includes
> donations in all three expiry states (fresh, expiring-soon, expired) and volunteers
> with live GPS pings so the proximity matcher and expiry badges are demonstrable.

---

## 🔑 Pre-Configured Demo Credentials

Use these demo accounts to log in at **[http://localhost:3000/login](http://localhost:3000/login)**:

| Role | Username | Password | Key Portal Features |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@123` | User/NGO/Donor/Volunteer management, **proximity-ranked volunteer assignment**, live tracking map, analytics dashboard, CSV report exporter, audit logs |
| **Donor** | `donor` | `Donor@123` | Post surplus food (photo upload, map pin, **prep/expiry times**), 20-min cancellation window, NGO permission grant |
| **NGO** | `ngo` | `Ngo@123` | Browse available food with **expiry badges**, FSSAI quality verification checklist, live volunteer tracking, beneficiary photo proof confirmation (`Mark as Done NGO OK`) |
| **Volunteer** | `volunteer` | `Volunteer@123` | Alex Rivera — accept assignments, enforced status workflow, HTML5 GPS broadcasting, proof upload. **Nearest volunteer in the proximity demo (~0.8 km)** |
| **Volunteer 2** | `volunteer2` | `Volunteer@123` | Priya Sharma — second volunteer with a farther live GPS ping (~1.5 km) to demonstrate ranking |
| **Volunteer 3** | `volunteer3` | `Volunteer@123` | Ravi Kumar — approved volunteer with **no location shared**, demonstrating the `NO LOCATION` handling |

---

## 🔄 End-to-End Workflow Demonstration

1. **Donor** logs in and posts surplus food with photo preview, pickup map pin, and **best-before/expiry time**.
2. **NGO** browses available food with **FRESH / EXPIRING SOON / EXPIRED** badges, completes the **FSSAI Quality Check**, and submits a food request (expired donations are blocked).
3. **Donor** reviews the NGO request and clicks **ACCEPT**.
4. **Admin** opens the assignment screen — volunteers are **ranked nearest-first by live GPS distance** — and assigns a volunteer (manual override possible).
5. **Volunteer** accepts the assignment, broadcasts live GPS position, updates delivery status (*Picked Up → Out for Delivery → Delivered* — order enforced server-side), and uploads the proof photo.
6. **NGO** verifies the delivered food proof and submits the beneficiary count (`Mark as Done NGO OK`).
7. **Admin** analytics, CSV monthly reports, and audit logs (with recorded pickup distances) update automatically.

---

## 📁 Project Structure

```
├── backend/            # Flask REST API (app factory, blueprints per role)
│   ├── app/models/     # 13 SQLAlchemy models (Donation, Request, Assignment, Delivery, ...)
│   ├── app/routes/     # auth, admin, donor, ngo, volunteer, notification, location
│   ├── app/services/   # notification + mock SMS (optional Twilio hook)
│   ├── app/utils/      # CAPTCHA, RBAC decorators, haversine geo helper, validators
│   ├── seed.py         # Demo data: 4 roles + expiry-state + proximity demo records
│   └── run.py          # Dev server entrypoint
├── frontend/           # React 18 + Vite + Tailwind SPA (role-based portals)
└── database/           # SQLite DB file + schema.sql / seed_data.sql reference
```
