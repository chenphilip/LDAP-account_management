#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This provides basic information of LDAP server and data structure
For Python hashing and test functions for user passwords stored in OpenLDAP, refer
to https://gist.github.com/rca/7217540

"""
__author__ = "Philip Chen"
__license__ = "https://opensource.org/licenses/GPL-3.0 GPL-3.0 License"
__date__ = "2016.06.18"
__version__ = "1.0.0"
__status__ = "Tested on Python 3.5, OpenLDAP 2.4 on Centos 7"

# LDAP_URI = '192.168.56.102'
LDAP_URI = 'ldap.mydomain.com'

BIND_USER = {
    'DN': 'cn=Manager,dc=ad,dc=mydomain,dc=com',
    'password': 'admpassword'
}

# BASE_DN = 'dc=ad,dc=mydomain,dc=com'
BASE_DN = 'ou=IDMUSERS,dc=ad,dc=mydomain,dc=com'

userInfo = {
    'uidLDAP': 'pchen',
    'uidNumber': 12345678,
    'gidNumber': 5000,
    'CN': 'X C 0617',
    'firstName': 'Philip',
    'lastName': 'Chen',
    'password': '{SSHA}http://www.openldap.org/faq/data/cache/347.html',
    'employeeNumber': 'A12345678',
    'workEmail': 'pchen@mydomain.com',
    'loginShell': '/bin/bash',
    'homeDirectory': '/home/pchen'
}
