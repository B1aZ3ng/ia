export ROOT_DIR="$(realpath .)"
source .venv/bin/activate
python updatejson.py
python main.py
