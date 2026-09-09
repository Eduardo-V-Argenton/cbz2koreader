import zipfile
import xml.etree.ElementTree as ET
import os


def create_metadata(path: str) -> str:
    filename = os.path.basename(path.rstrip('/\\'))
    if filename.lower().endswith('.cbz'):
        title = filename[:-4]
    else:
        title, _ = os.path.splitext(filename)
    root = ET.Element('ComicInfo')
    title_elem = ET.SubElement(root, 'Title')
    title_elem.text = title
    if hasattr(ET, 'indent'):
        ET.indent(root, space="  ")

    return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    

def read_comic_info(cbz_path: str) -> str | None:
    with zipfile.ZipFile(cbz_path, 'r') as zf:
        arquivo_alvo = next((f for f in zf.namelist() if f.lower() == 'comicinfo.xml'), None)
        if not arquivo_alvo:
            return None
        
        return zf.read(arquivo_alvo).decode('utf-8')


def get_element(root, tag):
    element = root.find(tag)
    if element is None:
        element = ET.SubElement(root,tag)
    return element


def update_xml(original_xml : str, tag: str, value: str):
    root = ET.fromstring(original_xml)
    element = get_element(root, tag)
    element.text = value
    return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')


def update_series(original_xml : str, value : str):
    return update_xml(original_xml, "Series", value)


def update_writer(original_xml : str, value : str):
    return update_xml(original_xml, "Writer", value)
    

def update_tags(original_xml : str, value : str):
    return update_xml(original_xml, "Tags", value)


def update_title(original_xml : str, value : str):
    return update_xml(original_xml, "Title", value)


def update_title_auto(original_xml : str, part : int):
    root = ET.fromstring(original_xml)
    element = get_element(root, 'Title')
    element.text = f'{element.text} - {part:03d}'
    return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')


def save_updated_comic_info(cbz_path: str, novo_conteudo_xml: str):
    temp_cbz = cbz_path + ".tmp"
    with zipfile.ZipFile(cbz_path, 'r') as zf_in, \
         zipfile.ZipFile(temp_cbz, 'w', compression=zipfile.ZIP_DEFLATED) as zf_out:
        for item in zf_in.infolist():
            if item.filename.lower() != 'comicinfo.xml':
                zf_out.writestr(item, zf_in.read(item.filename))
        zf_out.writestr('ComicInfo.xml', novo_conteudo_xml.encode('utf-8'))
    os.replace(temp_cbz, cbz_path)