from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class AuthRateThrottle(UserRateThrottle):
    scope = 'auth'


class OTPRateThrottle(UserRateThrottle):
    scope = 'otp'


class AnonAPIRateThrottle(AnonRateThrottle):
    scope = 'anon'