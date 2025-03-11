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



#delete old data and update new dataset

1.python manage.py shell
2.from listings.models import Property
3.Property.objects.all().delete()
4.exit()

#import new dataset
python manage.py import_properties

