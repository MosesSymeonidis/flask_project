main_urls = {
    "/user": 'views.Users.user',
    "/login": "views.Users.login"
}

debug_urls = {'/debug':'views.test.test'}

def get_urls(debug=False):
    if debug:
        main_urls.update(debug_urls)
        return main_urls
    return main_urls