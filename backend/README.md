## project structure backend
── 📁 backend/                          # Python Flask Backend API
   ├── run.py                           # Main application entry point (Port 5000)
   ├── seed.py                          # Database seed script for demo accounts
   ├── requirements.txt                 # Python package dependencies
   ├── .env                             # Environment configuration
   ├── .gitignore                       # Git ignore rules
   ├── 📁 uploads/                      # Uploaded files storage
   │   ├── 📁 food/                    # Surplus food images
   │   ├── 📁 delivery/                # Volunteer delivery proof images
   │   └── 📁 beneficiaries/           # Beneficiary proof photos
   └── 📁 app/                          # Flask Application Package
       ├── __init__.py                  # Flask Application Factory
       ├── config.py                    # Environment & Database config
       ├── extensions.py                # Extensions (db, jwt, cors)
       ├── 📁 models/                   # SQLAlchemy Database Models
       │   ├── user.py                  # User authentication model
       │   ├── donor.py                 # Donor profile model
       │   ├── ngo.py                   # NGO shelter model
       │   ├── volunteer.py             # Volunteer profile model
       │   ├── donation.py              # Food donation model
       │   ├── request.py               # NGO food request model
       │   ├── assignment.py            # Volunteer assignment model
       │   ├── delivery.py              # Delivery workflow & proof model
       │   ├── location.py              # GPS location model
       │   ├── notification.py          # Notification model
       │   ├── report.py                # Monthly report model
       │   ├── payment.py               # Mock payment model
       │   └── log.py                   # System audit action log model
       ├── 📁 routes/                   # REST API Blueprints
       │   ├── auth.py                  # Login, Register, CAPTCHA, /me
       │   ├── admin.py                 # Admin management & analytics
       │   ├── donor.py                 # Post surplus food & 20-min cancel
       │   ├── ngo.py                   # Request food & Quality check
       │   ├── volunteer.py             # Accept task & Geolocation tracking
       │   ├── notification.py          # Notification endpoints
       │   └── location.py              # Live GPS coordinates endpoint
       ├── 📁 services/                 # Business Logic Services
       │   ├── auth_service.py
       │   ├── donation_service.py
       │   ├── request_service.py
       │   ├── sms_service.py           # Mock SMS dispatcher (Twilio supported)
       │   ├── notification_service.py
       │   └── location_service.py
       └── 📁 utils/                    # Helper Utilities
           ├── captcha.py               # Visual CAPTCHA challenge generator
           ├── decorators.py            # Role & Approval decorators
           ├── logger.py                # Action logging utility
           └── validators.py            # Form validation helpers

