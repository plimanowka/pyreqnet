from __future__ import annotations
from enum import Enum, IntFlag, IntEnum
from typing import Any, Union, List, AnyStr, Type, TypeVar, Callable
from typing_extensions import Annotated
from dataclasses import dataclass, field, fields
from dataclass_wizard import JSONSerializable, json_key, json_field, LoadMixin, DumpMixin
from dataclass_wizard.type_def import N

# Example usage:
"""
from urllib import request as rq
import api

func = 'API'
resp = rq.urlopen(f'http://reqnet.iot/API/RunFunction?name={func}').read()
res = api.APIResult.from_json(resp)
"""
# To reload:
"""
from importlib import reload
api = reload(api)
"""

# Request type
RQ = TypeVar('RQ', JSONSerializable, JSONSerializable)
# Response type
RSP = TypeVar('RSP', JSONSerializable, JSONSerializable)

import urllib.parse, urllib.request

@dataclass
class Reqnet:
    host: str
    mqtt_server: str
    mqtt_port: int = 1883
    name: str = 'primary'
    mac_address: str = None
    ip: str = None
    mqtt_connected: bool = None
    wifi_connected: bool = None
    wifi_ssid: str = None
    wifi_signal_strength: str = None
    software_version: str = None
    api_version: int = None

    def __post_init__(self):
        res: APIResult = self.http(API(), APIResult)
        assert self.mac_address is None or self.mac_address == res.mac, f'MAC address mismatch; given: {self.mac_address}, actual: {res.mac}'
        self.mqtt_connected = res.mqtt_status
        self.wifi_connected = res.wifi_status
        self.wifi_ssid = res.wifi_ssid
        self.wifi_signal_strength = res.wifi_signal_strength_description
        self.ip = res.wifi_ip
        self.software_version = res.recuperator_software_version
        self.api_version = res.api_version
        
    def http(self, req: RQ, resp_type: Type[RSP]) -> RSP:
        params = [(prop.name, req.__getattribute__(prop.name)) for prop in fields(req)]
        params.insert(0, ('name', req.__class__.__name__))
        params = '&'.join([f'{name}={urllib.parse.quote(str(val))}' for (name, val) in params if val is not None])
        url = f'http://{self.host}/API/RunFunction?{params}'
        resp = urllib.request.urlopen(url).read()
        return resp_type.from_json(resp)
    
    def mqtt(self, req: RQ, resp_type: Type[RSP]) -> RSP:
        pass
    
    def mqtt_subscribe(self, callback: Callable[[RSP], None], resp_type: Type[RSP]) -> None:
        pass
    
_to_quey_params = lambda obj: '&'.join([f'{name}={urllib.parse.quote(str(val))}'
                                      for (name, val) in 
                                        [(prop.name, obj.__getattribute__(prop.name)) for prop in fields(obj)]
                                    if val is not None])


@dataclass
class API(JSONSerializable):
    pass


# Generated from /API/RunFunction?name=API result
@dataclass
class APIResult(JSONSerializable):
    """
    API function result
    """
    api_result: bool
    mac: str
    status: Union[bool, str]
    mqtt_status: bool
    wifi_status: Union[bool, str]
    wifi_ssid: Annotated[str, json_key('WIFISSID', all=True)]
    ap_ssid: Annotated[str, json_key('APSSID', all=True)]
    recuperator_software_version: Union[float, str]
    api_version: int
    device_type: int
    wifi_signal_strength: int
    wifi_ip: Annotated[str, json_key('WIFIIP', all=True)]
    wifi_signal_strength_description: str
    log_mode: int
    error_code: int


# Generated from /API/RunFunction?name=CurrentWorkParameters result
@dataclass
class CurrentWorkParametersResult(JSONSerializable):
    """
    CurrentWorkParameters function result
    """
    current_work_parameters_result: bool
    values_raw: List[Union[int, float]] = json_field('Values', all=True)
    
    @property
    def values(self):
        if not hasattr(self, '_values'):
            object.__setattr__(self, '_values', WorkParametersValues(*self.values_raw[:84]))
        return self._values
    

class State(Enum):
    OFF = 0
    ON = 1
    
class OperationMode(Enum):
    HEATING_FAST = 1
    COOLING_FAST = 2
    VACATION = 3
    AIRING = 4
    CLEANING = 5
    FIREPLACE = 6
    MANUAL = 8
    AI = 9
    PERF_MEASURE = 10
    
class ParallelMode(Enum):
    OFF = 0
    HEATING = 1
    COOLING = 2
    
class BypassState(Enum):
    MAN_CLOSED = 0
    MAN_OPEN = 1
    AUTO_CLOSED = 2
    AUTO_OPEN = 3
    
@dataclass
class WorkParametersValues:
    status: int | State
    intake_max: int
    temperature: float
    intake: int
    exhaust: int
    intake_manual: int
    exhaust_manual: int
    humidity: int
    co2_ppm: int
    harmonogram: int | State
    operation_mode: int | OperationMode
    override_ttl_min: int
    override_ttl_sec: int
    parallel_mode: int | ParallelMode
    vacation_ttl_days: int
    dev_model: int
    yield_coeff_fast_heating: int
    yield_coeff_fast_cooling: int
    yield_coeff_vacation: int
    yield_coeff_airing: int
    yield_coeff_cleaning: int
    yield_coeff_fireplace: int
    yield_coeff_alarm: int
    yield_coeff_other_1: int
    yield_coeff_other_2: int
    yield_coeff_other_3: int
    dev_state_1: State
    dev_state_2: State
    dev_state_3: State
    dev_state_4: State
    dev_state_5: State
    dev_state_6: State
    dev_state_7: State
    dev_state_8: State
    dev_state_9: State
    dev_state_10: State
    dev_state_11: State
    dev_state_12: State
    dev_state_13: State
    bypass_state: int | BypassState
    error_code: int
    message_code: int
    dev_value_1: int
    dev_value_2: int
    dev_value_3: int
    dev_value_4: int
    dev_value_5: int
    dev_value_6: int
    dev_value_7: int
    dev_value_8: int
    dev_value_9: int
    dev_value_10: int
    dev_value_11: int
    dev_value_12: int
    dev_value_13: int
    temp_intake: float
    temp_chute: float
    temp_supply: float
    temp_extract: float
    temp_heater_conduit: float
    temp_GHE: float
    temp_room: float
    temp_aux: float
    resistance_supply: int
    resistance_extract: int
    fan_supply: int
    fan_extract: int
    temp_comfort: float
    res1: float
    sensitivity_co2: float
    sensitivity_higro: float
    state_humidity_detection: int
    state_preheat: int | State
    state_anti_freeze: int | State
    state_anti_condensate: int | State
    pressure_supply: float
    pressure_extract: float
    res2: float
    res3: float
    res4: float
    res5: float
    pow_supply: int
    pow_extract: int
    filters_ttl_days: int

    def __post_init__(self: WorkParametersValues):
        self.status = State(self.status)
        self.harmonogram = State(self.harmonogram)
        self.operation_mode = OperationMode(self.operation_mode)
        self.parallel_mode = ParallelMode(self.parallel_mode)
        self.bypass_state = BypassState(self.bypass_state)
        self.state_preheat = State(self.state_preheat)
        self.state_anti_freeze = State(self.state_anti_freeze)
        self.state_anti_condensate = State(self.state_anti_condensate)

# Generated from /API/RunFunction?name=GetTemperatures result
@dataclass
class GetTemperaturesResult(JSONSerializable):
    """
    GetTemperatures function result
    """
    get_temperatures_result: bool
    intake: Union[float, str]
    launcher: Union[float, str]
    supply: Union[float, str]
    extract: Union[float, str]
    heater_cooler: Union[float, str]
    heater_cooler_active: State
    gwc: Union[float, str]
    gwc_active: State
    room: Union[float, str]
    room_temp_active: State
    additional: Union[float, str]
    additional_temp_active: State
