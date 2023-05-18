from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view(), name='home'),
   path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchList.as_view()),
   path('create/', PostAdd.as_view(), name='post_create'),
   path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscriber', subscriber, name='subscriber'),
   path('categories/<int:pk>/unsubscriber', unsubscriber, name='unsubscriber'),

]