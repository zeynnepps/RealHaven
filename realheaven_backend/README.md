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

python manage.py shell
from listings.models import Property
Property.objects.all().delete()
exit()

#import new dataset
python manage.py import_properties

