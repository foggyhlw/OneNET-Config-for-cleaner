import requests
import os
import time
#reg_date
#reg_date=time.strftime('%Y%m%d',time.localtime(time.time()))
#reg_date参数用于创建设备的sn参数，为了便于管理，统一将该参数设定为"cleaner"
sn='cleaner'
print(os.getcwd())
with open('register_code.txt','r') as f:
    register_code=f.readline().strip()
print('正式环境注册码为： '+register_code+'\n请核实是否正确')
#register_code='8DBVraHDlZHUG4Zg'
#register device
def register_device():
    reg_url='http://api.heclouds.com/register_de'
    data={"sn": sn,"title":"PMS5003S"}
    #data={"sn": '20170819',"title":"PMS5003S"}
    para={'register_code':register_code}
    r=requests.post(reg_url,json=data,params=para)
    #print(r.json())
    if r.status_code==requests.codes.ok :
        if r.json()['error']=='succ':
            api_key=r.json()['data']['key']
            device_id=r.json()['data']['device_id']
            return api_key,device_id
        else:
            print(r.json()['error'])
    else:
        print('register device failed!')


#add datastreams
def add_datastream(stream_id,api_key,device_id):
    url='http://api.heclouds.com/devices/{0}/datastreams'.format(device_id)
    header={'api-key':api_key}
    data={'id':stream_id}
    r=requests.post(url,headers=header,json=data)
    #print(r.json())
    if r.status_code==requests.codes.ok:
        if r.json()['error']=='succ':
            ds_uuid=r.json()['data']['ds_uuid']
            print('adding datastream {0} OK!'.format(stream_id))
            return ds_uuid
        else:
            print(r.json()['error'])
            #print('adding datastream {} FAILED!'.format(stream_id))
    else:
        print('adding datastream {} FAILED!'.format(stream_id))

#for Cleaner
datastream_ids=['cmd','off_threshold','low_threshold','medium_threshold','high_threshold','pm01','pm25','pm10']
#for fishtank controller
#datastream_ids=['manual_cmd','温度','过热保护']

def add_datapoints(api_key,device_id):
    url='http://api.heclouds.com/devices/{0}/datapoints'.format(device_id)
    header={'api-key':api_key}
    #for Cleaner
    data={'datastreams':[{'id':'off_threshold','datapoints':[{"value":20}]},
        {'id':'low_threshold','datapoints':[{"value":50}]},
        {'id':'medium_threshold','datapoints':[{"value":80}]},
        {'id':'high_threshold','datapoints':[{"value":160}]},
        {'id':'cmd','datapoints':[{"value":0}]}]}

    #for fishtank controller
    #data={'datastreams':[{'id':'manual_cmd','datapoints':[{"value":0}]},
    #    {'id':'过热保护','datapoints':[{"value":0}]},
    #    {'id':'温度','datapoints':[{"value":0}]}]}
    r=requests.post(url,headers=header,json=data)
    if r.status_code==requests.codes.ok:
#        print(r.json())
        if r.json()['error']=='succ':
        	print('reset control signals OK!')
        else:
        	print('reset control signals FAILED!')
    else:
    	print('add_datapoints FAILED!')

def delete_device(api_key,device_id):
    url='http://api.heclouds.com/devices/{0}'.format(device_id)
    header={'api-key':api_key}
    r=requests.delete(url,headers=header)
    print(r.status_code)
    if r.status_code==requests.codes.ok:
        if r.json()['error']=='succ':
        	print('delete device OK!')
        else:
        	print('delete device FAILED!')
    else:
    	print('delete device FAILED!')

key=input('-----\nChoose a selection:\n    n: create device and add datastreams(新建)\n    r: reset thresholds to default values(重置).\n    d: delete device and recreate device(删除)\n------\nYour choice is: ')
if key in ['n','N']:
    api_key,device_id=register_device()
    with open('./output/api_id.lua','w',newline='') as f:
        #用于配合NodeMCU读入文件格式
        #f.write('api-key:'+api_key)
        #f.write('\n')
        #f.write(device_id)
        #f.write('\n')
        f.writelines('api-key:'+api_key+'\n')
        f.writelines(device_id)
    for id in datastream_ids:
        add_datastream(id,api_key,device_id)
    add_datapoints(api_key,device_id)
if key in ['r','R']:
    api_key,device_id=register_device()
    add_datapoints(api_key,device_id)
if key in ['d','D']:
    api_key,device_id=register_device()
    delete_device(api_key,device_id)
key=input()
