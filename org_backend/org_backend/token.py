from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        if hasattr(user,'technicien') : 
            token['tech_id'] = user.technicien.id
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# tech token : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4OTUwMjg5LCJpYXQiOjE2NTI1NTAyODksImp0aSI6IjYxYTExZWU3YmVmYjRmYzZiZjNhYzIxN2QzZDk5NzljIiwidXNlcl9pZCI6MTUsImlzX2FkbWluIjpmYWxzZX0.ngEws59Zg9ISfVgV_TJeib2r_ByT8EiDCqksz0SgxRI
# admin token  : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4OTUwNTkzLCJpYXQiOjE2NTI1NTA1OTMsImp0aSI6Ijk5NzYzODkyM2QwMjRmYjBhZjhjZGE0NjlmYjU3NWY0IiwidXNlcl9pZCI6MywiaXNfYWRtaW4iOnRydWV9.hLp-l52pZlkOtfxHXjiGISHI22ntqXKlBtfVU6LTg70