from functools import wraps

from django.shortcuts import redirect, render


class CheckLogin:
    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            return view_func(self, request, *args, **kwargs)

        return wrapper


class RequireMethod:
    def __init__(class_self, allowed_method):
        class_self.allowed_method = allowed_method  # it should be like: GET,POST,PUT,DELETE

    def __call__(class_self, view_func):  # we name self to class_self in favor of not being conflict with warp's self
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if str(class_self.allowed_method).find(f'{request.method}') == -1:
                return redirect('website:landing')
            return view_func(self, request, *args, **kwargs)

        return wrapper