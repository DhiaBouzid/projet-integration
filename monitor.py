import paramiko
import getpass

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
            return f"[ERREUR] {error.strip()}"
        return output.strip()
    except Exception as e:
        return f"[EXCEPTION] {e}"

def show_system_info(ssh):
    print("\n=== 📊 Mémoire (RAM) ===")
    print(run_command(ssh, 'powershell -Command "systeminfo | findstr /C:\"Total Physical Memory\""'))

    print("\n=== 🧠 CPU ===")
    print(run_command(ssh, 'powershell -Command "wmic cpu get loadpercentage"'))

    print("\n=== 💾 Disques ===")
    print(run_command(ssh, 'powershell -Command "Get-PSDrive -PSProvider FileSystem | Out-String"'))

def manage_services(ssh):
    while True:
        print("\n--- Gestion des services ---")
        print("1) Lister tous les services")
        print("2) Démarrer un service")
        print("3) Arrêter un service")
        print("4) Retour au menu principal")
        choice = input("Entrez le numéro de l'action service : ")

        if choice == '1':
            print(run_command(ssh, 'powershell -Command "Get-Service | Out-String"'))
        elif choice == '2':
            svc = input("Nom du service à démarrer : ")
            print(run_command(ssh, f'powershell -Command "Start-Service -Name {svc}"'))
        elif choice == '3':
            svc = input("Nom du service à arrêter : ")
            print(run_command(ssh, f'powershell -Command "Stop-Service -Name {svc}"'))
        elif choice == '4':
            break
        else:
            print("❓ Option invalide, veuillez réessayer.")

def main():
    HOST = input("🖥️ Adresse IP ou nom d'hôte : ")
    USER = input("👤 Nom d'utilisateur : ")
    PASSWORD = getpass.getpass("🔐 Mot de passe : ")

    ssh = connect_ssh(HOST, USER, PASSWORD)
    if not ssh:
        return

    while True:
        print("\nQue souhaitez-vous faire ?")
        print("1) Afficher les infos système (RAM, CPU, Disques)")
        print("2) Redémarrer la machine distante")
        print("3) Éteindre la machine distante")
        print("4) Gestion des services")
        print("5) Quitter")
        choix = input("Entrez le numéro de l'option : ")

        if choix == '1':
            show_system_info(ssh)
        elif choix == '2':
            confirm = input("⚠️ Êtes-vous sûr de vouloir redémarrer ? (o/N) : ")
            if confirm.lower() == 'o':
                print(run_command(ssh, 'shutdown /r /t 0'))
                break
        elif choix == '3':
            confirm = input("⚠️ Êtes-vous sûr de vouloir éteindre ? (o/N) : ")
            if confirm.lower() == 'o':
                print(run_command(ssh, 'shutdown /s /t 0'))
                break
        elif choix == '4':
            manage_services(ssh)
        elif choix == '5':
            print("🔌 Déconnexion et sortie...")
            break
        else:
            print("❓ Option invalide, veuillez réessayer.")

    ssh.close()

if __name__ == "__main__":
    main()
