import zipfile
import xml.etree.ElementTree as ET
import os


def create_comic_info(path: str) -> str:
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
    

def update_xml(original_comic_info : str, tag: str, value: str) -> str:
    root = ET.fromstring(original_comic_info)
    element = root.find(tag)
    if element is None:
        element = ET.SubElement(root,tag)
    element.text = value
    return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')


def update_series(original_comic_info : str, value : str) -> str:
    return update_xml(original_comic_info, "Series", value)


def update_writer(original_comic_info : str, value : str) -> str:
    return update_xml(original_comic_info, "Writer", value)
    

def update_tags(original_comic_info : str, value : str) -> str:
    return update_xml(original_comic_info, "Tags", value)


def update_title(original_comic_info : str, value : str) -> str:
    return update_xml(original_comic_info, "Title", value)


def update_number(original_comic_info : str, value : float) -> str:
    return update_xml(original_comic_info, "Number", value)


def save_updated_comic_info(cbz_path: str, new_comic_info: str) -> None:
    temp_cbz = cbz_path + ".tmp"
    with zipfile.ZipFile(cbz_path, 'r') as zf_in, \
         zipfile.ZipFile(temp_cbz, 'w', compression=zipfile.ZIP_DEFLATED) as zf_out:
        for item in zf_in.infolist():
            if item.filename.lower() != 'comicinfo.xml':
                zf_out.writestr(item, zf_in.read(item.filename))
        zf_out.writestr('ComicInfo.xml', new_comic_info.encode('utf-8'))
    os.replace(temp_cbz, cbz_path)