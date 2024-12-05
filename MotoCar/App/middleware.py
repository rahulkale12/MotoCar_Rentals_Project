# from django.shortcuts import redirect


# def auth_middleware(get_response):

#     def middleware(request):

#         if ((request.path == 'my_rentals/' or request.path == 'my_cart/' or request.path == "/accounts/customer_profile/") and request.session.get('id') is None ):
#             return redirect('/accounts/login/')
        
     
#         if ((request.path == '/accounts/login/' or request.path == '/accounts/register/') and request.session.get('id') is not None):
#             return redirect('/accounts/customer_profile/')
        
        
        

#         response = get_response(request)



#         return response
#     return middleware


# from django.shortcuts import redirect

# def auth_middleware(get_response):
#     def middleware(request):
#         # Debugging: Log session and path
#         print(f"Path: {request.path}, Session ID: {request.session.get('id')}")

#         # Ensure session exists for protected paths
#         protected_paths = ['/my_rentals/', '/my_cart/', '/accounts/customer_profile/']
#         if request.path in protected_paths and not request.session.get('id'):
#             return redirect('/accounts/login/')

#         # Redirect logged-in users away from login/register pages
#         public_paths = ['/accounts/login/', '/accounts/register/']
#         if request.path in public_paths and request.session.get('id'):
#             return redirect('/accounts/customer_profile/')

#         # Pass the request further
#         return get_response(request)

#     return middleware

