from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth import views as auth_views

urlpatterns = [
     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


     path('home/', views.home, name='home'),
     path('', views.home, name='home'),
     path('contactus/',views.contact_us, name='contactus'),
     path('aboutus/',views.about_us, name='aboutus'),
     path('login/',views.login_view, name='login'),
     path('signup/',views.signup_view, name='signup'),
     path('signout/',views.signout_view , name='signout'),
     path('social-auth/', include('social_django.urls', namespace='social')),
     path('add_contactus/', views.add_contact_us, name='add_contact'),
 

     path('products/<int:pk>/', views.productdetail, name='productdetail'),
     path('category/<int:pk>/', views.category_view, name='category_view'),
     path('category_sort_in/<int:pk>/', views.sort_increment_product, name='category_sort_in'),
     path('category_sort_de/<int:pk>/', views.sort_decrement_product, name='category_sort_de'),
     path('profile/',views.profile_view, name='profile'),

     path('update_profile_user/', views.update_profile_user, name='update_profile_user'),
     path('changepassword_view/', views.change_password_view, name='changepassword_view'),
     path('update_pass_user/', views.update_password_user, name='update_password_user'),

     path('add_to_cart', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.cart, name='cart'),
     path('checkout/', views.payment_view, name='checkout'),
     path('order/', views.order, name='order'),
     path('save_order/',views.place_order, name='save_order'),

     path('increment_product',views.increment_product, name='increment_product'),
     path('decrement_product',views.decrement_product, name='decrement_product'),
     
     path('search_product/',views.search_product, name='search_product'),
     path('review/',views.Review_Rate, name='reivew'),
     path('remove_product/<int:pk>/',views.remove_product, name='remove_product'),
     path('plus_cart/<int:pk>/', views.plus_item, name='plus_cart'),
     path('minus_cart/<int:pk>/', views.minus_item, name='minus_cart'),


     path('adminlogin/',views.admin_login_view, name='adminlogin'),
     path('loginadmin/',views.admin_login, name='loginadmin'),
     path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
     path('logoutadmin/',views.logout_view, name='logoutadmin'),
     path('customer_view/',views.customer_view, name='customer_view'),
     
     path('product_view/',views.product_view, name='product_view'),
     path('add_product_view/', views.add_product_view, name='add_product_view'),
     path('add_product/', views.add_product_admin, name='add_product'),
     path('update_product_view/<int:pk>', views.update_product_view, name='update_product_view'),
     path('update_product/', views.update_product, name='update_product'),
     path('delete_product/<int:pk>', views.delete_product, name='delete_product'),

     path('customer_update_view/<int:pk>',views.customer_update_view, name='customer_update_view'),
     path('update_customer/',views.update_customer, name='update_customer'),
     path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),

     path('category_view_admin/',views.category_view_admin, name='category_view_admin'),
     path('add_category_view/', views.add_category_view, name='add_category_view'),
     path('add_category/', views.add_category, name='add_category'),
     path('delete_category/<int:pk>', views.delete_category, name='delete_category'),

     path('cart_view_admin/',views.cart_view_admin, name='cart_view_admin'),
     path('cartitem_view_admin/',views.cartitem_view_admin, name='cartitem_view_admin'),
     path('review_view_admin/',views.review_view_admin, name='review_view_admin'),
     path('order_view_admin/',views.order_view_admin, name='order_view_admin'),
     path('orderitem_view_admin/',views.orderitem_view_admin, name='orderitem_view_admin'),
     path('sales_chart/', views.sales_chart, name='sales_chart'),
     
     path('view_update_category/<int:pk>', views.view_update_category, name='view_update_category'),
     path('update_category/', views.update_category, name='update_category'),
     path('view_update_order/<str:pk>',views.view_update_order, name='view_update_order'),
     path('update_status_order/', views.update_status_order, name='update_status_order'),

     path('view_contactus/', views.contactus_view, name='view_contactus'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)