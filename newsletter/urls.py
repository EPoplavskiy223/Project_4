from django.urls import path

from newsletter import views

app_name = "newsletter"

urlpatterns = [
    path("", views.MessageListView.as_view(), name="message_list"),
    path("<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    path("create/", views.MessageCreateView.as_view(), name="message_create"),
    path("<int:pk>/update/", views.MessageUpdateView.as_view(), name="message_update"),
    path("<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/send/", views.MailingSendView.as_view(), name="mailing_send"),
    path("attempts/", views.MailingAttemptListView.as_view(), name="attempt_list"),
]
