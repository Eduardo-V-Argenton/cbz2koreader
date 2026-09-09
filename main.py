import os
from update_meta import read_comic_info, update_writer, update_tags, \
    update_series, create_metadata, save_updated_comic_info, update_title_auto
from send_file_ssh import connect, send_comic, close_connection

    
local_file = '/home/eduardo/Desktop/teste.cbz'
remote_folder = '/mnt/us/documents/ToRead/teste.cbz'

metadata = read_comic_info(local_file)
if metadata is None:
    metadata = create_metadata(local_file)

print(metadata)
print('=======================')
print(update_title_auto(metadata, 1))
save_updated_comic_info(local_file, metadata)

