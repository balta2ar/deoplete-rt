"""
This is RT source plugin for deoplete. It completes RequestTracker numbers from
a cache file.

# Install:

1. Copy the file to $HOME/.vim/bundle/deoplete.nvim/rplugin/python3/deoplete/sources/
2. pip install regex (https://pypi.python.org/pypi/regex supports cool fuzzy matching)
"""
from .base import Base

#import re
from os import expanduser
import regex as re
from time import strftime, time
from pprint import pformat

#CANDIDATES_FILENAME = '/tmp/rt.candidates.txt'
CANDIDATES_FILENAME = '~/.cache/rt/rt.candidates.txt'
RT_PATTERN = r'RT:?\w*$'
RX_RT = re.compile(RT_PATTERN, re.IGNORECASE)


def measure(func):

    def deco(*args, **kwargs):
        a = time()
        result = func(*args, **kwargs)
        b = time()
        log('%s running time: %s' % (func.__name__, b - a))
        return result

    return deco


def log(msg):
    return
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    with open('/tmp/rt.completer.log', 'a+') as file_object:
        file_object.write('%s ' % timestamp + msg + '\n')


# Taken from: https://github.com/amjith/fuzzyfinder
def fuzzyfinder(text, collection):
    suggestions = []
    text = str(text) if not isinstance(text, str) else text
    #pat = '.*?'.join(map(re.escape, text))
    pat = '(?:%s){i}' % text
    regex = re.compile(pat, re.IGNORECASE | re.BESTMATCH)
    for item in collection:
        r = regex.search(item)
        if r:
            suggestions.append((len(r.group()), r.start(), item))

    return [z for _, _, z in sorted(suggestions)]


def read_candidates(filename):
    with open(filename) as file_object:
        lines = file_object.readlines()
        candidates = [str(line.strip()) for line in lines]
        return candidates


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'request_tracker'
        #self.kind = 'keyword'
        self.mark = '[RT]'
        self.min_pattern_length = 2
        self.matchers = []
        self.sorters = []
        self.max_menu_width = 120
        self.max_abbr_width = 120
        self.input_pattern = RT_PATTERN

    def get_complete_position(self, context):
        log('GET POS: ' + pformat(context))
        match = RX_RT.search(context['input'])
        pos = match.start() if match else -1
        log('GET POS RESULT: ' + pformat(pos))
        return pos

    @measure
    def gather_candidates(self, context):
        log('GATHER: ' + pformat(context))

        # Cut off and remember RT prefix
        complete_str = context['complete_str']
        if complete_str.startswith('RT:'):
            prefix = 'RT:'
            complete_str = complete_str[3:]
        elif complete_str.startswith('RT'):
            prefix = 'RT'
            complete_str = complete_str[2:]
        else:
            log('NO PREFIX FOUND')
            return []
        log('COMPLETE STR: %s' % complete_str)

        # Read candidates, cut off http part and fuzzy match by long description
        candidates_from_file = read_candidates(CANDIDATES_FILENAME)
        candidates_without_http = []
        for candidate in candidates_from_file:
            pos = candidate.find(' http')
            candidates_without_http.append(candidate[:pos] if pos != -1 else candidate)

        if len(complete_str):
            filtered_candidates = fuzzyfinder(complete_str, candidates_without_http)
        else:
            filtered_candidates = sorted(candidates_without_http, reverse=True)

        result = []
        for x in filtered_candidates:
            short = prefix + x[:6]
            long = prefix + x
            item = {'word': short, 'abbr': long}
            result.append(item)

        log('GATHER CAND: ' + str(result))
        return result
