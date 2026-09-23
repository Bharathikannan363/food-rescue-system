## project structure backendbackend

├── run.py               # Main entry point (Port 5000)
├── seed.py              # Demo accounts seeding
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── .gitignore           # Git ignore rules
├── uploads/             # File storage
│   ├── food/            # Surplus food images
│   ├── delivery/        # Volunteer delivery proof
│   └── beneficiaries/   # Beneficiary proof photos
└── app/                 # Flask Application
├── init.py              # App factory
├── config.py            # Config (env, DB)
├── extensions.py        # db, jwt, cors
├── models/              # SQLAlchemy models
├── routes/              # REST API blueprints
├── services/            # Business logic
└── utils/               # Helpers (captcha, logger, validators)
