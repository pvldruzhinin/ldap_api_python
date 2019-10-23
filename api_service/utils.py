import re

import ldap
import ldap.filter

from ldap_api.constants import LDAP_USER, LDAP_PASSW, LDAP_SERVER, GROUP_SEARCH_PATTERN


def get_user_dn(account_name):
    criteria = f'(&(objectClass=user)(sAMAccountName={account_name}))'
    attributes = ['dn']
    request_result = make_ldap_request(criteria, attributes)

    if request_result:
        user_dn_name = request_result[0][0]
        return user_dn_name
    raise Exception(f'No users were found with sAMAccountName={account_name}')


def get_user_pnac_groups(account_name):
    user_dn_name = get_user_dn(account_name)
    criteria = f'(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={user_dn_name}))'
    attributes = ['cn']
    request_result = make_ldap_request(criteria, attributes)
    if request_result:
        results = [str(entry.get('cn')[0], 'utf-8') for dn, entry in request_result if isinstance(entry, dict)]
        pnac_groups = [group_name for group_name in results if GROUP_SEARCH_PATTERN in group_name]
        return pnac_groups
    raise Exception(f'No groups were found with sAMAccountName={account_name}')


def get_group_users(group_name):
    group_dn_name = get_group_dn(group_name)

    criteria = f'(&(objectClass=user)(memberOf:1.2.840.113556.1.4.1941:={group_dn_name}))'
    attributes = ['sAMAccountName']

    request_result = make_ldap_request(criteria, attributes)
    if request_result:
        samaccountnames_list = []
        raw_users_list = [entry for dn, entry in request_result if isinstance(entry, dict)]
        for entry in raw_users_list:
            value = entry.get('sAMAccountName')
            account_name = str(value[0], 'utf-8')
            samaccountnames_list.append(account_name)
        return samaccountnames_list
    raise Exception(f'No users were found in group DN={group_dn_name}')


def get_group_dn(group_name):
    criteria = f'(&(objectClass=group)(cn={group_name}))'
    attributes = ['dn']
    request_result = make_ldap_request(criteria, attributes)

    if request_result:
        group_dn_name = request_result[0][0]
        return group_dn_name
    raise Exception(f'No groups were found with CN={group_name}')


def make_ldap_request(criteria=None, attributes=None):
    conn = ldap.initialize(LDAP_SERVER)

    user_dn = LDAP_USER
    password = LDAP_PASSW

    try:
        conn.simple_bind_s(user_dn, password)
        base = 'Ou=Mail,dc=mail,dc=msk'
        query_result = conn.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
        return query_result
    except Exception as e:
        msg = e
    raise Exception(f'Something went wrong with LDAP request: {msg}')
