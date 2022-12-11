from pydantic import BaseModel


class ShortcutData(BaseModel):
    short_cut: str
    usage: str
    ref_url: str
    shortcut_description: str
