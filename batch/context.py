#!/usr/bin/env python3


class Context(object):
    """Context for operations on an individual repository."""
    def __init__(self, args, summary, alias_pool):
        """
        :param args: return value from argparse
        :param summary: pandas CSV object
        :param alias_pool: list
        """
        super(Context, self).__init__()
        self.args = args
        self.summary = summary
        self.alias_pool = alias_pool

