from django.conf.urls import url,include
from lvl5_App import views

app_name = 'lvl5_App'

urlpatterns = [
    # url(r'index',views.index,name = 'index'),
    url(r'^register',views.register,name = 'register'),
    url(r'^user_login',views.user_login,name='user_login'),

    ]
