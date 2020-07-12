# from django.conf.urls import url, include
# from .views import ExtractiveDocumentViewSet, ExpiredDocumentViewSet, UpcomingEffectiveDocumentViewSet
# from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'laws', ExtractiveDocumentViewSet)
# router.register(r'laws/expiry', ExpiredDocumentViewSet)
# router.register(r'law/upcoming', UpcomingEffectiveDocumentViewSet)
#
# urlpatterns = [
#     url(r'^', include(router.urls)),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('api/lawtech/document/<int:id>/', views.GetById.as_view()),
    path('api/lawtech/document/searchByCode', views.SearchCodes.as_view()),
    path('api/lawtech/document/searchByTitle', views.SearchTitle.as_view()),
    path('api/lawtech/document/searchByContent', views.SearchContent.as_view()),
    path('api/lawtech/document/searchMatchAll', views.SearchMatchAll.as_view()),
    path('api/lawtech/document/getRecommendation', views.RecommendSearch.as_view()),
    path('api/lawtech/document/searchMultiField', views.MultiFieldSearch.as_view()),
    ]
