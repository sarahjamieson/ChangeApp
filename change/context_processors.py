def app_name(request):
    app_name = request.resolver_match.route.split('/')[0]
    return {"app_name": app_name}
