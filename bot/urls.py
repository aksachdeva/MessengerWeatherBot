from django.conf.urls import url

from .views import FbotView

urlpatterns = [
    url(r'^7749d7bc89ce4aa3a2a27b375f8ce0ff245d5a3f0ec1efc35a/$', FbotView.as_view()),
]