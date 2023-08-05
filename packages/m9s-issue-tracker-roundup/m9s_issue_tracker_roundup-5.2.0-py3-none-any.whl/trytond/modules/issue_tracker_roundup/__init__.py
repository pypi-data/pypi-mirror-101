# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import company
from . import ir
from . import tracker
from . import work

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        company.Employee,
        ir.Cron,
        tracker.IssueTracker,
        work.SynchronizeTicketsAskChildren,
        work.Work,
        module='issue_tracker_roundup', type_='model')
    Pool.register(
        work.RefreshProjects,
        work.SynchronizeTickets,
        module='issue_tracker_roundup', type_='wizard')
