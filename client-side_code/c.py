import base64
import requests
import json
import socket
import ctypes

# 定义RGB值
r = 30
g = 31
b = 34
# MicroPython设备的IP地址和端口
device_ip = "192.168.1.46"  # 替换为你的设备IP
port = 80  # 替换为HTTP服务器端口
url = f"http://{device_ip}:{port}"

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[38;2;69;139;198m"
RESET = "\033[0m"
LightGrayFg = "\033[38;2;188;190;196m"
DimmedRed = "\033[38;2;230;0;0m"
AquaFg = "\033[38;2;125;182;191m"

def check_port(ip, port=80, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        return True  # 端口开放表示设备可达
    except OSError:
        return False  # 连接失败
    finally:
        s.close()

# 设置整个终端背景色 (仅限Windows)
def set_terminal_bg_color(r, g, b):
    # -11表示标准输出设备句柄
    STD_OUTPUT_HANDLE = -11

    # 创建COORD结构定义整个屏幕大小
    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    # 创建SMALL_RECT结构定义整个控制台区域
    class SMALL_RECT(ctypes.Structure):
        _fields_ = [("Left", ctypes.c_short),
                    ("Top", ctypes.c_short),
                    ("Right", ctypes.c_short),
                    ("Bottom", ctypes.c_short)]

    # 创建CONSOLE_SCREEN_BUFFER_INFOEX结构
    class CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("dwSize", COORD),
                    ("dwCursorPosition", COORD),
                    ("wAttributes", ctypes.c_ushort),
                    ("srWindow", SMALL_RECT),
                    ("dwMaximumWindowSize", COORD),
                    ("wPopupAttributes", ctypes.c_ushort),
                    ("bFullscreenSupported", ctypes.c_bool),
                    ("ColorTable", ctypes.c_ulong * 16)]

        def __init__(self):
            self.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)
            super().__init__()

    # 获取控制台信息
    hdl = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    csbi = CONSOLE_SCREEN_BUFFER_INFOEX()
    ctypes.windll.kernel32.GetConsoleScreenBufferInfoEx(hdl, ctypes.byref(csbi))

    # 修改颜色表中背景色的索引
    # 在Windows中，背景色对应索引5（黑色位置）
    csbi.ColorTable[0] = (r) | (g << 8) | (b << 16)

    # 应用修改
    ctypes.windll.kernel32.SetConsoleScreenBufferInfoEx(hdl, ctypes.byref(csbi))



set_terminal_bg_color(30, 31, 34)

def chinese_to_base64(text):
    encoded = base64.b64encode(text.encode('utf-8'))
    return encoded.decode('ascii').rstrip("=")

def base64_to_chinese(encoded_text):
    padding_needed = len(encoded_text) % 4
    if padding_needed:
        encoded_text += '=' * (4 - padding_needed)
    try:
        decoded_bytes = base64.b64decode(encoded_text)
    except Exception as e:
        raise ValueError(f"无效的Base64编码: {e}")
    return decoded_bytes.decode('utf-8')

def Get(*,color=False):
    list1 = []
    list2 = []
    list3 = []
    num1=0

    try:
        json1 = requests.get(f'{url}/get', stream=True)
        for line in json1.iter_lines():
            num = 0
            data = json.loads(line.decode('utf-8'))
            file_data = data[-1]
            chines = base64_to_chinese(file_data)
            if color:
                num1+=1
                print(f"{BLUE}({num1}){RESET}",end="")
            print(f"{BLUE}网站/应用：{RED}{chines}{RESET}")

            for z in data:
                if isinstance(z, dict):
                    if color:
                        num += 1
                        print(f"{RED}({num}){RESET}", end="")
                    print(f"用户名/账户：{base64_to_chinese(z["name"])}", end='  ')
                    print(f"密码：{base64_to_chinese(z["pwds"])}", end='  ')
                    print(f"备注：{base64_to_chinese(z["note"])}")
            list1.append(num)
            list2.append(file_data)
        list3.append(list1)
        list3.append(list2)
        if color:
            return list3
    except TypeError:
        print("无密码，请添加密码")

def GetModify_indices(para,web):
    while True:
        try:
            web_num = input(f"请输入{para}的网页的序号")
            if int(web_num)-1 <= int(len(web[1])):
                break
            else:
                print("请输入正确的序号")
        except ValueError:
            print("请输入正确的序号")

    while True:
        try:
            num = int(input(f"请输入{para}的密码组的序号"))
            axz = int(web[0][int(web_num)-1])
            if num<=axz:
                break
            else:
                raise IndexError
        except (IndexError, ValueError):
            print("请输入正确的序号")
    return [web_num,num]

class AbortProcessing(Exception):
    pass

class ConnectionFailed(Exception):
    pass

class ExitProgram(Exception):
    pass

while True:
    list1 = []
    dict1 = {}
    dict2 = {}
    site = []
    web_num = 0
    num = 0
    print(f"{AquaFg}(1)查看全部密码\n"
          "(2)查看部分密码\n"
          "(3)添加密码\n"
          "(4)修改密码\n"
          f"(5)删除密码{RESET}")

    try:
        if not check_port(device_ip):
            raise ConnectionFailed
        input1 = input()
        if input1 == '1':#读取密码
           Get()

        elif input1 == "2":
            data2 = requests.get(f'{url}/GetFile').json()
            print(f"{BLUE}网站/应用：{RESET}")
            for f in data2:
                num += 1
                print(f"{RED}({num}) {RESET}{base64_to_chinese(f[:-5])}")
            while True:
                input3 = input("请输入你想查询的网站(应用)的序号(T/退出)：").strip()
                if input3 == "":
                    print("请输入正确的序号")
                elif input3.upper() == "T":
                    raise AbortProcessing
                else:
                    break
            data3 = requests.get(f'{url}/PartGet/{data2[int(input3)-1]}')
            for z in data3.json():
                print(f"用户名/账户：{base64_to_chinese(z["name"])}", end='  ')
                print(f"密码：{base64_to_chinese(z["pwds"])}", end='  ')
                print(f"备注：{base64_to_chinese(z["note"])}")

        elif input1 == '3':#写入密码
            while True:
                data4 = requests.get(f'{url}/GetFile').json()
                print(f"{BLUE}网站/应用：{RESET}")
                for f in data4:
                    num += 1
                    print(f"{RED}({num}) {RESET}{base64_to_chinese(f[:-5])}")
                user_site = input("网站/应用(支持输入序号)(T/退出)：").strip()
                user_site_bool = user_site.isdigit()
                if len(user_site) == 0:
                    print("请输入正确的网站/应用")
                elif user_site_bool:
                    user_site_nums = int(user_site)
                    user_site = base64_to_chinese(data4[int(user_site_nums) - 1][:-5])
                    break
                elif user_site.upper() == "T":
                    raise AbortProcessing
                else:
                    break

            while True:
               user_name = input("用户名/账户(T/退出)：").strip()
               if user_name == "":
                   print("请输入正确的用户名/账户")
               elif user_name.upper() == "T":
                   raise AbortProcessing
               else:
                   break
            while True:
                user_password = input("密码(T/退出)：").strip()
                if user_password == "":
                    print("请输入正确的密码")
                elif user_password.upper() == "T":
                    raise AbortProcessing
                else:
                    break
            user_note = input("备注：")
            if user_note.strip() == '':
                user_note = "无"
            dict1["name"] = chinese_to_base64(user_name)
            dict1["pwds"] = chinese_to_base64(user_password)
            dict1["note"] = chinese_to_base64(user_note)
            site.append(chinese_to_base64(user_site))
            site.append(dict1)
            print(site)
            try:
                requests.post(f"{url}/post", json=site)
            except requests.exceptions.ConnectionError:
                print("远程主机强迫关闭了本次连接")

        elif input1 == '4':#修改密码
            web = Get(color=True)
            ac = {}
            get_modify = GetModify_indices("修改",web)
            web_num = get_modify[0]
            num = get_modify[1]

            ac["file"] = f"{web[1][int(web_num) - 1]}"
            ac["nums"] = f"{int(num) - 1}"
            name = input("用户名/账户(不修改则直接回车(Enter))：").strip()
            password = input("密码(不修改则直接回车(Enter))：").strip()
            note = input("备注(不修改则直接回车(Enter))：").strip()
            ac.update({"name": name, "pwds": password, "note": note})
            a = requests.patch(f"{url}/patch", json=ac)

        elif input1 == '5':
            acs = {}
            web = Get(color=True)
            get_modify = GetModify_indices("删除",web)
            web_num = get_modify[0]
            num = get_modify[1]
            file_num = web[1][int(web_num)-1]
            acs.update({"file":file_num,"pwd_num":int(num)-1})
            input2 = input("请确认(y/n): ")
            if input2=="y":
                requests.delete(f"{url}/del", json=acs)
            elif input2=="n":
                print("已成功删除")

        else:
            print("请输入正确的指令")
    except requests.exceptions.ConnectionError:
        print("连接失败")

    except AbortProcessing:
        print("已停止")

    except ConnectionFailed:
        print("远程设备未启动")
