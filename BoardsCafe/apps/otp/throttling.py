from rest_framework.throttling import UserRateThrottle


class OTPRateThrottle(UserRateThrottle):
    scope = 'otp'