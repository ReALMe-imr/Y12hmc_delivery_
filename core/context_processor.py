def user_info(request):
    if request.user.is_authenticated:
        return {'user_info': {'name': request.user.username}}
    return {}
