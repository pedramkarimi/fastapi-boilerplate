class RedisKeys:
    # ---- AUTH / SECURITY KEYS ----
    BRUTE_FORCE_EMAIL_ATTEMPTS = "security:bruteforce:email:{email}:attempts"
    BRUTE_FORCE_IP_ATTEMPTS = "security:bruteforce:ip:{ip}:attempts"
    BRUTE_FORCE_EMAIL_LOCK = "security:bruteforce:email:{email}:lock"
    BRUTE_FORCE_IP_LOCK = "security:bruteforce:ip:{ip}:lock"
    RATE_LIMIT_IP_ROUTE = "security:ratelimit:ip:{ip}:{path}"
    # RATE_LIMIT_USERID_ROUTE = "security:ratelimit:user:{user_id}:{route}"
    # OTP_PHONE = "auth:otp:phone:{phone}"
    # OTP_EMAIL = "auth:otp:email:{email}"
    # TOKEN_BLACK_LIST = "auth:token:blacklist:{jti}"
    # USER_ID_LOCK = "auth:user:{user_id}:lock"

    # ---- AUTH / SECURITY KEYS ----
    @staticmethod
    def brute_force_email_attempts(email: int) -> str:
        return RedisKeys.BRUTE_FORCE_EMAIL_ATTEMPTS.format(email=email)
    
    @staticmethod
    def brute_force_ip_attempts(ip: int) -> str:
        return RedisKeys.BRUTE_FORCE_IP_ATTEMPTS.format(ip=ip)

    @staticmethod
    def brute_force_email_lock(email: str) -> str:
        return RedisKeys.BRUTE_FORCE_EMAIL_LOCK.format(email=email)
    
    @staticmethod
    def brute_force_ip_lock(ip: str) -> str:
        return RedisKeys.BRUTE_FORCE_IP_LOCK.format(ip=ip)
    
    @staticmethod
    def rate_limit_ip(ip: str, path: str) -> str:
        return RedisKeys.RATE_LIMIT_IP_ROUTE.format(ip=ip, path=path)


