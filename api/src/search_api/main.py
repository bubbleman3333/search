import sys
import time
from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

sys.path.append('C:\\Users\\aiueo\\Desktop\\search\\django-dev\\engine\\api')
from src.es.elastic import ElasticsearchClient
from src.model.shotcut_data import ShortcutData

app = FastAPI()
origins = ["http://localhost:3000", ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
elasticsearch_client = ElasticsearchClient()


@app.get("/search")
async def test(q: Union[str, None] = None):
    ret = elasticsearch_client.search(q)
    return ret


# @app.post("/register_word/")
# async def register(data: Union[None, dict] = None):
#     print("here")
#     print(data)
@app.post("/register_word/")
async def register(data: ShortcutData):
    status = elasticsearch_client.create_short_cut(data)
    return status


