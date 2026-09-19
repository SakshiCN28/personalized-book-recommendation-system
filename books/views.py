from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import (
    Book,
    UserProfile,
    UserRating,
    FavoriteBook
)


# ============================================================
# BOOK LIST + PERSONALIZED RECOMMENDATION
# ============================================================

def book_list(request):

    search_query = request.GET.get(
        'search',
        ''
    )

    selected_genre = request.GET.get(
        'genre',
        ''
    )

    books = Book.objects.all()


    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    if search_query:

        books = books.filter(
            title__icontains=search_query
        ) | books.filter(
            author__icontains=search_query
        ) | books.filter(
            genre__icontains=search_query
        )


    # --------------------------------------------------------
    # Genre Filter
    # --------------------------------------------------------

    if selected_genre:

        books = books.filter(
            genre__iexact=selected_genre
        )


    # --------------------------------------------------------
    # Personalized Recommendation
    # --------------------------------------------------------

    if request.user.is_authenticated:

        # Get or create profile
        profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )


        # Books rated 4 or 5 by the user
        highly_rated_book_ids = set(

            UserRating.objects.filter(
                user=request.user,
                rating__gte=4
            ).values_list(
                'book_id',
                flat=True
            )

        )


        # Books saved as favorites
        favorite_book_ids = set(

            FavoriteBook.objects.filter(
                user=request.user
            ).values_list(
                'book_id',
                flat=True
            )

        )


        # List for recommendation calculation
        book_list_data = []


        for book in books:

            # Start with a small score
            # based on the book's overall rating

            score = float(
                book.rating
            ) * 0.2


            # ------------------------------------------------
            # Favorite Genre = +3
            # ------------------------------------------------

            if (
                profile.favorite_genre
                and
                book.genre.lower()
                ==
                profile.favorite_genre.lower()
            ):

                score += 3


            # ------------------------------------------------
            # User Rated Book 4 or 5 = +2
            # ------------------------------------------------

            if book.id in highly_rated_book_ids:

                score += 2


            # ------------------------------------------------
            # User Saved Book = +2
            # ------------------------------------------------

            if book.id in favorite_book_ids:

                score += 2


            # Store score temporarily
            book.recommendation_score = score


            # Mark as recommended
            if score >= 3:

                book.is_recommended = True

            else:

                book.is_recommended = False


            book_list_data.append(
                book
            )


        # ------------------------------------------------
        # Sort by recommendation score
        # Highest score first
        # ------------------------------------------------

        books = sorted(
            book_list_data,
            key=lambda book:
                book.recommendation_score,
            reverse=True
        )


    else:

        profile = None


        # Non-logged-in users
        # see highest-rated books first

        books = books.order_by(
            '-rating'
        )


    # --------------------------------------------------------
    # Get All Genres
    # --------------------------------------------------------

    genres = Book.objects.values_list(
        'genre',
        flat=True
    ).distinct()


    # --------------------------------------------------------
    # Send Data To Template
    # --------------------------------------------------------

    return render(

        request,

        'books/book_list.html',

        {
            'books': books,

            'search_query': search_query,

            'genres': genres,

            'selected_genre': selected_genre,

            'profile': profile,
        }

    )


# ============================================================
# BOOK DETAILS
# ============================================================

def book_detail(
    request,
    book_id
):

    book = get_object_or_404(
        Book,
        id=book_id
    )


    user_rating = None

    is_favorite = False


    # --------------------------------------------------------
    # Logged-in User
    # --------------------------------------------------------

    if request.user.is_authenticated:


        # Get existing user rating
        user_rating = UserRating.objects.filter(

            user=request.user,

            book=book

        ).first()


        # Check favorite status
        is_favorite = FavoriteBook.objects.filter(

            user=request.user,

            book=book

        ).exists()


        # ----------------------------------------------------
        # Handle POST
        # ----------------------------------------------------

        if request.method == 'POST':

            action = request.POST.get(
                'action'
            )


            # ------------------------------------------------
            # Save Rating
            # ------------------------------------------------

            if action == 'rating':

                rating_value = request.POST.get(
                    'rating'
                )


                if rating_value:

                    UserRating.objects.update_or_create(

                        user=request.user,

                        book=book,

                        defaults={
                            'rating': rating_value
                        }

                    )


                    messages.success(

                        request,

                        'Your rating has been saved successfully!'

                    )


                    return redirect(

                        'book_detail',

                        book_id=book.id

                    )


            # ------------------------------------------------
            # Add / Remove Favorite
            # ------------------------------------------------

            elif action == 'favorite':


                favorite = FavoriteBook.objects.filter(

                    user=request.user,

                    book=book

                ).first()


                # Remove favorite
                if favorite:

                    favorite.delete()


                    messages.success(

                        request,

                        'Book removed from your favorites.'

                    )


                # Add favorite
                else:

                    FavoriteBook.objects.create(

                        user=request.user,

                        book=book

                    )


                    messages.success(

                        request,

                        'Book added to your favorites! ❤️'

                    )


                return redirect(

                    'book_detail',

                    book_id=book.id

                )


    # --------------------------------------------------------
    # Display Book Details
    # --------------------------------------------------------

    return render(

        request,

        'books/book_detail.html',

        {
            'book': book,

            'user_rating': user_rating,

            'is_favorite': is_favorite,
        }

    )


# ============================================================
# REGISTER
# ============================================================

def register_user(request):


    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )


        # ----------------------------------------------------
        # Check Existing Username
        # ----------------------------------------------------

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(

                request,

                'Username already exists.'

            )


            return redirect(
                'register'
            )


        # ----------------------------------------------------
        # Create User
        # ----------------------------------------------------

        user = User.objects.create_user(

            username=username,

            password=password

        )


        # ----------------------------------------------------
        # Create User Profile
        # ----------------------------------------------------

        UserProfile.objects.create(

            user=user

        )


        # ----------------------------------------------------
        # Login New User
        # ----------------------------------------------------

        login(

            request,

            user

        )


        return redirect(
            'book_list'
        )


    return render(

        request,

        'books/register.html'

    )


# ============================================================
# LOGIN
# ============================================================

def login_user(request):


    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )


        # Authenticate user
        user = authenticate(

            request,

            username=username,

            password=password

        )


        if user is not None:

            login(

                request,

                user

            )


            return redirect(
                'book_list'
            )


        else:

            messages.error(

                request,

                'Invalid username or password.'

            )


    return render(

        request,

        'books/login.html'

    )


# ============================================================
# LOGOUT
# ============================================================

def logout_user(request):

    logout(
        request
    )


    return redirect(
        'login'
    )


# ============================================================
# USER PROFILE
# ============================================================

def profile(request):


    # User must be logged in
    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    # Get or create profile
    user_profile, created = UserProfile.objects.get_or_create(

        user=request.user

    )


    # Get available genres
    genres = Book.objects.values_list(

        'genre',

        flat=True

    ).distinct()


    # --------------------------------------------------------
    # Save Favorite Genre
    # --------------------------------------------------------

    if request.method == 'POST':

        user_profile.favorite_genre = request.POST.get(

            'favorite_genre',

            ''

        )


        user_profile.save()


        return redirect(
            'book_list'
        )


    return render(

        request,

        'books/profile.html',

        {
            'profile': user_profile,

            'genres': genres,
        }

    )


# ============================================================
# MY FAVORITES
# ============================================================

def my_favorites(request):


    # User must be logged in
    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    # Get user's favorite books
    favorite_books = FavoriteBook.objects.filter(

        user=request.user

    ).select_related(

        'book'

    ).order_by(

        '-created_at'

    )


    return render(

        request,

        'books/favorites.html',

        {
            'favorite_books': favorite_books,
        }

    )


# ============================================================
# USER DASHBOARD
# ============================================================

def dashboard(request):


    # --------------------------------------------------------
    # User must be logged in
    # --------------------------------------------------------

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    # --------------------------------------------------------
    # Get User Profile
    # --------------------------------------------------------

    user_profile, created = UserProfile.objects.get_or_create(

        user=request.user

    )


    # --------------------------------------------------------
    # Count Total Books
    # --------------------------------------------------------

    total_books = Book.objects.count()


    # --------------------------------------------------------
    # Get User Ratings
    # --------------------------------------------------------

    user_ratings = UserRating.objects.filter(

        user=request.user

    ).select_related(

        'book'

    ).order_by(

        '-created_at'

    )


    # --------------------------------------------------------
    # Get Favorite Books
    # --------------------------------------------------------

    favorite_books = FavoriteBook.objects.filter(

        user=request.user

    ).select_related(

        'book'

    ).order_by(

        '-created_at'

    )


    # --------------------------------------------------------
    # Count Ratings
    # --------------------------------------------------------

    total_ratings = user_ratings.count()


    # --------------------------------------------------------
    # Count Favorites
    # --------------------------------------------------------

    total_favorites = favorite_books.count()


    # --------------------------------------------------------
    # Display Dashboard
    # --------------------------------------------------------

    return render(

        request,

        'books/dashboard.html',

        {
            'profile': user_profile,

            'total_books': total_books,

            'user_ratings': user_ratings,

            'favorite_books': favorite_books,

            'total_ratings': total_ratings,

            'total_favorites': total_favorites,
        }

    )