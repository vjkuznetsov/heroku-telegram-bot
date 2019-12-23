import wikipedia
from serpapi.google_search_results import GoogleSearchResults

WATCH_QUERY_FIXTURE = "смотреть онлайн"
POSTER_QUERY_FIXTURE = "постер"
INFO_PREFIX = "фильм"


def search_watch(message, cfg):
    params = {"q": f"{message} {WATCH_QUERY_FIXTURE}"}
    params.update(cfg["search_engine"])
    print(params)
    client = GoogleSearchResults(params)
    result = client.get_dict()
    print(result)
    return result["organic_results"][0]["link"]

def search_info(message, cfg):
    wikipedia.set_lang(cfg["search_engine"]["language"])
    find_query = f"{message} {INFO_PREFIX}"
    print(find_query)
    return wikipedia.summary(find_query)

def search_poster(message, cfg):
    params = {"q": message}
    params.update(cfg["search_engine"])
    params.update({"tbm": "isch"}) # image search
    print(params)
    client = GoogleSearchResults(params)
    result = client.get_dict()
    print(result)
    return result["image_results"][0]["original"]
