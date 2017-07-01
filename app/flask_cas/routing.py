import sys
import ssl
import flask
from xmltodict import parse
from flask import current_app
from .cas_urls import create_cas_login_url
from .cas_urls import create_cas_logout_url
from .cas_urls import create_cas_validate_url

from flask import redirect, url_for

# for proxy
import urllib2
from .proxy_support import ConnectHTTPHandler
from .proxy_support import ConnectHTTPSHandler
 
try:
	from urllib import urlopen
except ImportError:
	from urllib.request import urlopen

blueprint = flask.Blueprint('cas', __name__)


@blueprint.route('/login/')
def login():
	"""
	This route has two purposes. First, it is used by the user
	to login. Second, it is used by the CAS to respond with the
	`ticket` after the user logs in successfully.

	When the user accesses this url, they are redirected to the CAS
	to login. If the login was successful, the CAS will respond to this
	route with the ticket in the url. The ticket is then validated.
	If validation was successful the logged in username is saved in
	the user's session under the key `CAS_USERNAME_SESSION_KEY` and
	the user's attributes are saved under the key
	'CAS_USERNAME_ATTRIBUTE_KEY'
	"""

	cas_token_session_key = current_app.config['CAS_TOKEN_SESSION_KEY']

	redirect_url = create_cas_login_url(
		current_app.config['CAS_SERVER'],
		current_app.config['CAS_LOGIN_ROUTE'],
		flask.url_for('.login', _external=True))

	if 'ticket' in flask.request.args:
		flask.session[cas_token_session_key] = flask.request.args['ticket']

	if cas_token_session_key in flask.session:

		if validate(flask.session[cas_token_session_key]):
			if 'CAS_AFTER_LOGIN_SESSION_URL' in flask.session:
				redirect_url = flask.session.pop('CAS_AFTER_LOGIN_SESSION_URL')
			else:
				redirect_url = flask.url_for(
					current_app.config['CAS_AFTER_LOGIN'])
		else:
			del flask.session[cas_token_session_key]

	current_app.logger.debug('Redirecting to: {0}'.format(redirect_url))
	return flask.redirect(redirect_url)


@blueprint.route('/logout/')
def logout():
	"""
	When the user accesses this route they are logged out.
	"""

	cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']
	cas_attributes_session_key = current_app.config['CAS_ATTRIBUTES_SESSION_KEY']

	if cas_username_session_key in flask.session:
		del flask.session[cas_username_session_key]

	if cas_attributes_session_key in flask.session:
		del flask.session[cas_attributes_session_key]

	if(current_app.config['CAS_AFTER_LOGOUT'] != None):
		redirect_url = create_cas_logout_url(
			current_app.config['CAS_SERVER'],
			current_app.config['CAS_LOGOUT_ROUTE'],
			current_app.config['CAS_AFTER_LOGOUT'])
	else:
		redirect_url = create_cas_logout_url(
			current_app.config['CAS_SERVER'],
			current_app.config['CAS_LOGOUT_ROUTE'])

	current_app.logger.debug('Redirecting to: {0}'.format(redirect_url))

	return redirect(url_for('home.signout'))		
	# return flask.redirect(redirect_url)


def validate(ticket):
	"""
	Will attempt to validate the ticket. If validation fails, then False
	is returned. If validation is successful, then True is returned
	and the validated username is saved in the session under the
	key `CAS_USERNAME_SESSION_KEY` while tha validated attributes dictionary
	is saved under the key 'CAS_ATTRIBUTES_SESSION_KEY'.
	"""

	cas_username_session_key = current_app.config['CAS_USERNAME_SESSION_KEY']
	cas_attributes_session_key = current_app.config['CAS_ATTRIBUTES_SESSION_KEY']

	current_app.logger.debug("validating token {0}".format(ticket))

	cas_validate_url = create_cas_validate_url(
		current_app.config['CAS_SERVER'],
		current_app.config['CAS_VALIDATE_ROUTE'],
		flask.url_for('.login', _external=True),
		ticket)

	current_app.logger.debug("Making GET request to {0}".format(
		cas_validate_url))

	xml_from_dict = {}
	isValid = False

	try:

		IIITproxy="proxy.iiit.ac.in:8080"
		opener = urllib2.build_opener(ConnectHTTPHandler(proxy=IIITproxy),ConnectHTTPSHandler(proxy=IIITproxy))
		urllib2.install_opener(opener)

		# currently no for IIIT proxy
		# proxies = {"http":("http://"+IIITproxy),"https":("https://"+IIITproxy),"no_proxy":"localhost, 127.0.0.1, iiit.ac.in, .iiit.ac.in, iiit.net, .iiit.net, 172.16.0.0/12, 192.168.0.0/16, 10.0.0.0/8"}
		# proxy_support = urllib.request.ProxyHandler(proxies)
		# opener = urllib.request.build_opener(proxy_support)
		# urllib.request.install_opener(opener)
		context = ssl._create_unverified_context()		
		xmldump = urlopen(cas_validate_url, context=context).read().strip().decode('utf-8', 'ignore')
		print ("xmldump :%s",xmldump)
		xml_from_dict = parse(xmldump)
		isValid = True if "cas:authenticationSuccess" in xml_from_dict["cas:serviceResponse"] else False
	except ValueError:
		current_app.logger.error("CAS returned unexpected result")

	if isValid:
		current_app.logger.debug("valid")
		xml_from_dict = xml_from_dict["cas:serviceResponse"]["cas:authenticationSuccess"]
		username = xml_from_dict["cas:user"]
		attributes = xml_from_dict["cas:attributes"]

		if "cas:memberOf" in attributes:
			attributes["cas:memberOf"] = attributes["cas:memberOf"].lstrip('[').rstrip(']').split(',')
			for group_number in range(0, len(attributes['cas:memberOf'])):
				attributes['cas:memberOf'][group_number] = attributes['cas:memberOf'][group_number].lstrip(' ').rstrip(' ')

		flask.session[cas_username_session_key] = username
		flask.session[cas_attributes_session_key] = attributes
	else:
		current_app.logger.debug("invalid")

	return isValid
