## project structure backendbackend

backend/
├── run.py
├── seed.py
├── requirements.txt
├── .env
├── .gitignore
├── uploads/
│   ├── food/
│   ├── delivery/
│   └── beneficiaries/
└── app/
    ├── __init__.py
    ├── config.py
    ├── extensions.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── donor.py
    │   ├── ngo.py
    │   ├── volunteer.py
    │   ├── donation.py
    │   ├── request.py
    │   ├── assignment.py
    │   ├── delivery.py
    │   ├── location.py
    │   ├── notification.py
    │   ├── report.py
    │   └── log.py
    ├── routes/
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── admin.py
    │   ├── donor.py
    │   ├── ngo.py
    │   ├── volunteer.py
    │   ├── notification.py
    │   └── location.py
    ├── services/
    │   ├── auth_service.py
    │   ├── donation_service.py
    │   ├── request_service.py
    │   ├── assignment_service.py
    │   ├── delivery_service.py
    │   ├── notification_service.py
    │   ├── sms_service.py
    │   ├── location_service.py
    │   └── report_service.py
    └── utils/
        ├── decorators.py
        ├── captcha.py
        ├── validators.py
        ├── logger.py
        └── helpers.py
