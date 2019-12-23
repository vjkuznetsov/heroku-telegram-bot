import wikipedia
from serpapi.google_search_results import GoogleSearchResults

WATCH_QUERY_FIXTURE = "смотреть онлайн"
POSTER_QUERY_FIXTURE = "постер"
INFO_PREFIX = "фильм"


def search_watch(message, cfg):
    params = {"q": f"{message} {WATCH_QUERY_FIXTURE}"}
    params.update(cfg["search_engine"])
    client = GoogleSearchResults(params)
    result = client.get_dict()
    return result["organic_results"][0]["link"]

def search_info(message, cfg):
    wikipedia.set_lang(cfg["search_engine"]["language"])
    return wikipedia.summary(f"{message} {INFO_PREFIX}")

def search_poster(message, cfg):
    params = {"q": message}
    params.update(cfg["search_engine"])
    params.update({"tbm": "isch"}) # image search
    client = GoogleSearchResults(params)
    result = client.get_dict()
    return result["image_results"][0]["original"]
