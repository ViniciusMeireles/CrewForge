from django.conf import settings
from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.accounts.views import auth
from apps.accounts.views.invitations import InvitationViewSet
from apps.accounts.views.members import MemberViewSet
from apps.accounts.views.organizations import OrganizationViewSet
from apps.accounts.views.signup import SignupViewSet

app_name = "accounts"


router = routers.DefaultRouter()
router.register(r"signup", SignupViewSet, basename="signup")
router.register(r"organizations", OrganizationViewSet, basename="organizations")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"invitations", InvitationViewSet, basename="invitations")


authentication_urlpatterns = [
    # Authentication (JWT)
    path('api/auth/token/', auth.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Password reset
    path('api/auth/password/reset/', auth.PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/auth/password/reset/confirm/', auth.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

accounts_urlpatterns = [
    path('api/accounts/', include(router.urls)),
]

urlpatterns = authentication_urlpatterns + accounts_urlpatterns

if settings.ENVIRONMENT == 'development':
    from apps.accounts.emails import PasswordResetRequestEmail

    urlpatterns += [
        path(
            route='email-preview/auth/password/reset/',
            view=PasswordResetRequestEmail.as_view(),
            name='password_reset_email_preview',
        )
    ]
