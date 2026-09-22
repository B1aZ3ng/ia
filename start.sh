export ROOT_DIR="$(realpath .)" # gets the path of the directory this is running in
export IP_ADDRESS="$(curl -s https://api.ipify.org)" # gets the ip
source .venv/bin/activate
python updatejson.py
python main.py
