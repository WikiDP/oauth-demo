"""Demonstrator for various flavours of OAuth"""
import logging
import os

from flask import (
    render_template,
    flash,
    request,
    session
)

from mwoauth import ConsumerToken, Handshaker

from oauthdemo.config import APP

@APP.route("/")
def route_page_welcome():
    """Landing Page for first time"""
    return render_template('welcome.html')

@APP.route("/login", methods=['POST'])
def oauth_login():
    """Login action handler."""
    consumer_key = os.environ.get('CONSUMER_TOKEN', '')
    access_key = os.environ.get('ACCESS_TOKEN', '')
    print("Consumer_key: %s" % consumer_key) #
    print("access_key: %s" % access_key) #
    consumer_token = ConsumerToken(
        consumer_key, access_key)

    print("Handshaking")
    # Construct handshaker with wiki URI and consumer
    handshaker = Handshaker(
        "https://wikidata.org/w/index.php", consumer_token)

    # Step 1: Initialize -- ask MediaWiki for a temporary key/secret for
    # user
    print("Initialising")
    redirect, request_token = handshaker.initiate()

    # Step 2: Authorize -- send user to MediaWiki to confirm authorization
    print("Point your browser to: %s" % redirect) #
    print("Authorising")
    response_qs = input("Response query string: ")

    # Step 3: Complete -- obtain authorized key/secret for "resource owner"
    print("Completing")
    access_token = handshaker.complete(request_token, response_qs)
    print(str(access_token))

    # Step 4: Identify -- (optional) get identifying information about the
    # user
    identity = handshaker.identify(access_token)
    print("Identified as {username}.".format(**identity))

    return "success"

@APP.errorhandler(404)
def route_page_error__not_found(excep):
    """Handler for 404 not found errors."""
    logging.error('Not Found: {}'.format(str(excep)))
    return render_template('error.html', message="Page Not Found"), 404


@APP.errorhandler(403)
def route_page_error__unauthorized(excep):
    """Handler for unauthorized errors."""
    logging.error('Unauthorized: {}'.format(str(excep)))
    return render_template('error.html', message="You are not authorized to view this page."), 403


@APP.errorhandler(500)
@APP.errorhandler(Exception)
def route_page_error__internal_error(excep):
    """Handler for application errors."""
    logging.error('Internal Error: {}'.format(str(excep)))
    message = "Internal Error. Please Help us by reporting this to our admin team! Thank you."
    return render_template('error.html', message=message), 500
