#!/usr/bin/python3
import re


class FilterModule:
    def filters(self):
        return {'any_regex_matches': self.any_regex_matches}

    def any_regex_matches(self, text, regex_list) -> bool:
        return any([re.match(regex, text) for regex in regex_list])
