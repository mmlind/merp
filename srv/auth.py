# coding: utf-8
#!/usr/bin/env python
#
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under LGPLv3+ license, see LICENSE.txt
#
# Cork example web application
#
# The following users are already available:
#  admin/admin, demo/demo

from language import _,get_html_tpl

import os
import settings
import bottle

from beaker.middleware import SessionMiddleware
from cork import Cork
import logging




logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

srv_path = os.path.dirname(os.path.realpath(__file__))

# Use users.json and roles.json in the local example_conf directory
aaa = Cork(srv_path+'/auth', email_sender='my_email@hostname.com', smtp_url='starttls://my_email@hostname.com:my_password@smtp.hostname.com:587')

app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)


# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


@bottle.post('/<locale>/signin')
def post_signin(locale=settings.DEFAULT_LOCALE):
    settings.CURRENT_LOCALE = locale
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/' + locale + '/', fail_redirect='/'+ locale +'/signin?error=1')


@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/signout')
def logout():
    aaa.logout(success_redirect='/' + settings.CURRENT_LOCALE + '/signin')


@bottle.post('/register')
def register():
    """Send out registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    return 'Please check your mailbox.'


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/signin">Go to sign-in</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address')
    )
    return 'Please check your mailbox.'


@bottle.route('/change_password/:reset_code')
@bottle.view('auth_password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/signin">Go to sign-in</a>'


# @bottle.route('/')
# def index():
#     """Only authenticated users can see this"""
#     aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
#     return 'Welcome! <a href="/admin">Admin page</a> <a href="/signout">Sign-out</a>'


@bottle.route('/restricted_download')
def restricted_download():
    """Only authenticated users can download this file"""
    aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print "Session from simple_webapp", repr(session)
    aaa.require(fail_redirect='/' + settings.CURRENT_LOCALE + '/signin')
    return aaa.current_user.role


# Admin-only pages

@bottle.route('/admin')
@bottle.view('auth_admin_page')
def admin():
    """Only admin users can see this"""
    aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles()
    )


@bottle.post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)



@bottle.route('/<locale>/signin')
def url_signin(locale=settings.DEFAULT_LOCALE):
    settings.CURRENT_LOCALE = locale
    tpl  = get_html_tpl(bottle, "page_header", page_title=_("Sign in"))
    tpl += get_html_tpl(bottle, "signin", page_title=_("Sign in"))
    tpl += get_html_tpl(bottle, "page_footer")
    return tpl



# Static pages

# @bottle.route('/signin')
# @bottle.view('auth_signin_form')
# def signin_form():
#     """Serve login form"""
#     return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


# #  Web application main  # #

# def main():

#     # Start the Bottle webapp
#     bottle.debug(True)
#     bottle.run(app=app, quiet=False, reloader=True)

# if __name__ == "__main__":
#     main()
