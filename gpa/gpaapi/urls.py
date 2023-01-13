from django.urls import path, register_converter
from rest_framework.urlpatterns import format_suffix_patterns
from gpaapi import views
from gpaapi.converters import DateConverter
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

register_converter(DateConverter,'date')

urlpatterns=[
    path('accounts/', views.PGAccountsList.as_view()),
    path('accounts/<int:pk>',views.PGAccountsDetail.as_view()),
    path('transactions/',views.PGTransactionsList.as_view()),
    #path('transactions/', views.PGTransactionsDetail.as_view()),
    path('transactions/<int:pk>',views.PGTransactionsDetail.as_view()),
    path('balance/',views.PGBalanceList.as_view()),
    path('balance/<str:account_id>/<date:date>/', views.PGBalanceDetail.balance_detail),
        # The below two are added for API Authentication
    #path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/',views.MyTokenObtainPairView.as_view(),name='token_obtain'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
#    path('user/',views.UserView.as_view(),name='user'),
    path('register/',views.RegisterView.as_view(),name='auth_register'),
    path('test/',views.testEndPoint,name='test'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# Below url pattern is for functional view
# urlpatterns=[
#     path('accounts/', views.pgaccounts_list),
#     path('accounts/<int:pk>',views.pgaccounts_detail),
#     
# ]