from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("field-update/", views.field_update, name="field_update"),
    path("clear/<str:form_id>/", views.clear_form, name="clear_form"),
]
