import re
from src.es.elastic import ElasticsearchClient

s = "ctrlx"

es = ElasticsearchClient()
import time
start = time.time()
print(es.convert_short_cut(s))
print(time.time()-start)