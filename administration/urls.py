from django.urls import path
from .views import index, UsersViews, UsersEdit, UsersCreation, UserDeletion, MediaLibraryCreations, MediaLibraryViews,\
    MediaLibraryEditing, MediaLibraryDelation

urlpatterns = [
    path('admininstration/', index, name='index_admin'),
    path('admininstration/users/', UsersViews, name='UsersViews'),
    path('admininstration/edit_user/<int:id>', UsersEdit, name='UsersEdit'),
    path('admininstration/create_user/', UsersCreation, name='UsersCreation'),
    path('admininstration/delete_users/', UserDeletion, name='UserDeletion'),
    path('admininstration/create_mediatheque/', MediaLibraryCreations, name='MediaLibraryCreations'),
    path('admininstration/mediatheques/', MediaLibraryViews, name='MediaLibraryViews'),
    path('admininstration/edit_mediatheque/<int:id>', MediaLibraryEditing, name='MediaLibraryEditing'),
    path('admininstration/delete_mediatheque/', MediaLibraryDelation, name='MediaLibraryDelation'),

]
