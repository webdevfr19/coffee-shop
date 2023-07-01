from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Userlogin, name='login'),
    path('signup/', views.Usersignup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'), #class-based logout function
    # path('logout/', views.logout, name="logout"),
    path('customer-info/', views.customerInfo, name='customer-info'),
    path('user-settings/<str:pk>', views.userProfile, name='user-settings'),
    path('menu/', views.menu, name='menu'),
    path('drink/<str:pk>', views.orderDrink, name='order-drink'),
    path('food/<str:pk>', views.orderFood, name='order-food'),
    path('merch/<str:pk>', views.orderMerch, name='order-merch'),
    path('cart/', views.cart, name='cart'),
    path('delivery/', views.delivery, name='delivery'),
    path('update-item/', views.updateItem, name='update-item'),
    path('404/', views.Error404, name="error404"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
