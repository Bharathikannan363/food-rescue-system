# Food Rescue Database Layer

This directory manages the SQLite database file (`food_rescue.db`), DDL schemas (`schema.sql`), and initial data seeds (`seed_data.sql`).

## Automatic Initialization

The database is managed via Python Flask-SQLAlchemy.
To seed or re-initialize the database with demo accounts:

```bash
cd backend
python seed.py
```
