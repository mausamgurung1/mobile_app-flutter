# PostgreSQL Setup Guide

The application has been configured to use PostgreSQL by default. Follow these steps to set up PostgreSQL:

## 1. Install PostgreSQL

### macOS
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Windows
Download and install from: https://www.postgresql.org/download/windows/

## 2. Create Database and User

Connect to PostgreSQL:
```bash
psql postgres
```

Then run:
```sql
CREATE DATABASE nutrition_db;
CREATE USER nutrition_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE nutrition_db TO nutrition_user;
\q
```

## 3. Configure Environment Variables

Create a `.env` file in the `backend` directory with your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://nutrition_user:your_password_here@localhost:5432/nutrition_db
```

**Format**: `postgresql://username:password@host:port/database_name`

## 4. Install Dependencies

The PostgreSQL driver (`psycopg2-binary`) is already in `requirements.txt`. Install it:

```bash
cd backend
source venv/bin/activate  # or activate your virtual environment
pip install -r requirements.txt
```

## 5. Run Database Migrations

Initialize and run Alembic migrations:

```bash
cd backend
alembic upgrade head
```

This will create all the necessary tables in your PostgreSQL database.

## 6. Start the Application

```bash
python main.py
```

Or:
```bash
uvicorn main:app --reload
```

## Verification

The application will automatically:
- Use PostgreSQL if `DATABASE_URL` starts with `postgresql://`
- Use SQLite if `DATABASE_URL` starts with `sqlite://`

Check your database:
```bash
psql -U nutrition_user -d nutrition_db
\dt  # List all tables
```

## Troubleshooting

### Connection Error
- Verify PostgreSQL is running: `brew services list` (macOS) or `sudo systemctl status postgresql` (Linux)
- Check your connection string format
- Verify database and user exist

### Permission Error
- Ensure the user has proper privileges on the database
- Check PostgreSQL authentication settings in `pg_hba.conf`

### Migration Issues
- Make sure the database exists before running migrations
- Check that the user has CREATE TABLE permissions

