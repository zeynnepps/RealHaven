# RealHaven

#pip install django
#source venv/bin/activate  # For macOS/Linux


django-admin startproject realheaven_backend
cd realheaven_backend

python manage.py startapp listings

python manage.py migrate
