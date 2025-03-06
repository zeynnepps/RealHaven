# RealHaven
pip install virtualenv
python -m venv env
source env/bin/activate


pip install django
source venv/bin/activate  # For macOS/Linux



python manage.py migrate

python manage.py runserver


python manage.py makemigrations
python manage.py migrate

#command to import dataset
python manage.py import_properties

pip install djangorestframework

