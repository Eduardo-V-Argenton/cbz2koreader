import posixpath
import paramiko


def lua_string(value: str | int | float | None) -> str:
    """Encode a value as a quoted Lua string, including control characters."""
    text = "" if value is None else str(value)
    escaped = []
    for character in text:
        if character in ('"', "\\"):
            escaped.append("\\" + character)
        elif ord(character) < 32 or ord(character) == 127:
            escaped.append(f"\\{ord(character):03d}")
        else:
            escaped.append(character)
    return '"' + "".join(escaped) + '"'


def create_metadata_cbz_lua(sftp: paramiko.SFTPClient, remote_folder: str, comic_path: str) -> None:
    location = posixpath.join(remote_folder, "metadata.cbz.lua")
    try:
        sftp.stat(location)
    except FileNotFoundError:
        pass
    else:
        # Preserve existing KOReader settings and reading progress.
        return

    metadata = f'return {{ ["doc_path"] = {lua_string(comic_path)} }}\n'
    with sftp.open(location, "wx") as file:
        file.write(metadata.encode("utf-8"))


def create_custom_metadata_lua(
    sftp: paramiko.SFTPClient,
    remote_folder: str,
    authors: str | None,
    series: str | None,
    series_index: str | int | float | None,
    title: str | None,
    keywords: str | None,
) -> None:
    metadata = f"""return {{
    ["custom_props"] = {{
        ["authors"] = {lua_string(authors)},
        ["series"] = {lua_string(series)},
        ["series_index"] = {lua_string(series_index)},
        ["title"] = {lua_string(title)},
        ["keywords"] = {lua_string(keywords)},
    }},
    ["doc_props"] = {{
        ["authors"] = "",
        ["series"] = "",
        ["title"] = "",
    }},
}}
"""
    location = posixpath.join(remote_folder, "custom_metadata.lua")
    with sftp.open(location, "w") as file:
        file.write(metadata.encode("utf-8"))


def create_sdr(
    ssh: paramiko.SSHClient,
    remote_folder: str,
    file_name: str,
    authors: str | None,
    series: str | None,
    series_index: str | int | float | None,
    title: str | None,
    keywords: str | None,
) -> None:
    with ssh.open_sftp() as sftp:
        sdr_folder = posixpath.join(remote_folder, posixpath.splitext(file_name)[0] + ".sdr")
        try:
            sftp.stat(sdr_folder)
        except FileNotFoundError:
            sftp.mkdir(sdr_folder)

        create_custom_metadata_lua(sftp, sdr_folder, authors, series, series_index, title, keywords)
        create_metadata_cbz_lua(sftp, sdr_folder, posixpath.join(remote_folder, file_name))
        print("Metadata created successfully")
