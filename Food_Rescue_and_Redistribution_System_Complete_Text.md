# Food Rescue and Redistribution System
## Complete Text Extraction and Structured Transcription

---

# Slide 1 — Title

**Food Rescue and Redistribution System**  
Final Year Engineering Project

**Team: Equality Engine**

Sharveshwar (2024115002) | Elavarasi (2024115096) | Bharathikannan (2024115026)

---

# Slide 2 — Problem Statement

## Problem Identification & Existing Challenges

### The Challenge

**Daily Food Wastage**  
Hotels, restaurants, marriage halls, and college messes generate edible surplus food that is routinely discarded.

**Inefficient Coordination**  
Existing donation methods rely on phone calls, messaging groups, or personal contacts — slow and unreliable.

**Food Insecurity**  
Safe, consumable food is wasted while shelters and underprivileged communities face hunger every day.

### Root Causes
- Manual communication
- No centralized coordination
- No expiry monitoring
- Limited safety validation
- No delivery tracking
- No data management

---

# Slide 3 — Our Solution

## Proposed Solution & Project Objectives

A centralized web-based platform enabling:
- Verified food donation
- Efficient coordination
- Food safety tracking
- Delivery verification
- Impact reporting

### Process / Flow
Donor Posts → Admin Verifies → NGO & Delivery → Impact Reports

### Verified Registration
Enable verified donor registration and real-time NGO food requests with matching.

### Automated Logistics
Automate volunteer assignment, delivery tracking, and food safety compliance with expiry validation.

### Impact Analytics
Provide delivery proof, receiver confirmation, and generate analytics to measure food wastage reduction.

---

# Slide 4 — Stakeholders

## Stakeholders & Policy Alignment

### Key Stakeholders

**01 — Food Donors**  
Hotels, restaurants, marriage halls, college messes, event organizers.

**02 — NGOs / Shelters**  
Request and receive donated food for beneficiaries.

**03 — Volunteers**  
Collect and deliver food between donors and NGOs.

**04 — Administrator**  
Verify users, monitor donations, generate reports.

**05 — Government & FSSAI**  
Ensure food safety compliance and traceability.

### Policy & SDG Alignment

**SDG 2 — Zero Hunger**  
Redistribute edible surplus food to reduce hunger.

**SDG 12 — Responsible Consumption**  
Minimize food wastage and promote sustainability.

**SDG 17 — Partnerships**  
Collaborate across donors, NGOs, volunteers, and government.

**FSSAI / NISP 2019**  
Maintains food safety standards and encourages student innovation.

---

# Slide 5 — Modules

## Functional Modules Overview

### Donor Module
- **SDG Goal:** SDG 12
- **Objective:** Register & post food donations
- **Deliverable:** Donation listings with images
- **Stakeholder:** Food Donors

### NGO Module
- **SDG Goal:** SDG 2
- **Objective:** View & request available food
- **Deliverable:** Food requests & confirmations
- **Stakeholder:** NGOs / Shelters

### Volunteer Module
- **SDG Goal:** SDG 17
- **Objective:** Accept & execute deliveries
- **Deliverable:** Delivery proof & tracking
- **Stakeholder:** Volunteers

### Admin Module
- **SDG Goal:** SDG 2, 12, 17
- **Objective:** Verify & manage system
- **Deliverable:** Reports & analytics
- **Stakeholder:** Administrator

---

# Slide 6 — Bird's Eye View Architecture

## Food Rescue and Redistribution System

### 1. Presentation Layer
**Web Portals (User Interfaces)**

#### Donor Portal
- Register / Login
- Post Donations
- Track Donations

#### NGO Portal
- View Donations
- Request Food
- Track Requests

#### Volunteer Portal
- View Assignments
- Pickup & Delivery
- Upload Proof

#### Admin Portal
- User Verification
- Monitor System
- Generate Reports

### 2. Application / Business Logic Layer
**Core Services & Business Logic**

#### Authentication Service
- User Registration
- Login/Logout
- RBAC

#### Donation Management
- Create Donation
- Validate Food Info
- Expiry Tracking

#### Request Management
- NGO Requests
- Request Status
- Approval/Rejection

#### Volunteer Management
- Availability Tracking
- Assignment Engine
- Nearest Match

#### Delivery Management
- Pickup Tracking
- Delivery Tracking
- Proof/Confirm

#### Reporting & Analytics
- Impact Reports
- Dashboard
- Alerts & Insights

### 3. Data Access Layer
**APIs & Data Abstraction**

**RESTful API Gateway — Secure Communication / HTTPS**

### 4. Data Layer
**Database & Persistent Storage**

**SQLite Database**
- Users
- Donors
- NGOs
- Volunteers
- Donations
- Requests
- Assignments
- Deliveries
- Reports
- Logs

### 5. External Integrations
**Third Party Services (If Needed)**
- Email Service — Notifications
- SMS Service — Alert Messages
- Map Service — Location & Routing
- Cloud Storage — Images / Proofs

### Security & Cross-Cutting Concerns
- **AUTH:** Authentication & Authorization
- **DV:** Data Validation & Sanitization
- **LOG:** Audit Logs & Monitoring
- **BKP:** Backup & Recovery
- **SSL:** HTTPS / SSL Encryption

Legend:
- → Data Flow
- ↔ Two Way Interaction
- ⇢ Security / Monitoring

---

# Slide 7 — Overall System Architecture

## Architecture

The system is built using a **Three-Tier Architecture**, ensuring:
- Separation of concerns
- Scalability
- Security
- Maintainability

### Goal
Connect food donors with NGOs through efficient verification, smart volunteer assignment, and real-time tracking.

## Three-Tier Architecture

### Presentation Layer (Frontend)
- Donor Portal
- NGO Portal
- Volunteer Portal
- Admin Portal

User interfaces built with **React.js and Tailwind**.

### Application Layer (Backend)
- Authentication & User Management
- Donation Management
- NGO Food Verification
- Volunteer Assignment
- Notification & Tracking
- Reporting & Analytics

Built with **Python (Flask/FastAPI)**.

### Data Layer (Database)
- User Data
- Donation & Food Data
- Images (Food Photos)
- Geospatial Location Data
- Delivery & Tracking Data
- Reports & Logs

Database: **SQLite with Spatial Extension**

## Tech Stack
- **Frontend:** React.js / Tailwind CSS
- **Backend:** Python (Flask / FastAPI)
- **Database:** SQLite (Geospatial Ext.)

## System Workflow (High Level)

### 1. Donor Uploads Food
Donor registers and uploads food details, including images and location.

### 2. Admin Verification
Admin verifies the donation for food safety, compliance, and authenticity.

### 3. NGO Review
Verified donations are displayed to nearby NGOs. NGO can accept or reject the food.

### 4. Volunteer Assignment
System assigns the nearest available volunteer using a **Proximity Matcher** based on geospatial location data.

### 5. Delivery & Impact
Volunteer delivers the food. NGO confirms receipt. Admin generates impact reports and system analytics.

## Key Features
- **Proximity Matcher:** Nearest volunteer
- **Geospatial Data:** Location in SQLite
- **Image Storage:** Donor uploads
- **NGO Decision:** Accept / Reject
- **Real-time Tracking:** Donations & deliveries

---

# Slide 8 — Data Flow

## Data Flow Diagram (DFD)

**Donor Portal**  
submits → **Food Donation Data**

**Processing Layer**  
performs → **Food Verification**

**Decision Layer**  
handles → **NGO Matching and Volunteer Assignment**

**Volunteer Portal**  
executes → **Delivery Tracking and Proof Upload**

**Admin Dashboard**  
receives → **Confirmation and generates Analytics and Reports**

Data flows sequentially from left to right through each processing stage.

## Key Data Entities

### Users
Donors, NGOs, Volunteers, Admins — each with role-based access privileges.

### Donations
Food items with metadata:
- Type
- Quantity
- Expiry time
- Pickup location

### Requests
NGO food requests with acceptance status and matching logic.

### Deliveries
Volunteer assignments with real-time delivery tracking and proof upload.

### Analytics
Aggregated metrics for:
- Food saved
- Meals donated
- Social impact reporting

---

# Slide 9 — Donor Module Algorithm

## Donor Module

Enables donors to securely share food details and images. The system stores the donation and notifies nearby NGOs for quick action.

### Input
- Donor credentials (email/phone)
- Food details (type, quantity, expiry date)
- Food image
- Pickup location
- Additional notes (optional)

### Output
- Donation posted successfully
- Stored in SQLite Database
- NGOs notified about new donation

### Algorithm
1. Authenticate donor using email/phone and password.
2. Capture and enter food details including expiry and location.
3. Upload food image and validate file type and size.
4. Validate all inputs for completeness and correctness.
5. Store donation record and image path in SQLite Database.
6. Notify nearby NGOs about the new donation.

### Deliverables
- Verified donation record in database
- Food image stored securely
- NGOs receive real-time notification
- Unique Donation ID generated

### Flow
Donor → Login / Register → Enter Food Details → Upload Food Image → Submit Donation → SQLite Database → Notify NGOs → Donation Posted

---

# Slide 10 — Admin Module Algorithm

## Admin Module

Provides administrators with complete control to:
- Manage users
- Monitor donations
- Assign volunteers
- Generate insightful reports
- Ensure efficient system operations

### Input
- Admin credentials
- User details and role information
- Donation records and status
- Volunteer availability and location
- System activity logs

### Output
- Users managed successfully
- Volunteers assigned to tasks
- Reports generated
- Analytics dashboard updated
- System monitored and secured

### Algorithm
1. Authenticate admin using secure login.
2. Manage users: create, update, activate/deactivate, and assign roles.
3. Monitor donations: review, verify, and track donation status.
4. Assign nearest volunteers based on location and availability.
5. Generate reports and analytics from system data.
6. Update dashboard and system monitoring in real time.

### Deliverables
- User management and role control
- Volunteer assignment records
- Donation monitoring & verification
- Reports and analytics dashboard
- System monitoring and audit logs
- RBAC enforced across the system

### Flow
Admin → Login → Manage Users → Monitor Donations → Assign Volunteers → Generate Reports → Analytics Dashboard → SQLite Database → Operations Managed Successfully

---

# Slide 11 — NGO Module Algorithm

## NGO Module

Enables NGOs to:
- Discover available donations
- Verify food quality
- Create requests
- Ensure help reaches those in need

### Input
- NGO login credentials
- Active food donations
- Food details and images
- Donor information
- Beneficiary requirements
- Request details (pickup, quantity)

### Output
- Donation accepted or rejected
- Food request generated
- Donor and Admin notified
- Request status updated
- Record stored in database

### Algorithm
1. Authenticate NGO using secure login.
2. View active food donations with filters and sorting.
3. Verify food quality, quantity, and expiry details.
4. Accept or reject the donation based on suitability.
5. If accepted, generate a food request with required details.
6. Update request status in SQLite database.
7. Notify donor and admin about the decision.

### Deliverables
- Food request created
- Acceptance / Rejection status
- Database updated
- Donor & Admin notifications
- Request ID generated
- Transparent tracking

### Flow
NGO → Login → View Active Donations → Verify Food Quality → Accept Donation? (Yes / No) → Generate Request → SQLite Database → Notify Donor & Admin → Completed

---

# Slide 12 — Volunteer Module Algorithm

## Volunteer Module

Enables volunteers to:
- Accept assignments
- Pick up food from donors
- Deliver food to NGOs
- Upload proof
- Ensure transparency and trust

### Input
- Volunteer login credentials
- Assigned task details
- Pickup (donor) location
- Drop-off (NGO) location
- Delivery proof image
- Delivery status updates

### Output
- Food delivered successfully
- Delivery proof uploaded
- Delivery status updated
- Confirmation to NGO, Donor and Admin
- Record stored in database

### Algorithm
1. Authenticate volunteer using secure login.
2. View and accept assigned delivery task.
3. Navigate to donor location and pick up the food.
4. Deliver the food to the NGO.
5. Capture and upload delivery proof (photo).
6. Update delivery status as “Delivered”.
7. System stores the record and notifies NGO, Donor, and Admin.

### Deliverables
- Successful food delivery
- Proof image stored
- Delivery record in database
- Status confirmation
- Notifications to all stakeholders
- Volunteer performance tracking

### Flow
Volunteer → Login → Accept Assigned Task → Pickup Food from Donor → Deliver Food to NGO → Upload Delivery Proof → Update Delivery Status → Delivery Database → Notify NGO, Donor & Admin → Task Completed

---

# Slide 13 — Module Architectures & Algorithms

## Donor Module
- **Authentication:** Secure login with email/phone verification
- **CRUD Operations:** Create, read, update, delete donation records
- **Image Upload:** Validate and store food images for quality assessment

## NGO Module
- **Food Discovery:** View verified donations with filtering and sorting
- **Request Management:** Submit and track food requests
- **Delivery Confirmation:** Confirm receipt and provide feedback

## Volunteer Module
- **Task Assignment:** Receive pickup and delivery assignments
- **Delivery Tracking:** Real-time location and status updates
- **Proof Upload:** Capture and upload delivery proof images

## Admin Module
- **Manual Verification:** Review and approve food donations
- **Expiry Validation:** Monitor and flag expiring donations
- **Volunteer Assignment:** Proximity-based nearest volunteer algorithm
- **RBAC:** Role-Based Access Control for all user roles

---

# Slide 14 — Data

## Dataset Used

The system uses a well-structured relational database to manage:
- Users
- Donations
- Requests
- Assignments
- Deliveries
- Reporting

## Dataset Attributes

### Food Donation Dataset
- Food type
- Quantity
- Preparation time
- Expire time
- Pickup location
- Food image
- Donor ID
- Verification status

### User Dataset
- User ID
- Name
- Email
- Phone
- Role (Donor/NGO/Volunteer/Admin)
- Address
- Verification status
- Registration date

### Logistics Dataset
- Delivery ID
- Volunteer ID
- Donation ID
- Pickup time
- Delivery time
- Delivery status
- Proof image
- Confirmation timestamp

## Key Highlights
- All datasets are structured to support Role-Based Access Control (RBAC).
- Expiry validation ensures only safe and usable food is delivered.
- Geospatial location data is stored in the database to enable proximity matching for nearby volunteers.

## Database Schema

### USERS
- user_id — INT PK
- name — STR
- email — STR
- phone — STR
- role — STR
- status — STR

### NGOS
- ngo_id — INT PK
- user_id — INT FK

### VOLUNTEERS
- volunteer_id — INT PK
- user_id — INT FK
- availability — STR

### ASSIGNMENTS
- assignment_id — INT PK
- volunteer_id — INT FK
- request_id — INT FK
- status — STR

### DONORS
- donor_id — INT PK
- user_id — INT FK

### DONATIONS
- donation_id — INT PK
- donor_id — INT FK
- food_name — STR
- quantity — INT
- prep_time — DT
- expiry_time — DT
- image — STR
- location — STR
- status — STR

### REQUESTS
- request_id — INT PK
- ngo_id — INT FK
- donation_id — INT FK
- request_status — STR

### DELIVERIES
- delivery_id — INT PK
- assignment_id — INT FK
- pickup_time — DT
- delivery_time — DT
- proof_image — STR

### LOGS
- log_id — INT PK
- action — STR
- timestamp — DT

### REPORTS
- report_id — INT PK
- month — STR
- donations — INT
- deliveries — INT
- beneficiaries — INT

## Schema Benefits
- Maintains data integrity
- Enables proximity matching
- Supports end-to-end traceability
- Keeps audit logs

---

# Slide 15 — Database Schema & ER Diagram

## Database

### Users
- **Primary Key:** user_id
- **Key Attributes:** name, email, phone, role, address, verified

### Donations
- **Primary Key:** donation_id
- **Key Attributes:** donor_id (FK), food_type, quantity, prep_time, expiry_time, location, image_url, verified

### Requests
- **Primary Key:** request_id
- **Key Attributes:** ngo_id (FK), donation_id (FK), status, request_date

### Deliveries
- **Primary Key:** delivery_id
- **Key Attributes:** volunteer_id (FK), request_id (FK), pickup_time, delivery_time, status, proof_image

### Analytics
- **Primary Key:** analytics_id
- **Key Attributes:** total_donations, completed_deliveries, beneficiaries_served, food_saved_kg

## Entity Relationships
- **Users → Donations:** One donor can post many donations.
- **Donations → Requests:** One donation can receive many requests.
- **Requests → Deliveries:** Each request maps to one delivery.
- **Users → Deliveries:** One volunteer executes many deliveries.

## ER Diagram Details Visible in the Slide

### Donors
- donor_id (PK)
- user_id (FK)

Relationship:
- Users ↔ Donors: one-to-one
- Donors → Donations: one-to-many

### Users
- user_id (PK)
- name
- email
- phone
- password
- role
- status

### NGOs
- ngo_id (PK)
- user_id (FK)

Relationship:
- Users ↔ NGOs: one-to-one
- NGOs → Requests: one-to-many

### Volunteers
- volunteer_id (PK)
- user_id (FK)
- availability

Relationship:
- Users ↔ Volunteers: one-to-one
- Volunteers → Assignments: one-to-many

### Donations
- donation_id (PK)
- donor_id (FK)
- food_name
- quantity
- preparation_time
- expiry_time
- image
- location
- status

Relationship:
- Donations → Requests: one-to-many

### Requests
- request_id (PK)
- ngo_id (FK)
- donation_id (FK)
- request_status
- request_date

Relationship:
- Requests → Assignments: one-to-one

### Assignments
- assignment_id (PK)
- volunteer_id (FK)
- request_id (FK)
- assignment_status

Relationship:
- Assignments → Deliveries: one-to-one

### Deliveries
- delivery_id (PK)
- assignment_id (FK)
- pickup_time
- delivery_time
- proof_image

### Reports
- report_id (PK)
- month
- donations
- deliveries
- beneficiaries

### Logs
- log_id (PK)
- action
- timestamp

### Relationship Summary
- One User can be one Donor, one NGO, or one Volunteer.
- One Donor can make many Donations.
- One NGO can create many Requests.
- One Donation can be requested multiple times.
- One Request generates one Assignment.
- One Volunteer can have many Assignments.
- One Assignment results in one Delivery.
- Reports summarize donations, deliveries, and beneficiaries.
- Logs record all system activities.

Cardinality Legend:
- 1 = One
- N = Many
- 1:N = One to Many
- 1:1 = One to One

---

# Slide 16 — User Interface & Dashboards

## UI Design

**User Interface & Dashboards**

Clean, intuitive, and role-based dashboards for all users to manage food donations and deliveries efficiently.

## Donor Portal
- Post new food donations with image upload
- Track donation status and pickup history
- View impact metrics and recent activity

Visible dashboard elements include:
- Welcome screen
- Food name
- Category
- Quantity
- Preparation time
- Pickup address
- Image upload
- Submit donation button
- Recent donations table
- Donation status

The dashboard also contains the message:
**“Share food. Spread hope. Your donation can feed many and reduce food waste.”**

## NGO Portal
- Browse verified donations with smart filters
- Submit food requests and track live status
- Confirm food receipt and provide feedback

Visible dashboard elements include:
- Operations and quick statistics
- Rescued food
- Families served
- Active volunteers
- Estimated food waste diverted
- Pending food requests
- Recent deliveries
- Operations hub chart

## Volunteer Portal
- View assigned pickup and delivery tasks
- Navigate to donor and NGO locations
- Upload delivery proof and mark completion

Visible dashboard elements include:
- Assigned tasks
- Pending tasks
- Completed tasks
- Pickup task details
- Delivery task details
- Task summary
- Upload proof button

## Admin Portal
- Verify users, donations and deliveries
- Monitor system metrics and KPIs
- Generate reports and manage system settings

Visible dashboard elements include:
- Total users
- Partner NGOs
- Active volunteers
- Total donations
- Total deliveries
- Food saved
- Donation trend chart
- Recent system alerts
- System actions such as:
  - Manage Users
  - Manage NGOs
  - Manage Donations
  - Assign Volunteers
  - Reports & Analytics
  - System Settings

### Goal
Build a transparent, efficient, and scalable food donation management system that connects donors, NGOs, volunteers, and communities.

### Impact
Reducing food waste and fighting hunger together.

---

# Slide 17 — Timeline

## Project Timeline & Gantt Chart (12 Weeks)

The project is planned over 12 weeks, with tasks scheduled in a logical sequence to ensure timely delivery and deployment.

### Weeks
W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12

### Tasks
- Requirement Analysis
- Survey
- UI Design
- Database Design
- Backend Development
- Frontend Development
- Integration
- Testing
- Documentation
- Final Deployment
- Go Live

### Goal
Deliver a secure, reliable, and scalable Food Donation Management System within 12 weeks.

### Duration
12 Weeks (W1 – W12)

---

# Slide 18 — Team Contributions

## Contribution

### Team Contributions

Our team collaborates to design and develop a Food Rescue and Redistribution System, leveraging our individual strengths to build a secure, scalable, and impactful solution.

## Bharathikannan — Database Works

### Key Contributions
- Designing the database schema and ER model
- Creating and managing all database tables and relationships in SQLite
- Implementing data integrity, constraints, and indexing
- Handling data storage for donations, users, requests, deliveries, and logs
- Optimizing queries for better performance and reporting

## Sharveshwar — Backend Development

### Key Contributions
- Developing RESTful APIs using Python (FastAPI/Flask)
- Building core modules:
  - Authentication
  - Donation management
  - Request handling
  - Volunteer assignment
  - Delivery tracking
- Integrating location-based logic for nearest volunteer assignment
- Implementing role-based access and business logic
- Ensuring API security, validation, and error handling

## Elavarasi — Frontend Development

### Key Contributions
- Designing and developing the user interface using React.js and Tailwind CSS
- Building responsive pages for:
  - Donor Portal
  - NGO Portal
  - Volunteer Portal
  - Admin Portal
- Implementing forms, dashboards, tables, charts, and real-time status updates
- Integrating frontend with backend APIs
- Enhancing UI/UX for a clean, intuitive, and user-friendly experience

### Team Goal
Together, we aim to build a secure, scalable, and impactful platform to reduce food waste and support communities in need.

### Overall Goal
Build a transparent, efficient, and scalable system that connects donors, NGOs, volunteers, and communities.
