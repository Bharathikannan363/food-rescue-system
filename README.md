# Database structure
```text
database/
├── schema.sql       # Creates all database tables
├── seed_data.sql    # Inserts sample data
└── README.md        # Database documentation
```

### Tables

| Table                 | Purpose                                                         |
| `users`               | Stores user accounts, login details, roles, and approval status |
| `donors`              | Stores donor details and locations                              |
| `ngos`                | Stores NGO details, registration information, and locations     |
| `volunteers`          | Stores volunteer details, vehicles, availability, and locations |
| `donations`           | Stores food donation information                                |
| `requests`            | Stores NGO requests for food donations                          |
| `assignments`         | Assigns volunteers to donation requests                         |
| `deliveries`          | Stores pickup and delivery information                          |
| `volunteer_locations` | Stores volunteer location tracking data                         |
| `notifications`       | Stores notifications sent to users                              |
| `reports`             | Stores monthly food rescue statistics                           |
| `logs`                | Stores system activity and audit logs                           |
