from fastapi import Request

def get_client_ip(request: Request) -> str:
    if request.client:
        return request.client.host
    
    if request.headers.get("x-forwarded-for"):
        forwarded_for = request.headers["x-forwarded-for"]
        return forwarded_for.split(",")[0].strip()
    
    return "unknown"
