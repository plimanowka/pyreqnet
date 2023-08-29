# LK3
mosquitto_sub -h mqtt.iot -u hass -P hass_w@chata -t 'iot/lk3/#' -v

# Reqnet (API: https://portal.inprax.pl/REQNET/OpisyAPI_REQNET?ID_TYPU=9 )
mosquitto_sub -h mqtt.iot -u hass -P hass_w@chata -t 'D8:BF:C0:FA:75:C3/#'
mosquitto_rr -h mqtt.iot -u hass -P hass_w@chata -t 'D8:BF:C0:FA:75:C3/GetTemperatures' -e 'D8:BF:C0:FA:75:C3/GetTemperaturesResult' -m ''
curl 'http://reqnet.iot/API/RunFunction?name=API' | wiz gs - >> api.py
