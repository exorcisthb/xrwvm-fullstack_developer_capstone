"""
URL configuration for the djangoapp (REST API + page routes).
"""
from django.urls import path
from . import views

urlpatterns = [
    # Page routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dealer/<int:dealer_id>/', views.dealer_detail, name='dealer_detail'),

    # Auth
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.register_user, name='register_user'),

    # Dealer APIs
    path('dealers', views.get_dealers, name='get_dealers'),
    path('fetchDealers', views.get_dealers, name='fetch_dealers'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_by_id, name='fetch_dealer_by_id'),
    path('dealers/state/<str:state>', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('fetchDealers/<str:state>', views.get_dealers_by_state, name='fetch_dealers_by_state'),

    # Review APIs
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='fetch_dealer_reviews'),
    path('reviews/add', views.add_review, name='add_review'),

    # Car APIs (two endpoints that return the same data with different keys)
    path('carmakes', views.get_all_car_makes, name='get_all_car_makes'),
    path('get_cars', views.get_cars, name='get_cars'),

    # Sentiment (supports both ?text= and /<text> forms)
    path('analyze', views.analyze_review, name='analyze_review'),
    path('analyze/<path:text>', views.analyze_review_path, name='analyze_review_path'),
]
