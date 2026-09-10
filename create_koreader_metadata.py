import paramiko
def create_sdr_folder():
    pass

def create_metadata_cbz_lua(sftp: paramiko.SFTPClient, remote_folder : str, comic_path : str) -> None:
    metadata = f"""
        return {{
            ["doc_path"] = "{comic_path}",
        }}
    """
    location = remote_folder + "/metadata.cbz.lua"
    with sftp.open(location, "wx") as file:
        file.write(metadata.encode("utf-8"))
    

def create_custom_metadata_lua(sftp : paramiko.SFTPClient, remote_folder : str, authors : str, series : str, series_index : str, title : str, keywords : str) -> None:
    metadata = f"""
        return {{
            ["custom_props"] = {{
                ["authors"] = "{authors}",
                ["series"] = "{series}",
                ["series_index"] = "{series_index}",
                ["title"] = "{title}",
                ["keywords"] = [[{keywords}]],
            }},
            ["doc_props"] = {{
                ["authors"] = "",
                ["series"] = "",
                ["title"] = "",
            }},
        }}
    """
    location = remote_folder + "/custom_metadata.lua"
    with sftp.open(location, "wx") as file:
        file.write(metadata.encode("utf-8"))
    

def create_sdr(ssh : paramiko.SSHClient, remote_folder : str, file_name : str, authors : str, series : str, series_index : str, title : str, keywords : str) -> None:
    with ssh.open_sftp() as sftp:
        sdr_folder = remote_folder + file_name[:-3] + "sdr"
        try:
            sftp.stat(sdr_folder)
        except FileNotFoundError:
            sftp.mkdir(sdr_folder)
        
        create_custom_metadata_lua(sftp, sdr_folder, authors, series, series_index, title, keywords)
        create_metadata_cbz_lua(sftp, sdr_folder, (remote_folder + file_name))