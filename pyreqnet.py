from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class APIResult:
    API_result: bool
    mac: str
    status: bool
    MQTT_status: bool
    WIFI_status: bool
    WIFI_SSID: str = None
    AP_SSID: str = None
    update_firmware_status: int = None
    mode: int = None
    update_to_version: int = None
    recuperator_software_version: str = None
    API_version: int = None
    available_heap_size: int = None
    total_program_size: int = None
    program_size: int = None
    device_type: int = None
    WIFI_IP: str = None
    WIFI_signal_strength: int = None
    log_mode: int = None
    
