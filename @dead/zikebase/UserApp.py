"""
App to let users signup, login, request passwords, etc.
"""
__ver__="$Id$"

import zikebase
zikebase.load("AppActor")

class UserApp(zikebase.AppActor):

    def act_create(self):

        # create the user:
        user = zikebase.User()
        user.username = self.input['username']
        user.password = self.input['password']
        user.email = self.input['email']
        user.save()
