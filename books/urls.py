from django.urls import path
from . import views


urlpatterns = [

    # --------------------------------
    # Home / Book List
    # --------------------------------

    path(
        '',
        views.book_list,
        name='book_list'
    ),


    # --------------------------------
    # Book Details
    # --------------------------------

    path(
        'book/<int:book_id>/',
        views.book_detail,
        name='book_detail'
    ),


    # --------------------------------
    # Register
    # --------------------------------

    path(
        'register/',
        views.register_user,
        name='register'
    ),


    # --------------------------------
    # Login
    # --------------------------------

    path(
        'login/',
        views.login_user,
        name='login'
    ),


    # --------------------------------
    # Logout
    # --------------------------------

    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),


    # --------------------------------
    # User Profile
    # --------------------------------

    path(
        'profile/',
        views.profile,
        name='profile'
    ),


    # --------------------------------
    # My Favorites
    # --------------------------------

    path(
        'favorites/',
        views.my_favorites,
        name='favorites'
    ),


    # --------------------------------
    # User Dashboard
    # --------------------------------

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

]