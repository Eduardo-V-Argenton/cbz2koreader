import paramiko
import os


def connect(hostname : str, port : int, username : str, password : str | None, key_filename : str | None):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if password is None and key_filename != None:
        ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            key_filename=os.path.expanduser('~/.ssh/id_ed25519'),
        )

    elif password != None and key_filename is None:
        ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
        )
    
    return ssh


def progress(transfered, total):
    perct = (transfered / total) * 100
    print(f"Enviando: {perct:.1f}% ({transfered}/{total} bytes)", end='\r')


def send_comic(ssh : paramiko.SSHClient, local_file, remote_folder):
    sftp = ssh.open_sftp()

    try:
        atributos = sftp.put(local_file, remote_folder, callback=progress)
        print(" Upload concluído com sucesso!")
        print(f"Tamanho remoto confirmado: {atributos.st_size} bytes")
    except Exception as e:
        raise(e)

def create_sdr_folder():
    pass

def create_metadata_cbz_lua():
#     return {
#     ["doc_path"] = "/mnt/us/documents/ToRead/Devil is a Part-Timer! v05, The - Satoshi Wagahara, Akio Hiiragi_kcc0.cbz",
# }
    pass

def create_custom_metadata_lua():
# return {
#     ["custom_props"] = {
#         ["authors"] = "Akio Hiiragi Satoshi Wagahara",
#         ["series"] = "The Devil Is a Part-Timer!",
#         ["series_index"] = "1.0",
#         ["title"] = "The Devil is a Part-Timer! v05",
#     },
#     ["doc_props"] = {
#         ["authors"] = "",
#         ["series"] = "",
#         ["series_index"] = "",
#         ["title"] = "",
#     },
# }
    pass

def create_sdr():
    pass

def close_connection(ssh : paramiko.SSHClient):
    ssh.close()

