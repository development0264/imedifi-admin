from django.urls import path, include
from api.views import overview, guest_overview, notifications_get
from . import views

urlpatterns = [
    path('show_category/', views.DisplayCatogery.as_view()),
    path('get_blog/', views.GetCatDetails.as_view()),
    path('Get_all_blogs/<int:pid>', views.Get_all_blogs),
path('Get_all_cat/<int:pid>', views.Get_all_cat),
]

