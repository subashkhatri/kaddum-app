# Configuration variables
$DB_NAME = '[Your DB Name]'
$DB_USER = '[Your DB User]'
$DB_PASSWORD ='[Your DB password]'

# Django project directory
$DJANGO_DIR = "kaddumapp/dashboard"


Write-Host "Resetting the database: $DB_NAME"

# Drop the current database
Write-Host "Dropping the database..."
psql -U $DB_USER -h localhost -c "DROP DATABASE IF EXISTS $DB_NAME;"

# Create a new database
Write-Host "Creating a new database..."
psql -U $DB_USER -h localhost -c "CREATE DATABASE $DB_NAME;"

# Navigate to Django project directory
Set-Location -Path $DJANGO_DIR

# Remove migration files
Write-Host "Removing old migration files..."
Get-ChildItem -Path .\migrations\*.py -Recurse | Remove-Item
Get-ChildItem -Path .\migrations\*.pyc -Recurse | Remove-Item

# Create new migrations
Write-Host "Creating new migrations..."
python manage.py makemigrations users dashboard

# Apply migrations
Write-Host "Applying migrations..."
python manage.py migrate

# Seed the database
Write-Host "Seeding the database..."
python manage.py seed_project
python manage.py seed_resource_cost
python manage.py seed_useraccount
python manage.py seed_dairy_records
python manage.py seed_cost_tracking
python manage.py seed_daily_tracking
python manage.py seed_day_tracking_emp_details
python manage.py seed_day_tracking_resource_details

Write-Host "Database reset and seeded successfully!"

# Create Weekly Report View
python manage.py create_view_weekly_report