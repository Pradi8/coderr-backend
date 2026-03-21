# Coderr API

## Overview
Coderr API is a **Django REST Framework project** for a freelance developer platform that connects clients and developers, enabling project management and communication.  
It uses **Token Authentication** for secure access and supports a browsable API for development and testing.

---

## Features
- User registration, login, and logout
- CRUD operations for **Offers** , **Orders** and **Reviews**
- Reviews system for oders, offers
- Object-level permissions:
  - Only authors can edit their reviews
  - Only admins or authors can delete reviews
- Token-based authentication
- Browsable API for development

---

# Installation
## Follow these steps to set up the project locally:

## Requirements: Python 3.14.

## 1. Clone the repository
  git clone https://github.com/Pradi8/coderr-backend.git <br>       
  cd coderr-backend

## 2. Create a virtual environment
  ```bash 
    python -m venv env
  ```

## 3. Activate the virtual environment
### <b>Linux/Mac</b>
```bash
  env/bin/activate  
```
### <b>Windows</b>
```bash
  env\Scripts\activate      
```

## 4. Install Python dependencies
```bash
  pip install -r requirements.txt
```

## 5. Create database migrations
```bash
  python manage.py makemigrations
```

## 6. Apply database migrations
```bash
  python manage.py migrate
```

## 7. Create a superuser (admin account)
```bash
  python manage.py createsuperuser
```

## 8. Start the development server
```bash
  python manage.py runserver  
```
  The project will be running at http://127.0.0.1:8000/


# Project Structure
## coderr_app/
├── models.py        # Offer, Offerdetails <br>
├── views.py         # API views  <br>
├── paginations.py   # API paginations  <br>
├── filters.py       # DRF filters  <br>
├── serializers.py   # DRF serializers  <br>
├── urls.py

## auth_app/
├── models.py        # Customuser, Fileupload  <br>
├── views.py         # Registration, login, logout  <br>
├── serializers.py   # DRF serializers  <br>
├── urls.py  <br>
├── permissions.py   # Custom permissions

manage.py
requirements.txt
README.md