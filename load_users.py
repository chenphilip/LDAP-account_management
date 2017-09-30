#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This will create user accounts in OpenLDAP

"""
import csv
import ldap3 as ldap
from mydomainLDAP import *

__author__ = "Philip Chen"
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

# searchFilter = '(objectClass=inetOrgPerson)'
# searchFilter = '(objectClass=*)'
def isUserExist(newEmployeeNumber):
    searchFilter = '(&(objectclass=posixAccount)(employeeNumber={}))'.format(newEmployeeNumber)
    if connLDAP.search(search_base=BASE_DN, search_filter=searchFilter, search_scope=ldap.SUBTREE, attributes=['employeeNumber','givenName']):
        for entry in connLDAP.response:
            print(entry['dn'], entry['attributes']['givenName'])
        return True
    else:
        return False

nCount = 0
with open('user_list.csv', newline='') as acctInputFile:
    csvAcctReader = csv.reader(acctInputFile, delimiter=',', quotechar='"')
    for arrayAcctInfo in csvAcctReader:
        userInfo['employeeNumber'] = arrayAcctInfo[0]
        userInfo['firstName'] = arrayAcctInfo[1]
        userInfo['lastName'] = arrayAcctInfo[2]
        userInfo['workEmail'] = arrayAcctInfo[5]
        userInfo['uidLDAP'] = userInfo['workEmail'].split("@")[0]
        # userInfo['uidLDAP'] = arrayAcctInfo[0]
        emailExternal = arrayAcctInfo[6]
        # plainPassword = arrayAcctInfo[7]
        nCount += 1

        # userInfo['uidNumber'] = int(userInfo['employeeNumber'][1:])
        userInfo['uidNumber'] = nCount + 10000
        newUserDN = 'uid={},{}'.format(userInfo['uidLDAP'], BASE_DN)
        userInfo['CN'] = '{} {}'.format(userInfo['firstName'], userInfo['lastName'])
        # Using SASL for pass-through authentication
        userInfo['password'] = '{{SASL}}{}'.format(userInfo['employeeNumber'])
        userInfo['loginShell'] = '/bin/bash'
        userInfo['homeDirectory'] = '/home/{}'.format(userInfo['employeeNumber'].lower())

        if isUserExist(userInfo['employeeNumber']):
            print('The user {} exist in LDAP already'.format(userInfo['CN']))
            continue
        else:
            connLDAP.add(newUserDN, ['inetOrgPerson', 'posixAccount', 'shadowAccount'],
                         {'uid': userInfo['uidLDAP'], 'givenName': userInfo['firstName'], 'sn': userInfo['lastName'],
                          'userPassword': userInfo['password'], 'cn': userInfo['CN'],
                          'uidNumber': userInfo['uidNumber'], 'gidNumber': userInfo['gidNumber'],
                          'loginShell': userInfo['loginShell'], 'homeDirectory': userInfo['homeDirectory'],
                          'employeeNumber': userInfo['employeeNumber'], 'mail': userInfo['workEmail']
                          })

        print (userInfo, emailExternal)

connLDAP.unbind()
