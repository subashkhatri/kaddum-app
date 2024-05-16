# Kaddum App
# Before you run the application
pip install django python-decouple psycopg2-binary pillow

# create and activate env file
# create together with readme file  
python -m venv projectenv   
projectenv\Scripts\activate 

# To run requirements txt file
pip install -r requirements.txt

# Run PgAdmin4, delete existing database and create a new database named: kaddum-app


# Make migrations
python manage.py makemigrations dashboard users

# Migrate to database
python manage.py migrate

# Add Seeds to database: projects, resource cost and useraccount
python manage.py seed_project
python manage.py seed_resource_cost
python manage.py seed_useraccount

# Create superuser
python manage.py createsuperuser
*Username: KD0025
*First name: admin
*Last name: admin
*Email: admin@gmail.com
*Is indigenous: False
*Is local: False
*Roles: super admin
*Password: admin

# Run Kaddum-app
python manage.py runserver




