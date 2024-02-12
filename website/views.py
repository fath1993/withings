from django.shortcuts import render, redirect


def index_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    else:
        return render(request, 'index.html', context)

