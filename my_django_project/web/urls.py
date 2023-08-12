from django.urls import path
from . import views
from django.conf.urls import (handler400, handler403, handler404, handler500)
handler404 = 'web.views.handler404'
handler500 = 'web.views.handler500'
urlpatterns = [
    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),

    path('login/', views.log_in, name='login'),
    path('project/', views.project_view, name='project_view'),

    path('users_view/', views.users_view, name='users_view'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),


    path('addProject/', views.addProject, name='addProject'),
    path('editproject/<int:id>/', views.editProject, name='editProject'),
    path('delete_project/<int:id>/', views.delete_project, name='delete_project'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

    path('autocomplete_userid/', views.autocomplete_userid, name='autocomplete_userid'),


    path('logout_view/', views.logout_view, name='logout_view'),
    path('start_break/', views.start_break, name='start_break'),
    path('report_view/', views.report_view, name='report_view'),
    path('user_progress_view/', views.user_progress_view, name='user_progress_view'),


    # path('end_break/<int:break_id>/', views.end_break, name='end_break')




]
