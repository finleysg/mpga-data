from django.conf.urls import url
from clubs import views as core_views


urlpatterns = [
    url(r'^$', core_views.api_root),
    url(r'^courses/$', core_views.GolfCourseList.as_view(), name='course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$', core_views.GolfCourseDetail.as_view(), name='course-detail'),
    url(r'^contacts/$', core_views.ContactList.as_view(), name='contact-list'),
    url(r'^contacts/(?P<pk>[0-9]+)/$', core_views.ContactDetail.as_view(), name='contact-detail'),
    url(r'^clubs/$', core_views.ClubList.as_view(), name='club-list'),
    url(r'^clubs/(?P<pk>[0-9]+)/$', core_views.ClubDetail.as_view(), name='club-detail'),
    url(r'^memberships/$', core_views.MembershipList.as_view(), name='membership-list'),
    url(r'^memberships/(?P<pk>[0-9]+)/$', core_views.MembershipDetail.as_view(), name='membership-detail'),
    url(r'^teams/$', core_views.TeamList.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$', core_views.TeamDetail.as_view(), name='team-detail'),
]
