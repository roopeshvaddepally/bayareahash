from common.db import get_admin_for_authentication


def authenticate_user(user, password):
    admin = get_admin_for_authentication(user)
    if admin.get('password') == password:
        print "yes"
        return True
    else:
        print "no"
        return False
