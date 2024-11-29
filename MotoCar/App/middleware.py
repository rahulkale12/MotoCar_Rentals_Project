from django.shortcuts import redirect


def auth_middleware(get_response):

    def middleware(request):

        if ((request.path == 'my_rentals/' or request.path == 'my_cart/' or request.path == "/accounts/customer_profile/") and request.session.get('id') is None ):
            return redirect('/accounts/login/')
        
     
        elif ((request.path == '/accounts/login/' or request.path == '/accounts/register/') and request.session.get('id') is not None):
            return redirect('/accounts/customer_profile/')
        
        
        

        response = get_response(request)



        return response
    return middleware
