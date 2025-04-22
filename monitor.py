import paramiko

def connect_ssh(host, user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, username=user, password=password)
        print(f"✅ Connexion SSH réussie à {host} avec l'utilisateur {user}")
        return ssh
    except Exception as e:
        print(f"❌ Échec de la connexion SSH : {e}")
        return None

def run_command(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('latin1')
        error = stderr.read().decode('latin1')
        if error:
            return f"[ERREUR] {error}"
        return output.strip()
    except Exception as e:
        return f"[EXCEPTION] {e}"

if __name__ == "__main__":
    HOST = "192.168.66.133"
    USER = "firas"
    PASSWORD = "firas123hayet"

    ssh = connect_ssh(HOST, USER, PASSWORD)
    
    if ssh:
        print("\n=== 📊 Mémoire (RAM) ===")
        print(run_command(ssh, 'powershell -Command "systeminfo | findstr /C:\\"Total Physical Memory\\""'))

        print("\n=== 🧠 CPU ===")
        print(run_command(ssh, 'powershell -Command "wmic cpu get loadpercentage"'))

        print("\n=== 💾 Disques ===")
        print(run_command(ssh, 'powershell -Command "Get-PSDrive -PSProvider FileSystem | Out-String"'))

        ssh.close()
