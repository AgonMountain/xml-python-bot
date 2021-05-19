# from django.http import HttpResponseRedirect
# from django.urls import reverse
#
#
# def simple_middleware(get_response):
#     def process_request(request):
#         if not request.user.is_authenticated():
#             return HttpResponseRedirect(reverse('/'))
#         return None
#     return process_request