from rest_framework.routers import DefaultRouter
from .views import ApiRootView

class CustomRootRouter(DefaultRouter):
    APIRootView = ApiRootView