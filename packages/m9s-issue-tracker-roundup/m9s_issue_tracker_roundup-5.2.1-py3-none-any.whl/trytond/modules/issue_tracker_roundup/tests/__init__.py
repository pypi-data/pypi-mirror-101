# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.issue_tracker_roundup.tests.test_issue_tracker_roundup import suite
except ImportError:
    from .test_issue_tracker_roundup import suite

__all__ = ['suite']
