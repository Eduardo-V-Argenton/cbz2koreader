import os
from update_comic_info import update_writer, update_tags, \
    update_series, create_comic_info, save_updated_comic_info
from send_file_ssh import connect, send_comic, close_connection
from create_koreader_metadata import create_sdr
from get_comic_info import get_comic_info, get_title, get_series, get_writer, get_tags, get_number
from pathlib import Path


local_file = '/home/eduardo/Desktop/teste_2.cbz'
remote_folder = '/mnt/us/documents/ToRead/'
file_name = Path(local_file).name

comic_info = get_comic_info(local_file)
if comic_info is None:
    comic_info = create_comic_info(local_file)
print(comic_info)
title = get_title(comic_info)
series = get_series(comic_info)
authors = get_writer(comic_info)
keywords = get_tags(comic_info)
keywords = "\n".join(parte.strip() for parte in keywords.split(","))
series_index = get_number(comic_info)

ssh = connect("192.168.0.103", 2222, "root")
send_comic(ssh, local_file, remote_folder+file_name)
create_sdr(ssh, remote_folder, file_name, authors, series, series_index, title, keywords)
close_connection(ssh)
