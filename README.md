# RealHaven

# Real Estate Website Project

## 📌 Overview
📍 Built for San Jose – Tailored specifically to the local market

🤖 AI-Powered Chatbot – Guides users through property search naturally

🎯 Smart Filtering – Matches listings to user needs & preferences

📊 Visual Insights – Graphs help compare prices and features

🏷️ Detailed Property Views – See kitchen, living room, and more

🚀 Simplified Experience – Makes home search faster and more informed

---

# 🏡 RealHaven – AI-Powered Real Estate Platform

This guide will help you clone, set up, and run the **RealHaven** project locally on a MacBook. It includes setup instructions for both the backend (Django) and frontend (React).

## 🚀 Clone the Project

1. **Install Git and Python 3**  
Make sure Git and Python 3 are installed on your system:
```bash
git --version
python3 --version
```

2. **Clone the Repository**  
Navigate to your desired directory and clone the project:
```bash
cd ~/Documents
git clone https://github.com/zeynnepps/RealHaven
```
You may be prompted for your GitHub **username** and **password/token**.

---

## 🛠️ Set Up the Development Environment

3. **Install Visual Studio Code**
- Download and install [VS Code for macOS](https://code.visualstudio.com/)
- Install the following extensions:
  - Python
  - Jupyter
  - ES7+ React/Redux/React-Native snippets

---

## ⚙️ Backend Setup (Django + Python)

4. **Create a Virtual Environment**
```bash
python3 -m pip install virtualenv
pip3 install --upgrade pip
python3 -m venv venv  # or python3.12 -m venv venv
source venv/bin/activate
```

5. **Install Python Dependencies (inside virtualenv)**
```bash
pip install django djangorestframework pillow pandas
pip install django-cors-headers
pip install spacy            # or pip install spacy --only-binary=:all:
pip install numpy            # or pip install numpy --only-binary=:all:
pip install joblib
pip install xgboost
pip install fuzzywuzzy python-Levenshtein
```

---

## 🔧 System-Level Setup (outside virtualenv)

6. **Install Homebrew and System Packages**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"
brew install libomp
brew install node
```

7. **Update Shell Configuration**
```bash
nano ~/.zshrc
```
Add this line at the bottom if it's not already there:
```bash
export PATH="/opt/homebrew/bin:$PATH"
```
Save and exit:
- Press `Ctrl + O`, then `Enter`
- Press `Ctrl + X`

Apply the changes:
```bash
source ~/.zshrc
```

---

## 🧪 Final Backend Steps (in virtualenv)

8. **Install Remaining Package**
```bash
pip install scikit-learn
```

9. **Setup and Run Django**
```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) **Clear old data**
```bash
python manage.py shell
>>> from listings.models import Property
>>> Property.objects.all().delete()
>>> exit()
```

**Import properties**
```bash
python manage.py import_properties
```

**Run the server**
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/api/properties](http://127.0.0.1:8000/api/properties)

To stop the server: `Ctrl + C`  
To exit virtualenv: `deactivate`

---

## 🌐 Frontend Setup (React)

10. **Start the Frontend App**
```bash
cd frontend
npm install
npm start
```

Visit: [http://localhost:3000](http://localhost:3000)

---

## ✅ Done!

You're now ready to explore and develop on **RealHaven**! 🎉
