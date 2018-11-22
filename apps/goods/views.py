from django.shortcuts import render

# Create your views here.
def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    return render(request, 'index.html')