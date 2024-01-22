import subprocess


def ping_raspberry_pi(ip_address):
    try:
        response = subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if response.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
        return False


ip_raspberry_pi = "172.20.10.4"

if ping_raspberry_pi(ip_raspberry_pi):
    print("Pi Max connected")
else:
    print("Pi Max not connected")
