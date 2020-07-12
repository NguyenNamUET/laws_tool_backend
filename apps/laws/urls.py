from django.urls import path
from . import views

urlpatterns = [
#    path('laws/', views.ExtractiveDocumentList.as_view()),
#    path('laws/<int:pk>/', views.ExtractiveDocumentDetail.as_view()),
     path('laws/sitemaps-list', views.Sitemap.as_view()),
#     path('api/lawtech/document/NERsearch', views.SearchDocInDoc.as_view())    
]
