
import zipfile
import xml.etree.ElementTree as ET

def get_comic_info(cbz_path: str) -> str | None:
    with zipfile.ZipFile(cbz_path, 'r') as zf:
        arquivo_alvo = next((f for f in zf.namelist() if f.lower() == 'comicinfo.xml'), None)
        if not arquivo_alvo:
            return None
        
        return zf.read(arquivo_alvo).decode('utf-8')


def get_tag(comic_info : str, tag : str) -> str:
    root = ET.fromstring(comic_info)
    element = root.find(tag)
    if element is None:
        return ""
    return element.text


def get_title(comic_info : str) -> str:
    return get_tag(comic_info, "Title")

def get_series(comic_info : str) -> str:
    return get_tag(comic_info, "Series")

def get_writer(comic_info : str) -> str:
    return get_tag(comic_info, "Writer")

def get_tags(comic_info : str) -> str:
    return get_tag(comic_info, "Tags")

def get_number(comic_info : str) -> str:
    return get_tag(comic_info, "Number")