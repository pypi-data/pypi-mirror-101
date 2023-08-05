# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import xmlrpc.client
import ssl

from urllib.parse import urlparse
from trytond.model import ModelView, ModelSQL
from trytond.pool import Pool
from trytond.config import config
from trytond.cache import Cache


#Status
#id,name,order
#1,new,1.0
#2,chatting,2.0
#3,need-eg,3.0
#5,order-approved,8.0
#4,order-waiting-approval,7.0
#6,in-progress,9.0
#7,testing,10.0
#8,resolved,11.0
#9,planning-waiting-approval,4.0
#10,planning-in-progress,6.0
#11,planning-approved,5.0

#Resolution
#id,name,order
#1,done,1.0
#2,duplicate,2.0
#3,invalid,3.0
#4,later,4.0
#5,out of date,5.0
#6,rejected,6.0
#7,wont fix,7.0
#8,works for me,8.0


class IssueTracker(ModelSQL, ModelView):
    'Issue Tracker'
    __name__ = 'issue_tracker'

    _roundup_cache = Cache('issue_tracker.roundup', context=False)

    @classmethod
    def clear_roundup_cache(cls, *args):
        '''
        A method which conveniently clears the cache
         - used in triggers
        '''
        cls._roundup_cache.clear()

    def __init__(self):
        super(IssueTracker, self).__init__()
        self.uri = config.get('roundup', 'uri')
        self.username = config.get('roundup', 'username')
        self.password = config.get('roundup', 'password')
        parsed = urlparse(self.uri)
        self.host = parsed.hostname
        self.port = parsed.port
        self.protocol = parsed.scheme
        url = '%s://%s:%s@%s' % (self.protocol, self.username,
            self.password, self.host)
        if self.port:
            url = '%s:%s' % (url, self.port)
        path = parsed.path
        self.url = '%s%s' % (url, path)
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            if self.protocol == 'https':
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                connection = xmlrpc.client.ServerProxy(
                    self.url, allow_none=True, context=ssl_context)
            elif self.protocol == 'http':
                connection = xmlrpc.client.ServerProxy(
                    self.url, allow_none=True)
            self.connection = connection
        return self.connection

    def check_connection(self):
        try:
            self.get_connection().list('user')
        except Exception as e:
            return False
        return True

    def get_roundup_users(self):
        cache_ru = self._roundup_cache.get('users')
        if cache_ru is not None:
            return cache_ru
        connection = self.get_connection()
        roundup_users = {}
        user_ids = connection.list('user', 'id')
        for user_id in user_ids:
            user = connection.display('user%s' % (user_id,),
                'username', 'address')
            roundup_users.setdefault(user_id, {})
            roundup_users[user_id]['username'] = user['username']
            roundup_users[user_id]['email'] = user['address']
        self._roundup_cache.set('users', roundup_users)
        return roundup_users

    def get_roundup_states(self):
        cache_rs = self._roundup_cache.get('states')
        if cache_rs is not None:
            return cache_rs
        connection = self.get_connection()
        states = {None: None}
        state_ids = connection.list('status', 'id')
        for state_id in state_ids:
            state = connection.display('status%s' % (state_id,),
                'name')
            states[state_id] = state['name']
        self._roundup_cache.set('states', states)
        return states

    def get_roundup_organisations(self, organisation_ids=[]):
        cache_ro = self._roundup_cache.get('organisations')
        if cache_ro is not None:
            return cache_ro
        connection = self.get_connection()
        organisations = {}
        if not organisation_ids:
            organisation_ids = connection.list('organisation', 'id')
        for organisation_id in organisation_ids:
            organisation = connection.display('organisation%s' % (
                    organisation_id,), 'code')
            organisations[organisation_id] = organisation['code']
        self._roundup_cache.set('organisations', organisations)
        return organisations

    def get_organisation_for_party(self, party_id):
        connection = self.get_connection()
        return connection.filter('organisation', None, {'code': party_id})

    def get_tickets_for_organisation(self, organisation_id):
        connection = self.get_connection()
        return connection.filter('issue', None,
            {'organisations': organisation_id})

    def get_tickets(self, ticket_ids=[], use_cache=True):
        connection = self.get_connection()
        users = self.get_roundup_users()
        if not ticket_ids:
            ticket_ids = connection.list('issue', 'id')

        if not use_cache:
            self.clear_roundup_cache()
        users = self.get_roundup_users()
        organisations = self.get_roundup_organisations()
        states = self.get_roundup_states()

        tickets = []
        for ticket_id in ticket_ids:
            data = connection.display('issue%s' % (ticket_id,),
                'status', 'activity', 'id', 'organisations', 'assignedto',
                'title', 'project')
            ticket = {
                'id': ticket_id,
                'title': data['title'],
                'status': states[data['status']],
                'project': data['project'],
                'activity': data['activity'],
                }
            if data.get('assignedto'):
                ticket['assignedto'] = \
                    users[data['assignedto']]['username']
            if data.get('creator'):
                ticket['creator'] = \
                    users[data['creator']]['email']
            if data.get('organisations'):
                org_codes = []
                for org_id in data['organisations']:
                    org_codes.append(organisations[org_id])
                ticket['organisations'] = org_codes
            tickets.append(ticket)
        return tickets

    def synchronize_tickets(self, ticket_ids=[], use_cache=True):
        pool = Pool()
        Project = pool.get('project.work')

        tickets = self.get_tickets(ticket_ids=ticket_ids, use_cache=use_cache)
        for ticket in tickets:
            task = Project.sync_roundup_task(ticket)

    @classmethod
    def cron_synchronize_tickets(cls):
        pool = Pool()
        Tracker = pool.get('issue_tracker')
        Tracker().synchronize_tickets(use_cache=False)
