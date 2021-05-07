"""middleware URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from middleware_area.routes import service, area, auth_service, auth, file_route, app, user_email, third_party_auth, third_party_link, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app', app.DownloadApp.as_view(),name="App downloading path"),
    path('auth/login', auth.Login.as_view(), name="Login user"),
    path('auth/third_party_auth', third_party_auth.ThirdPartyAuth.as_view(), name="Third Party Auth"),
    path('auth/third_party_link/<str:user_id>', third_party_link.ThirdPartyLink.as_view(), name="Third Party Link"),
    path('auth/register', auth.Register.as_view(), name="Register user"),
    path('auth/delete', auth.Delete.as_view(), name="Delete user"),
    path('user/email', user_email.UserEmail.as_view(), name="Reset password for user"),
    # Oauth routes service
    path('service/spotify/callback', auth_service.Spotify.as_view(), name="Spotify callback"),
    path('service/github/callback', auth_service.GithubOAuth.as_view(), name="Github callback"),
    path('service/discord/callback', auth_service.DiscordOAuth.as_view(), name="Discord callback"),
    path('service/reddit/callback', auth_service.RedditOAuth.as_view(), name="Reddit callback"),
    path('service/stackoverflow/callback', auth_service.StackOverflowOAuth.as_view(), name="StackOverflow callback"),
    path('service/twitch/callback', auth_service.TwitchOAuth.as_view(), name="Twitch callback"),
    path('service/azure/callback', auth_service.AzureOAuth.as_view(), name="Azure callback"),

    path('services', service.Services.as_view(), name="service"),
    path('service/<str:service_name>', service.Service.as_view(), name="service"),
    path('area/', area.HandleArea.as_view(), name="Handle AREA"),
    path('area/<str:area_id>/', area.AreaInformation.as_view(), name="Information AREA"),
    path('about.json', about.About.as_view(), name="About information on ou service/trigger/reaction")
]