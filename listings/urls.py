from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledLoginForm

app_name = "listings"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(
        template_name="listings/login.html",
        authentication_form=StyledLoginForm,
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="listings:home"), name="logout"),

    path("my-listings/", views.my_listings, name="my_listings"),
    path("post/", views.create_listing, name="create_listing"),
    path("listing/<int:pk>/edit/", views.edit_listing, name="edit_listing"),
    path("listing/<int:pk>/delete/", views.delete_listing, name="delete_listing"),

    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("map/", views.map_view, name="map_all"),
    path("map/<str:category>/", views.map_view, name="map_category"),
    path("<str:category>/", views.listing_list, name="listing_list"),  # student or general
]
