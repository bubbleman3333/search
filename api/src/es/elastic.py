from src.conf import config
from elasticsearch import Elasticsearch
import re


class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(config.ES_HOST)

    def search(self, q):
        key_list = self.convert_short_cut(q)
        if len(key_list) == 0:
            return {"status": "failure"}
        body = {
            "query": {
                "bool": {
                    "must": [
                    ]
                }
            }
        }
        for key in key_list:
            body["query"]["bool"]["must"].append(self.create_match("short_cut", key))
        hits = self.es.search(index="shortcut", body=body, size=10)["hits"]
        if hits["total"]["value"] == 0:
            return {"status": "failure"}
        return {"status": "success", "hits": hits}

    def put_hello(self):
        return

    def create_hello(self, q):
        body = {
            "name": q,
            "age": len(q)
        }
        self.es.index(index="hello", body=body)

    @staticmethod
    def convert_short_cut(short_cut) -> set:
        short_cut = short_cut.lower()
        s = set()
        if "ctrl" in short_cut:
            s.add("Ctrl")
            short_cut = short_cut.replace("ctrl", "")
        elif "ctl" in short_cut:
            s.add("Ctrl")
            short_cut = short_cut.replace("ctl", "")
        elif "ct" in short_cut:
            s.add("Ctrl")
            short_cut = short_cut.replace("ct", "")
        elif "cl" in short_cut:
            s.add("Ctrl")
            short_cut = short_cut.replace("cl", "")

        if "shift" in short_cut:
            s.add("Shift")
            short_cut = short_cut.replace("shift", "")
        elif "sht" in short_cut:
            s.add("Shift")
            short_cut = short_cut.replace("sht", "")
        elif "sft" in short_cut:
            s.add("Shift")
            short_cut = short_cut.replace("sft", "")
        elif "st" in short_cut:
            s.add("Shift")
            short_cut = short_cut.replace("st", "")

        if "alt" in short_cut:
            s.add("Alt")
            short_cut = short_cut.replace("alt", "")
        elif "at" in short_cut:
            s.add("Alt")
            short_cut = short_cut.replace("at", "")

        match = re.search("(f[0-9]{1,2})([^0-9])", short_cut)
        if match:
            str_num = match.group(1)
            num = int(str_num[1:])
            if 1 <= num <= 12:
                s.add(str_num)
                short_cut = short_cut.replace(str_num, "")
            else:
                return set()

        if "tab" in short_cut:
            s.add("Tab")
            short_cut = short_cut.replace("tab", "")
        elif "tb" in short_cut:
            s.add("Tab")
            short_cut = short_cut.replace("tb", "")

        short_cut = short_cut.replace(" ", "")
        short_cut = short_cut.replace("\t", "")
        short_cut = short_cut.replace("\n", "")

        if not re.fullmatch("[a-z]*", short_cut):
            return set()

        s = s.union(set(re.findall("[A-Z]", short_cut.upper())))

        return s

    def create_short_cut(self, data):
        short_cut = data.short_cut
        usage = data.usage
        description = data.shortcut_description
        ref_url = data.ref_url

        keys = list(self.convert_short_cut(short_cut))
        if len(keys) == 0:
            return {"status": "Failure,command is invalid or empty."}
        if len(usage) == 0:
            return {"status": "Failure,usage is empty."}
        if len(description) == 0:
            return {"status": "Failure,description is empty."}

        body = {
            "short_cut": keys,
            "usage": usage,
            "description": description,
            "ref_url": ref_url
        }

        self.es.index(index="shortcut", body=body)

    @staticmethod
    def create_match(field, q):
        return {"match": {field: q}}
