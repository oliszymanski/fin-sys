from django.urls import path
from . import views

urlpatterns = [
    path( '', views.index, name='index' ),
    path( 'account/', views.account_details, name='account_details' ),
    path( 'deposit/', views.deposit, name='deposit' ),
    path( 'withdraw/', views.withdraw, name='withdraw' ),
]