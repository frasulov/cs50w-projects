from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("visititem/<int:item_id>", views.infoitem, name="info"),
    path("addcomment/<int:item_id>", views.addcomment, name="addcomment"),
    path("addbid/<int:item_id>", views.addbid, name="addbid"),
    path("unactive/<int:item_id>", views.makeunactive, name="unactive"),
    path("create", views.createAuction, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.category, name="categories"),
    path("categories/<str:category>", views.specificcategory, name="specificcategory")
]
