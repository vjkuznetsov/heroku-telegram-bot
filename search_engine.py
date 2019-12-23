import wikipedia
from cinema_bot_exception import CinemaBotException
from serpapi.google_search_results import GoogleSearchResults

WATCH_QUERY_FIXTURE = "смотреть онлайн"
POSTER_QUERY_FIXTURE = "постер"
INFO_PREFIX = "фильм"


def search_watch(message, cfg):
    params = {"q": f"{message} {WATCH_QUERY_FIXTURE}"}
    params.update(cfg)
    try:
        result = _search(params)
        link = result["organic_results"][0]["link"]
        return link
    except Exception as exc:
        raise CinemaBotException(*exc.args)

def search_info(message, cfg):
    find_query = f"{message} {INFO_PREFIX}"
    try:
        wikipedia.set_lang(cfg["language"])
        info = wikipedia.summary(find_query)
        return info
    except Exception as exc:
        raise CinemaBotException(*exc.args)

def search_poster(message, cfg):
    params = {"q": message}
    params.update(cfg)
    params.update({"tbm": "isch"}) # image search
    try:
        result = _search(params)
        link = result["images_results"][0]["original"]
        return link
    except Exception as exc:
        raise CinemaBotException(*exc.args)

def _search(params):
    client = GoogleSearchResults(params)
    return client.get_dict()
