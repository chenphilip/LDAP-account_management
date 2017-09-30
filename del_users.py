#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This will delete user accounts in OpenLDAP

"""
import csv
import ldap3 as ldap
from mydomainLDAP import *__author__ = "Philip Chen"

__license__ = "https://opensource.org/licenses/GPL-3.0 GPL-3.0 License"
__date__ = "2016.07.08"
__version__ = "1.0.0"
__status__ = "Tested on Python 3.5, OpenLDAP 2.4 on Centos 7"

# ldapGlad = ldap.Server(LDAP_URI, port=389, get_info=ldap.ALL)
ldapGlad = ldap.Server(LDAP_URI, port=636, use_ssl=True)
connLDAP = ldap.Connection(ldapGlad, authentication=ldap.AUTH_SIMPLE, user=BIND_USER['DN'], password=BIND_USER['password'], check_names=True, lazy=False, client_strategy=ldap.STRATEGY_SYNC, raise_exceptions=True)
connLDAP.open()
if not connLDAP.bind():
    print('error in bind', connLDAP.result)

def isUserExist(newEmployeeNumber):
    searchFilter = '(&(objectclass=posixAccount)(employeeNumber={}))'.format(newEmployeeNumber)
    if connLDAP.search(search_base=BASE_DN, search_filter=searchFilter, search_scope=ldap.SUBTREE, attributes=['employeeNumber','givenName']):
        for entry in connLDAP.response:
            print(entry['dn'], entry['attributes']['givenName'])
        return True
    else:
        return False

with open('user_list.csv', newline='') as acctInputFile:
    csvAcctReader = csv.reader(acctInputFile, delimiter=',', quotechar='"')
    for arrayAcctInfo in csvAcctReader:
        userInfo['employeeNumber'] = arrayAcctInfo[0]
        userInfo['workEmail'] = arrayAcctInfo[5]
        userInfo['uidLDAP'] = userInfo['workEmail'].split("@")[0]
        userDN = 'uid={},{}'.format(userInfo['uidLDAP'], BASE_DN)
        # userDN = 'employeeNumber={},{}'.format(userInfo['employeeNumber'], BASE_DN)
        # print(userDN)

        if isUserExist(userInfo['employeeNumber']):
            connLDAP.delete(userDN)
            print(connLDAP.result)
        else:
            print('The user {} does NOT exist in LDAP'.format(userInfo['employeeNumber']))
            continue

        # print(userInfo, emailExternal)

connLDAP.unbind()
