"""
This is RT source plugin for deoplete. It completes RequestTracker numbers from
a cache file.

# Install:

1. Copy the file to $HOME/.vim/bundle/deoplete.nvim/rplugin/python3/deoplete/sources/
2. pip install regex (https://pypi.python.org/pypi/regex supports cool fuzzy matching)
"""
from .base import Base

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

        # Use these options if you want to filter candidates yourself
        self.is_volatile = True
        self.matchers = []
        self.sorters = []

        # Use these options if you want to implement custom matcher
        #self.matchers = ['matcher_fuzzy', 'matcher_full_fuzzy']
        #self.sorters = ['sorter_rank']
        #self.converters = []

        self.max_menu_width = 120
        self.max_abbr_width = 120
        self.input_pattern = self._source.input_pattern

    def get_complete_position(self, context):
        return self._source.get_complete_position(context)

    def gather_candidates(self, context):
        ready, result = self._source.async_gather_candidates(context)
        context['is_async'] = not ready
        return result

    def old_gather_candidates(self, context):
        return self._source.gather_candidates(context)

    # def on_post_filter(self, context):
    #     return self._source.on_post_filter(context)
