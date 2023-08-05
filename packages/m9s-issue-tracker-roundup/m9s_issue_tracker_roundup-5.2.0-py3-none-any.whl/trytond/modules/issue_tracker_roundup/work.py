# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from datetime import datetime

from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.rpc import RPC
from trytond.exceptions import UserError, UserWarning
from trytond.i18n import gettext

ROUNDUP_STATUS_MAP = {
    # roundup-status: tryton-status
    None: 'opened',
    'new': 'opened',
    'chatting': 'opened',
    'need-eg': 'opened',
    'order-approved': 'opened',
    'order-waiting-approval': 'opened',
    'in-progress': 'opened',
    'testing': 'opened',
    'resolved': 'done',
    'planning-waiting-approval': 'opened',
    'planning-in-progress': 'opened',
    'planning-approved': 'opened',
}

# Roundup Date Format from XMLRPC <Date 2011-09-02.08:11:27.559>
ROUNDUP_DATE_FORMAT = '<Date %Y-%m-%d.%H:%M:%S.%f>'
EMPTY_ROUNDUP_ID = ' - '


def _convert_roundup_date(date):
    # Roundup Date Format from XMLRPC can come in several formats
    # <Date 2011-09-02.08:11:27.559> or '2019-10-19.00:33:28'
    try:
        return datetime.strptime(date,
            ROUNDUP_DATE_FORMAT).replace(microsecond=0)
    except:
        return datetime.strptime(date, '%Y-%m-%d.%H:%M:%S')


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    roundup_id = fields.Char('Roundup ID',
        readonly=True,
        help='Identfier of the related issue on roundup')
    employee = fields.Many2One('company.employee', 'Employee',
        domain=[('company', '=', Eval('company'))],
        depends=['company'],
        help='Employee who is assigned the issue.')
    last_sync = fields.DateTime('Last Tracker Sync',
        readonly=True)
    roundup_name = fields.Function(fields.Char('Name'),
        'get_roundup_name')

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls.__rpc__['sync_roundup_task'] = RPC(readonly=False)
        cls._order.insert(0, ('roundup_id', 'ASC'))
        cls.state.selection.append(('closed', 'Closed'))

    @classmethod
    def write(cls, *args):
        super(Work, cls).write(*args)
        cls.manage_closed_projects(sum(args[::2], []))

    @classmethod
    def manage_closed_projects(cls, works):

        def get_subprojects(work, state):
            subs = []
            for child in work.children:
                if child.state == state:
                    subs.append(child)
                subs.extend(get_subprojects(child, state))
            return subs

        switch_state = {
            'opened': 'closed',
            'closed': 'opened',
            }
        for work in set(works):
            if work.type == 'project':
                to_write = []
                if work.state in list(switch_state.keys()):
                    to_write = get_subprojects(work, switch_state[work.state])
                if to_write:
                    cls.write(to_write, {'state': work.state})

    def get_rec_name(self, name):
        rec_name = super(Work, self).get_rec_name(name)
        if self.roundup_id and self.roundup_id != EMPTY_ROUNDUP_ID:
            rec_name = '[%s] %s' % (self.roundup_id, rec_name)
        return rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super(Work, cls).search_rec_name(name, clause)
        return ['OR',
            domain,
            ('roundup_id',) + tuple(clause[1:]),
            ]

    @classmethod
    def get_roundup_name(cls, works, names):
        result = {}
        for name in names:
            values = {w.id: '[%s] %s' % (w.roundup_id, w.name) if w.roundup_id
                else w.name for w in works}
            result[name] = values
        return result

    @classmethod
    def _get_roundup_project(cls, party):
        pool = Pool()
        Project = pool.get('project.work')
        Lang = pool.get('ir.lang')
        Configuration = pool.get('project.roundup.configuration')

        transaction = Transaction()
        configuration = Configuration(1)

        lang, = Lang.search([
                    ('code', '=', transaction.language),
                ], limit=1)
        now = datetime.now().strftime(str(lang.date) + " %H:%M")
        project = Project()
        project.type = 'project'
        prefix = (configuration.default_project_prefix
            or configuration.default_default_project_prefix())
        project.name = '%s %s (%s)' % (prefix, party.name, now)
        project.company = transaction.context.get('company')
        project.party = party
        project.project_invoice_method = configuration.default_invoice_method
        project.state = 'opened'
        project.roundup_id = EMPTY_ROUNDUP_ID
        project.product = configuration.billing_product
        project.save()
        return project

    @classmethod
    def sync_roundup_project(cls, party_code):
        pool = Pool()
        Party = pool.get('party.party')

        parties = Party.search([
                ('code', '=', party_code),
                ])
        if not parties:
            warning_name = 'no_party_for_project_%s' % party_code
            raise UserWarning(warning_name,
                gettext('issue_tracker_roundup.no_party_for_project',
                party_code=party_code))
            return None
        party = parties[0]

        projects = cls.search([
                ('party', '=', party.id),
                ('state', '=', 'opened'),
                ('parent', '=', None),
                ('roundup_id', '=', EMPTY_ROUNDUP_ID),
                ])
        if len(projects) > 1:
            open_projects = '\n'.join([' '.join([p.id, p.name]
                        for p in projects)])
            raise UserError(gettext(
                        'issue_tracker_roundup.multiple_roundup_projects',
                        projects=open_projects))
        elif len(projects) == 1:
            project = projects[0]
        else:
            project = cls._get_roundup_project(party)
        return project

    @classmethod
    def sync_roundup_task(cls, ticket):
        '''
        If a task with same id exists, update the task.
        Otherwise create a new task.
        '''
        pool = Pool()
        Project = pool.get('project.work')
        Company = pool.get('company.company')
        Employee = pool.get('company.employee')
        Configuration = pool.get('project.roundup.configuration')

        transaction = Transaction()

        tasks = cls.search([
                ('roundup_id', '=', str(ticket['id'])),
                ])
        if len(tasks) > 1:
            error_tasks = '\n'.join([' '.join([t.id, t.name]
                        for t in tasks)])
            raise UserError(gettext(
                        'issue_tracker_roundup.multiple_roundup_tasks',
                        tasks=error_tasks))
        elif len(tasks) == 1:
            task = tasks[0]
            # force_update provides a mean to skip the sync required check
            if (not task._sync_required(ticket)
                    and not ticket.get('force_update')):
                return task.id
        else:
            task = Project()
        task.type = 'task'
        task_company = transaction.context.get('company')
        task.company = task_company
        # Assign a project in any case
        projects = []
        if ticket.get('organisations'):
            for org_code in ticket['organisations']:
                if org_code is not None:
                    project = cls.sync_roundup_project(org_code)
                    projects.append(project)
        # Use default project if none was found
        if projects:
            # XXX Fixme: multiple projects?
            project = projects[0]
        else:
            company_code = Company(task_company).party.code
            project = cls.sync_roundup_project(company_code)
        task.parent = project

        if not hasattr(task, 'product'):
            configuration = Configuration(1)
            task.product = configuration.billing_product
            task.on_change_product()
        task.name = ticket['title']
        task.roundup_id = str(ticket['id'])
        task.state = ROUNDUP_STATUS_MAP[ticket['status']]
        if ticket.get('assignedto'):
            employees = Employee.search([
                    ('roundup_user', '=', ticket['assignedto']),
                    ])
            if employees:
                task.employee = employees[0]
        task.last_sync = _convert_roundup_date(ticket['activity'])
        task.save()
        return task.id

    def _sync_required(self, ticket):
        # Roundup Date Format from XMLRPC <Date 2011-09-02.08:11:27.559>
        if ticket.get('activity', None):
            last_activity = _convert_roundup_date(ticket['activity'])
            if (self.last_sync
                    and (self.last_sync >= last_activity)):
                return False
        return True


class SynchronizeTicketsAskChildren(ModelView):
    'Synchronize TicketsAsk Children'
    __name__ = 'project.work.synchronize_tickets.ask_children'

    with_children = fields.Boolean('Synchronize Children',
        help='Also synchronize all children of the selected projects/tasks.')

    @staticmethod
    def default_with_children():
        return True


class SynchronizeTickets(Wizard):
    'Synchronize Tickets'
    __name__ = 'project.work.synchronize_tickets'
    start_state = 'synchronize'
    synchronize = StateTransition()
    ask_children = StateView(
        'project.work.synchronize_tickets.ask_children',
        'issue_tracker_roundup.roundup_synchronize_ask_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Synchronize', 'synchronize_with_children',
                'tryton-ok', default=True),
            ])
    synchronize_with_children = StateTransition()

    def transition_synchronize(self):
        pool = Pool()
        Tracker = pool.get('issue_tracker')
        Work = pool.get('project.work')

        context = Transaction().context
        if context['active_model'] == 'ir.ui.menu':
            Tracker().synchronize_tickets()
            return 'end'
        elif context['active_model'] == 'project.work':
            works = Work.browse(context['active_ids'])
            if any([w for w in works if w.children]):
                return 'ask_children'
            else:
                self.synchronize_tickets(works)
                return 'end'

    def transition_synchronize_with_children(self):
        pool = Pool()
        Work = pool.get('project.work')

        context = Transaction().context
        works = Work.browse(context['active_ids'])
        all_works = set(works)
        if self.ask_children.with_children:
            for work in works:
                child_works = Work.search([
                        ('parent', 'child_of', work.id),
                        ])
                all_works.update(set(child_works))
        self.synchronize_tickets(all_works)
        return 'end'

    def synchronize_tickets(self, works):
        pool = Pool()
        Tracker = pool.get('issue_tracker')

        ticket_ids = [w.roundup_id for w in works
            if w.roundup_id != EMPTY_ROUNDUP_ID]
        Tracker().synchronize_tickets(ticket_ids=ticket_ids)
        #with Transaction().set_context(
        #        queue_name='roundup'):
        #    Tracker.__queue__.synchronize_tickets(1)
        #    #cls.__queue__.process(sales)


class RefreshProjects(Wizard):
    'Synchronize Tickets'
    __name__ = 'project.work.refresh_project_tickets'
    start_state = 'refresh'
    refresh = StateTransition()

    def transition_refresh(self):
        pool = Pool()
        Tracker = pool.get('issue_tracker')
        Work = pool.get('project.work')

        context = Transaction().context
        works = Work.browse(context['active_ids'])
        party_codes = list(set([str(w.party.code) for w in works]))

        tracker = Tracker()
        for code in party_codes:
            organisation = tracker.get_organisation_for_party(code)
            if organisation:
                ticket_ids = tracker.get_tickets_for_organisation(organisation)
                if ticket_ids:
                    tracker.synchronize_tickets(ticket_ids=ticket_ids)
        return 'end'
