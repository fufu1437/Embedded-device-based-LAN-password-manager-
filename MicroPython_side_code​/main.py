from microdot import Microdot
from machine import Pin,SPI
import ujson as json
import os
import sdcard

def sd():#连接sd卡来的
    spi = SPI(1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    cs = Pin(5, Pin.OUT)
    sd1 = sdcard.SDCard(spi, cs)
    os.mount(sd1, '/sd')

sd()
app = Microdot()
list1=[]
path = "/sd/data"

@app.route("/test" ,methods=['GET'])
def test(request):
    return 404

@app.route("/get" ,methods=['GET'])
def get(request):#读密码来的
    def yule():
        file_path = os.listdir("/sd/data")
        file_len = len(file_path)
        if file_len > 0:
            for i in file_path:
                return_str = i[:-5]
                with open(f"{path}/{i}", "r") as f:
                    file_out = json.load(f)
                try:
                    file_out[0]
                    file_out.append(return_str)
                    yield json.dumps(file_out) + "\n"
                except IndexError:
                    os.remove(f"{path}/{i}")

        else:
            yield "null"
    return yule(), {'Content-Type': 'application/x-ndjson'}


@app.route("/GetFile",methods=["GET"])
def get_file(request):
    file_path = os.listdir("/sd/data")
    return  json.dumps(file_path)
@app.route("/PartGet/<file>",methods=["GET"])
def part_get(request,file):
    with open(f"{path}/{file}","r")as f:
        json_data = json.load(f)
    return  json.dumps(json_data)


@app.route("/post" , methods=['POST'])
def write(request):#添加密码来的
    dict1 = request.json#接受客户端的json数据
    path1 = f"{path}/{dict1[0]}.json"#每个应用或网站单独一个文件（sd卡的优势来的）
    try:#这行开始
        os.stat(path1)
    except OSError:
        open(path1, 'w').close()#到这行为检查文件是否存在
    try:#这行开始
        with open(path1, 'r') as f:
            json_data = json.load(f)
    except ValueError:
        json_data=[]#到这行为检查文件里是否有内容
    json_data.append(dict1[1])
    with open(path1, 'w') as f:
        json.dump(json_data,f)#到这里是添加新内容，而不覆盖原有内容

@app.route("/patch",methods=['PATCH'])
def patch(request):
    data = request.json
    file = data["file"]
    nums = int(data["nums"])
    name = data["name"]
    pwds = data["pwds"]
    note = data["note"]
    with open(f"{path}/{file}.json","r")as f:
        data_json_read = json.load(f)
    data_json = data_json_read[nums]
    if name!="":
        data_json["name"] = name
    if pwds!="":
        data_json["pwds"] = pwds
    if note!="":
        data_json["note"] = note

    data_json_read[nums]=data_json
    with open(f"{path}/{file}.json","w") as f:
        json.dump(data_json_read,f)



@app.route("/del", methods=["DELETE"])
def delete(request):
    data = request.json
    file = data["file"]
    pwd_num = data["pwd_num"]
    with open(f"{path}/{file}.json","r") as f:
        json_data = json.load(f)
    del json_data[int(pwd_num)]
    with open(f"{path}/{file}.json","w") as f:
        json.dump(json_data,f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

