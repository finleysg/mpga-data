"""mpga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from clubs import views as club_views
from communication import views as communication_views
from core import views as core_views
from documents import views as document_views
from events import views as event_views
from pages import views as page_views
from policies import views as policy_views

admin.site.site_header = "MPGA Administration"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"courses", club_views.GolfCourseViewSet, "courses")
router.register(r"contacts", club_views.ContactViewSet, "contacts")
router.register(r"club-contacts", club_views.ClubContactViewSet, "club-contacts")
router.register(r"clubs", club_views.ClubViewSet, "clubs")
router.register(r"memberships", club_views.MembershipViewSet, "memberships")
router.register(r"teams", club_views.TeamViewSet, "teams")
router.register(r"committee", club_views.CommitteeViewSet, "committee")
router.register(r"affiliates", club_views.AffiliateViewSet, "affiliates")
router.register(r"announcements", communication_views.AnnouncementViewSet, "announcements")
router.register(r"settings", core_views.SettingsViewSet, "settings")
router.register(r"documents", document_views.DocumentViewSet, "documents")
router.register(r"photos", document_views.PhotoViewSet, "photos")
router.register(r"events", event_views.EventViewSet, "events"),
router.register(r"awards", event_views.AwardViewSet, "awards"),
router.register(r"tournaments", event_views.TournamentViewSet, "tournaments"),
router.register(r"pages", page_views.LandingPageViewSet, "pages")
router.register(r"policies", policy_views.PolicyViewSet, "policies")

urlpatterns = [
    path('', include('drfpasswordless.urls')),
    url(r"^api/", include(router.urls)),
    url(r"^api/roles/", club_views.club_roles),
    url(r"^api/club-validation/(?P<club_id>[0-9]+)/$", club_views.club_validation_messages),
    url(r"^api/club-membership/(?P<club_id>[0-9]+)/$", club_views.pay_club_membership),
    url(r"^api/messages/$", communication_views.ContactMessageView.as_view()),
    url(r"^grappelli/", include("grappelli.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^nested_admin/", include("nested_admin.urls")),
    url(r"^rest-auth/", include("rest_auth.urls")),
    url(r"^rest-auth/registration/", include("rest_auth.registration.urls")),
    # this url is used to generate a password reset email
    url(r"^session/reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm"),
]
