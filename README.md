# Capstone Project - Car Dealership Review Platform

[![Django CI/CD](https://github.com/exorcisthb/capstone-car-dealership/actions/workflows/django-ci-cd.yml/badge.svg)](https://github.com/exorcisthb/capstone-car-dealership/actions/workflows/django-ci-cd.yml)

## Project Name
**Car Dealership Review Platform**

## Project Description
A full-stack web application that allows users to:
- Browse car dealerships across multiple US states
- Filter dealerships by state
- Read customer reviews for each dealership
- Sign up and post their own reviews
- Get automatic sentiment analysis (positive/negative/neutral) on reviews

## Tech Stack
- **Backend:** Python 3.11, Django 4.2, Django REST Framework
- **Frontend:** React 18, HTML5, CSS3, JavaScript
- **Database:** SQLite (development) / PostgreSQL (production)
- **Deployment:** Heroku / Render / Railway (configurable via `Procfile` & `runtime.txt`)
- **CI/CD:** GitHub Actions (see `.github/workflows/django-ci-cd.yml`)

## Project Structure
```
ABC/
├── README.md
├── .github/workflows/django-ci-cd.yml   # GitHub Actions CI/CD
└── server/
    ├── manage.py
    ├── requirements.txt
    ├── Procfile                          # Heroku/Render deployment
    ├── runtime.txt                       # Python version
    ├── djangoproject/                    # Django project settings
    └── djangoapp/                        # Main Django app
        ├── models.py                     # Dealer, Review, CarMake, CarModel
        ├── views.py                      # Page + REST API views
        ├── sentiment.py                  # Sentiment analysis engine
        ├── urls.py                       # API routes
        ├── admin.py                      # Django admin registration
        └── management/commands/seed_data.py   # DB seeding command
```

## Local Setup

```bash
cd server
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

## Default Test Credentials
- **Root admin:** username `root`, password `rootpass123` (created by `seed_data`)
- **Test user:** username `testuser`, password `TestPass123`

## REST API Endpoints

| Method | Endpoint                                | Description                       |
|--------|----------------------------------------|-----------------------------------|
| POST   | /djangoapp/login                       | Login (JSON: userName, password)  |
| POST   | /djangoapp/logout                      | Logout current user               |
| POST   | /djangoapp/register                    | Register new user                 |
| GET    | /djangoapp/dealers                     | List all dealers                  |
| GET    | /djangoapp/dealers?state=KS            | List dealers in a state           |
| GET    | /djangoapp/dealer/<id>                 | Get one dealer                    |
| GET    | /djangoapp/dealers/state/<state>       | Dealers in a state                |
| GET    | /djangoapp/reviews/dealer/<id>         | Reviews for a dealer              |
| POST   | /djangoapp/reviews/add                 | Add a review (login required)     |
| GET    | /djangoapp/carmakes                    | All car makes with models         |
| GET    | /djangoapp/analyze?text=...            | Analyze sentiment of text         |
| GET    | /                                      | Home page (dealer list)           |
| GET    | /djangoapp/about/                      | About Us page                     |
| GET    | /djangoapp/contact/                    | Contact Us page                   |
| GET    | /djangoapp/dealer/<id>/                | Dealer detail + reviews page      |
| GET    | /admin/                                | Django admin                      |

## License
This project is for educational purposes as part of the IBM Full Stack Developer Capstone.
