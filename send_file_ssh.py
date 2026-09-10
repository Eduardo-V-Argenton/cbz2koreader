import paramiko
import os

def connect(hostname: str, port: int, username: str, password: str | None = None, key_filename: str | None = None,*,passphrase: str | None = None,) -> paramiko.SSHClient:
    if key_filename is not None:
        key_filename = os.path.expanduser(key_filename)
        if not os.path.isfile(key_filename):
            raise FileNotFoundError(f"SSH key not found: {key_filename}")

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            key_filename=key_filename,
            password=password,
            passphrase=passphrase,
            allow_agent=True,
            look_for_keys=True,
        )
    except Exception:
        ssh.close()
        raise

    return ssh


def progress(transfered, total):
    perct = (transfered / total) * 100
    print(f"Sending: {perct:.1f}% ({transfered}/{total} bytes)", end='\r')


def send_comic(ssh : paramiko.SSHClient, local_file, remote_file):
    with ssh.open_sftp() as sftp:
        atributos = sftp.put(local_file, remote_file, callback=progress)
        print(" Upload concluído com sucesso!")
        print(f"Tamanho remoto confirmado: {atributos.st_size} bytes")


def close_connection(ssh : paramiko.SSHClient):
    ssh.close()
