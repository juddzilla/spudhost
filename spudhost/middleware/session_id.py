from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the sessionid from the request cookies        
        # sessionid = request.COOKIES.get('sessionid')             
        
        # Check if sessionid exists
        # if sessionid:
        #     try:
        #         # Find the user associated with the sessionid
        #         session = Session.objects.get(session_key=sessionid)
        #         user_id = session.get_decoded().get('_auth_user_id')  
        #         user = User.objects.get(id=user_id)
        #         # Attach the user to the request for easy access in views
        #         request.user = user
        #     except (Session.DoesNotExist, User.DoesNotExist):                
        #         pass

        user = User.objects.get(id=2)
        # Attach the user to the request for easy access in views
        request.user = user

        response = self.get_response(request)
        return response
