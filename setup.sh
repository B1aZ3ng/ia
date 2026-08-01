python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo add-apt-repository multiverse; sudo dpkg --add-architecture i386; sudo apt update #installs steamcmd requirements
sudo apt install steamcmd #installs steamcmd for cs and unturned