api_version = "v58.0"


def create(object):
    return "/services/data/" + api_version + "/sobjects/" + object


def login():
    return "/services/oauth2/token"


def query():
    return "/services/data/" + api_version + "/query/"


def describe(object):
    return "/services/data/" + api_version + "/sobjects/" + object + "/describe"


def retrieve(object, id):
    return "/services/data/" + api_version + "/sobjects/" + object + "/" + id
