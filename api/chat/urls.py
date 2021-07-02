from django.urls import include, path
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
     path('chatintents/', views.get_chatintents ),
     path('verify/', views.verify_chat_call ),
     path('get/<query>', views.get_chat),
     path('post/<query>/', views.post_chat),

]