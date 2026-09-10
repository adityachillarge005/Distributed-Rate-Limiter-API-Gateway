from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from .rate_limit import check_request_rate_limit
from .load_balancer import get_next_backend
from .queue import add_to_queue
import redis
# Create your views here.

class RedisTestView(APIView):
    def get(self,request):
        cache.set("test_key","hello from Django",timeout=60)
        value = cache.get("test_key")

        return Response({"redis_value":value})


class HealthCheck(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({
            "status":"healthy",
            "user":str(request.user),
            "user_id":request.user.id,
            })


class AdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({
            "message":"Hello admin",
            "user" : str(request.user)
        })

# token bucket

# class HealthView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         if not check_rate_limit(request.user.id):
#             return Response(
#                 {"detail": "Rate limit exceeded"},
#                 status=status.HTTP_429_TOO_MANY_REQUESTS
#             )

#         return Response({"status": "healthy"})

# sliding window

class HealthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if not check_request_rate_limit(request.user.id):
                return Response(
                    {"detail":"Rate limit exeeced"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        return Response({"status":"Healthy"})

class Backend1View(APIView):
    def get(self, request):
        return Response({
            "backend": "Backend 1",
            "message": "Response from Backend 1"
        })


class Backend2View(APIView):
    def get(self, request):
        return Response({
            "backend": "Backend 2",
            "message": "Response from Backend 2"
        })


class Backend3View(APIView):
    def get(self, request):
        return Response({
            "backend": "Backend 3",
            "message": "Response from Backend 3"
        })


r = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
class GatewayView(APIView):
    permission_classes = [IsAuthenticated]

    

    def get(self, request):

        if not check_request_rate_limit(request.user.id):
            r.incr("gateway:metrics:rejected_requests")

            return Response(
                {"detail": "rate limit exceeded"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
                )

        r.incr("gateway:metrics:total_requests")

        backend = get_next_backend()
        if backend == "Backend 1":
            r.incr("gateway:metrics:backend1")

        elif backend == "Backend 2":
            r.incr("gateway:metrics:backend2")

        elif backend == "Backend 3":
            r.incr("gateway:metrics:backend3")

        add_to_queue(f"Request from {backend}")

        return Response({
            "message": "succesfully reached backend",
            "backend": backend
        })


class MetricsView(APIView):

    def get(self, request):

        return Response({
            "total_requests": int(
                r.get("gateway:metrics:total_requests") or 0
            ),
            "rejected_requests": int(
                r.get("gateway:metrics:rejected_requests") or 0
            ),
            "backend1": int(
                r.get("gateway:metrics:backend1") or 0
            ),
            "backend2": int(
                r.get("gateway:metrics:backend2") or 0
            ),
            "backend3": int(
                r.get("gateway:metrics:backend3") or 0
            ),
        })