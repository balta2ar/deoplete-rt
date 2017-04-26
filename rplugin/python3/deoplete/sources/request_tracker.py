"""
This is RT source plugin for deoplete. It completes RequestTracker numbers from
a cache file.

# Install:

1. Copy the file to $HOME/.vim/bundle/deoplete.nvim/rplugin/python3/deoplete/sources/
2. pip install regex (https://pypi.python.org/pypi/regex supports cool fuzzy matching)
"""
from .base import Base

#import re
import os
import sys
from time import strftime, time
from pprint import pformat



#from deoplete.util import load_external_module

#current = __file__
#load_external_module(current, 'sources/deoplete_matcher')
#from matcher import MyMatcher, RT_PATTERN, CANDIDATES_FILENAME


MAX_CANDIDATES = 10


def measure(func):

    def deco(*args, **kwargs):
        a = time()
        result = func(*args, **kwargs)
        b = time()
        log('%s running time: %s' % (func.__name__, b - a))
        return result

    return deco


def log(msg):
    if os.environ.get('NVIM_PYTHON_LOG_LEVEL', None) != 'DEBUG':
        return
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    with open('/tmp/rt.completer.log', 'a+') as file_object:
        file_object.write('%s ' % timestamp + msg + '\n')


log('PATH: %s' % sys.path)

import jira_rt_completion_server
from jira_rt_completion_server.deoplete_rt import DeopleteSourceRT


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self._source = DeopleteSourceRT()

        self.debug_enabled = True
        self.name = 'request_tracker'
        #self.kind = 'keyword'
        self.mark = '[RT]'
        #self.min_pattern_length = 2
        self.matchers = []
        self.sorters = []
        #self.converters = []
        self.max_menu_width = 120
        self.max_abbr_width = 120
        self.input_pattern = self._source.input_pattern

    def get_complete_position(self, context):
        return self._source.get_complete_position(context)

    def gather_candidates(self, context):
        return self._source.gather_candidates(context)

    def on_post_filter(self, context):
        return self._source.on_post_filter(context)

# class Source(Base):
#     def __init__(self, vim):
#         Base.__init__(self, vim)
#
#         self.debug_enabled = True
#         self.name = 'request_tracker'
#         #self.kind = 'keyword'
#         self.mark = '[RT]'
#         self.min_pattern_length = 2
#         self.matchers = []
#         self.sorters = []
#         #self.converters = []
#         self.max_menu_width = 120
#         self.max_abbr_width = 120
#         self.input_pattern = RT_PATTERN
#
#         self.mymatcher = MyMatcher(prefixes=['RT:', 'RT'])
#         log('CONSTRUCTOR %s' % self.input_pattern)
#
#     def get_complete_position(self, context):
#         log('GET POS: ' + pformat(context))
#         pos = self.mymatcher.get_complete_position(context)
#         log('GET POS RESULT: ' + pformat(pos))
#         return pos
#
#     @measure
#     def gather_candidates(self, context):
#         log('GATHER: ' + pformat(context))
#         prefix, complete_str = self.mymatcher.get_complete_str(context)
#         log('COMPLETE STR: %s' % complete_str)
#         if prefix is None:
#             return []
#
#         filtered_candidates = self.mymatcher.load_raw_candidates(
#             CANDIDATES_FILENAME, complete_str)
#
#         result = self.mymatcher.prepare_deoplete_candidates(
#             prefix, filtered_candidates)
#         log('GATHER CAND: ' + str(result))
#         log('GATHER CAND COUNT: ' + str(len(result)))
#         return result[:MAX_CANDIDATES]
#
#     @measure
#     def on_post_filter(self, context):
#         log('POST FILTER: ' + pformat(context))
#         prefix, complete_str = self.mymatcher.get_complete_str(context)
#         log('POST FILTER PREFIX: ' + str(prefix) + ' COMPLETE_STR ' + str(complete_str))
#         log('POST FILTER types: %s %s' % (type(prefix), type(complete_str)))
#         candidates = context['candidates']
#         result = candidates
#         if complete_str is not None:
#             result = self.mymatcher.filter_deoplete_candidates(
#                 complete_str, candidates)
#         log('POST FILTER RESULT: ' + pformat(context))
#         log('POST FILTER RESULT LEN: ' + str(len(context)))
#         return result[:MAX_CANDIDATES]
