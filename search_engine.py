import wikipedia

from cinema_bot_exception import CinemaBotException
from serpapi.google_search_results import GoogleSearchResults

WATCH_QUERY_FIXTURE = r"смотреть онлайн"
POSTER_QUERY_FIXTURE = r"постер"
INFO_PREFIX = r"фильм"

# cfg (depends on serp api format)
WATCH_RESULT = "organic_results"
WATCH_CATEGORY = "link"
POS = 0
POSTER_RESULT = "images_results"
POSTER_SIZE = "original"


def watch(message, cfg):
    params = {"q": f"{message} {WATCH_QUERY_FIXTURE}"}
    params.update(cfg)
    try:
        result = _search(params)
        link = result[WATCH_RESULT][POS][WATCH_CATEGORY]
        return link
    except Exception as exc:
        raise CinemaBotException(*exc.args)


def info(message, cfg):
    find_query = f"{message} {INFO_PREFIX}"
    try:
        wikipedia.set_lang(cfg["language"])
        info = wikipedia.summary(find_query)
        return info
    except Exception as exc:
        raise CinemaBotException(*exc.args)


def poster(message, cfg):
    params = {"q": message}
    params.update(cfg)
    params.update({"tbm": "isch"})  # image search
    try:
        result = _search(params)
        link = result[POSTER_RESULT][POS][POSTER_SIZE]
        return link
    except Exception as exc:
        raise CinemaBotException(*exc.args)


def _search(params):
    client = GoogleSearchResults(params)
    return client.get_dict()
