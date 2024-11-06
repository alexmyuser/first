import os
import subprocess
import shutil

# User input and configurations
username = "user"  # Specify the username
password = "root"  # Specify the password

# Create user and add to sudo group
os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\\/bin\\/sh/\\/bin\\/bash/g' /etc/passwd")

class SSHSetup:
    def __init__(self, user):
        self.installSSHServer()
        self.installDesktopEnvironment()
        self.changewall()
        self.installGoogleChrome()
        self.installTelegram()
        self.installQbit()
        self.finish(user)

    @staticmethod
    def installSSHServer():
        subprocess.run(['apt', 'update'])
        subprocess.run(['apt', 'install', '-y', 'openssh-server'])
        os.system("systemctl enable ssh --now")
        print("SSH Server Installed and Started")

    @staticmethod
    def installDesktopEnvironment():
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("sudo apt purge light-locker")
        os.system("sudo apt install --reinstall xfce4-screensaver")
        os.system("systemctl disable lightdm.service")
        print("Installed XFCE4 Desktop Environment")

    @staticmethod
    def installGoogleChrome():
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])
        print("Google Chrome Installed")

    @staticmethod
    def installTelegram():
        subprocess.run(["apt", "install", "--assume-yes", "telegram-desktop"])
        print("Telegram Installed")

    @staticmethod
    def changewall():
        os.system(f"curl -s -L -k -o xfce-verticals.png https://gitlab.com/chamod12/changewallpaper-win10/-/raw/main/CachedImage_1024_768_POS4.jpg")
        current_directory = os.getcwd()
        custom_wallpaper_path = os.path.join(current_directory, "xfce-verticals.png")
        destination_path = '/usr/share/backgrounds/xfce/'
        shutil.copy(custom_wallpaper_path, destination_path)
        print("Wallpaper Changed")

    @staticmethod
    def installQbit():
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "-y", "qbittorrent"])
        print("Qbittorrent Installed")

    @staticmethod
    def finish(user):
        os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
        link = "www.youtube.com/@The_Disala"
        colab_autostart = """[Desktop Entry]
Type=Application
Name=Colab
Exec=sh -c "sensible-browser {}"
Icon=
Comment=Open a predefined notebook at session signin.
X-GNOME-Autostart-enabled=true""".format(link)
        with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
            f.write(colab_autostart)
        os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop")
        os.system(f"chown {user}:{user} /home/{user}/.config")
        
        print("Setup Complete!")
        print("You can now SSH into the server with:")
        print(f"Username: {username}")
        print(f"Password: {password}")
        
try:
    SSHSetup(username)
except NameError as e:
    print("'username' variable not found, create a user first")
