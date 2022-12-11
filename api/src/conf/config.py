import pathlib

BASE_PATH = pathlib.Path(__file__).parent.parent.parent.parent
SECRET_PATH = BASE_PATH.with_name("secret")

ES_HOST = "http://127.0.0.1:9200/"

