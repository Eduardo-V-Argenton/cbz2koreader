from update_comic_info import update_writer, update_tags, \
    update_series, update_title, update_number, create_comic_info, save_updated_comic_info
from send_file_ssh import connect, send_comic, close_connection
from create_koreader_metadata import create_sdr
from get_comic_info import get_comic_info, get_title, get_series, get_authors, get_tags, get_number
from pathlib import Path
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Send CBZ to KOReader, creating the metadata files"
        )

        parser.add_argument("files", nargs="+", type=Path, help="Path to a CBZ file or a folder containing CBZ files (non-recursive)")
        parser.add_argument("--host", required=True, help="Device IP address or hostname")
        parser.add_argument("--port", type=int, default=2222, help="SSH port (default: 2222)")
        parser.add_argument("--user", default="root", help="SSH user (default: root)")
        parser.add_argument("--dest", default="/mnt/us/documents", help="Remote destination folder (default: /mnt/us/documents)")
        parser.add_argument("--key", help="Path to a private SSH key")
        parser.add_argument("--password", help="SSH password")
        parser.add_argument("--passphrase", help="SSH passphrase")
        parser.add_argument("--series", help="Set the series for all the selected CBZ files")
        parser.add_argument("--authors", help="Set the authors for all the selected CBZ files (comma-separated)")
        parser.add_argument("--tags", help="Set the tags for all the selected CBZ files (comma-separated)")
        parser.add_argument("--titles", help="Set one title per selected CBZ file. The number of titles must match the number of files (comma-separated)")
        parser.add_argument("--series_indexes", help="Set the series_index value. Use with --not_use_comic_info_number or --update_local_series_index to it works. The number of series_indexes must match the number of files(must be an int or a float)")
        parser.add_argument("--not_use_comic_info_number", action="store_true", help="Do not use ComicInfo Number as series_index")
        parser.add_argument("--update_local_series_index", action="store_true", help="Do not use ComicInfo Number as series_index")
        parser.add_argument("--not_local_update",action="store_true", help="Skip local CBZ updates while still creating KOReader metadata")
        

        args = parser.parse_args()

        cbz_files = []

        for input_path in args.files:
            input_path = input_path.expanduser()

            if input_path.is_dir():
                folder_files = sorted(
                    path for path in input_path.iterdir()
                    if path.is_file() and path.suffix.lower() == ".cbz"
                )
                if not folder_files:
                    parser.error(f"No CBZ files found in folder: {input_path}")

                cbz_files.extend(folder_files)

            elif input_path.is_file():
                if input_path.suffix.lower() != ".cbz":
                    parser.error(f"File must have a .cbz extension: {input_path}")

                cbz_files.append(input_path)

            else:
                parser.error(f"File or folder not found: {input_path}")

        remote_folder = args.dest.rstrip("/") + "/"

        ssh = connect(
            args.host,
            args.port,
            args.user,
            key_filename=args.key,
        )
        update_local_files = not args.not_local_update
        
        titles = None
        if args.titles is not None:
            titles = [title.strip() for title in args.titles.split(",")]
            if len(titles) != len(cbz_files):
                raise(Exception("The number of titles must match the number of files"))

        series_indexes = None
        if args.series_indexes is not None:
            series_indexes = [index.strip() for index in args.series_indexes.split(",")]
            if len(series_indexes) != len(cbz_files):
                raise(Exception("The number of series_indexes must match the number of files"))
        try:
            for i,file_path in enumerate(cbz_files):
                local_file = str(file_path)
                file_name = file_path.name
                print(f"Processing: {file_name}")


                comic_info = get_comic_info(local_file)

                series = args.series
                authors = args.authors
                tags = args.tags
                title = titles[i] if titles is not None else None
                if series_indexes is not None:
                    series_index = series_indexes[i]
                else:
                    series_index = i + 1
                
                if update_local_files:
                    updated_value = False
                    if comic_info is None:
                        comic_info = create_comic_info(local_file)
                        updated_value = True
                    if series is not None:
                        comic_info = update_series(comic_info, series)
                        updated_value = True
                    if authors is not None:
                        comic_info = update_writer(comic_info, authors)
                        updated_value = True
                    if tags is not None:
                        comic_info = update_tags(comic_info, tags)
                        updated_value = True
                    if title is not None:
                        comic_info = update_title(comic_info, title)
                        updated_value = True
                    if args.update_local_series_index:
                        comic_info = update_number(comic_info, series_index)
                        updated_value = True
                    if updated_value:
                        print("Updating ComicInfo")
                        save_updated_comic_info(str(file_path), comic_info)

                if comic_info is not None:
                    if series is None:
                        series = get_series(comic_info)
                    if authors is None:
                        authors = get_authors(comic_info)
                    if tags is None:
                        tags = get_tags(comic_info)
                    if title is None:
                        title = get_title(comic_info)
                    if not args.not_use_comic_info_number:
                        number = get_number(comic_info)
                        if number != "":
                            series_index = number
                
                if authors is not None:
                    authors = "\n".join(author.strip() for author in authors.split(","))
                if tags is not None:
                    tags = "\n".join(tag.strip() for tag in tags.split(","))
                if title is None:
                    title = file_name[:-4]

                # send_comic(ssh, local_file, remote_folder + file_name)
                create_sdr(
                    ssh, remote_folder, file_name,
                    authors, series, series_index, title, tags,
                )
                print("==================================================")
        finally:
            close_connection(ssh)
    except Exception as e:
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    main()
