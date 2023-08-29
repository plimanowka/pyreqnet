echo "\n# Generated from /API/RunFunction?name=$1 result" >> api.py
curl "http://reqnet.iot/API/RunFunction?name=$1" | wiz gs - | sed -n '/@dataclass/,$p' >> api.py
