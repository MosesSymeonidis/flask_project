from views import BaseView
from Models.User import *
import os


class test(BaseView):
    def get(self):
        user = User()
        user.set_username_and_password('moses', 'moses2113')

        user.save()

        return user
