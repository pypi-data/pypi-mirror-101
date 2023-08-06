from pronomial import replace_corefs
from intentBox.coreference.base import CoreferenceSolver


class PronounCoreferenceSolver(CoreferenceSolver):

    @classmethod
    def solve_corefs(cls, text, lang="en"):
        return replace_corefs(text, lang="en")
