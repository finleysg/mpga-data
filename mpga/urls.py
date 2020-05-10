"""mpga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.conf.urls import url, include
from django.contrib import admin
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
router.register(r"match-results", club_views.MatchPlayResultViewSet, "match-results")
router.register(r"committee", club_views.CommitteeViewSet, "committee")
router.register(r"affiliates", club_views.AffiliateViewSet, "affiliates")
router.register(r"announcements", communication_views.AnnouncementViewSet, "announcements")
router.register(r"settings", core_views.SettingsViewSet, "settings")
router.register(r"documents", document_views.DocumentViewSet, "documents")
router.register(r"photos", document_views.PhotoViewSet, "photos")
router.register(r"events", event_views.EventViewSet, "events"),
router.register(r"event-links", event_views.EventLinkViewSet, "event-links"),
router.register(r"event-points", event_views.EventPointsViewSet, "event-points"),
router.register(r"event-policies", event_views.EventPolicyViewSet, "event-policies"),
router.register(r"awards", event_views.AwardViewSet, "awards"),
router.register(r"award-winners", event_views.AwardWinnerViewSet, "award-winners"),
router.register(r"tournaments", event_views.TournamentViewSet, "tournaments"),
router.register(r"tournament-winners", event_views.TournamentWinnerViewSet, "tournament-winners"),
router.register(r"pages", page_views.LandingPageViewSet, "pages")
router.register(r"policies", policy_views.PolicyViewSet, "policies")
router.register(r"tags", document_views.TagViewSet, "tags")

urlpatterns = [
    url(r"^api/", include(router.urls)),
    url(r"^api/roles/", club_views.club_roles),
    url(r"^api/contact-roles/", club_views.contact_roles),
    url(r"^api/club-dues/(?P<club_id>[0-9]+)/$", club_views.get_club_dues_intent),
    url(r"^api/club-dues/complete/$", club_views.club_dues_complete),
    url(r"^api/messages/$", communication_views.ContactMessageView.as_view()),
    url(r"^api/tournament-photos/random/(?P<tournament>[0-9]+)/$", document_views.random_photo),
    url(r"^api/tournament-photos/years/(?P<tournament>[0-9]+)/$", document_views.available_years),
    url(r"^admin/", admin.site.urls),
    url(r"^nested_admin/", include("nested_admin.urls")),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
