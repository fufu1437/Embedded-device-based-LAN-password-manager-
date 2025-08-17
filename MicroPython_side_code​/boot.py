import network
import time
from machine import Pin




def wifi(name="CMCC-sia7", password="Lb9E5PFC", timeout=10):
    """
    连接Wi-Fi网络1
    参数:
        ssid (str): Wi-Fi名称
        password (str): 密码
        timeout (int): 超时时间(秒)
    返回:
        bool: 是否连接成功
    """
    led = Pin(2,Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"正在连接 {name}...")
        wlan.connect(name, password)
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print("连接成功!")
        print("IP地址:", wlan.ifconfig()[0])
        led.value(1)
        time.sleep_ms(500)
        led.value(0)
        return True
    else:
        print("连接失败")
        return False

wifi()