import json 
import os
import re

# 加载配置文件
with open('Info.json','r') as file:
    Info = json.load(file)

# world文件夹里需要修改UUID文件的文件夹
dirs = []
advancements_path = os.path.join(Info['root_dir'], "world/advancements")
dirs.append(advancements_path)
playerdata_path = os.path.join(Info['root_dir'], "world/playerdata")
dirs.append(playerdata_path)
stats_path = os.path.join(Info['root_dir'], "world/stats")
dirs.append(stats_path)

#需要修改的玩家信息
players = []
for playerinfo in Info['player']:
    player_name = playerinfo['name']
    player_OnlineUUID = playerinfo['Online_UUID']
    player_OfflineUUID = playerinfo['Offline_UUID']
    players.append([player_name, player_OnlineUUID, player_OfflineUUID])


#判断转换模式并修改server.properties中的online-mode
server_properties_path = Info['root_dir'] + "/" + "server.properties"
with open(server_properties_path, 'r') as file:
    server_properties = file.readlines()
with open(server_properties_path, 'w') as file:
    for line in server_properties:
        if line.startswith('online-mode='):
            if 'true' in line:
                print("Mode Change: Online -> Offline")
                line = 'online-mode=false\n'
                mode_id = 1
            elif 'false' in line:
                print("Mode Change: Offline -> Online")
                line = 'online-mode=true\n'
                mode_id = 2
        file.write(line)


#根据模式改写usercache.json的每项uuid
usercache_path = Info['root_dir'] + "/" + "usercache.json"
with open(usercache_path, 'r') as file:
    usercache = json.load(file)
    for item in usercache:
        for j in range(len(players)):
            if item['name'] == players[j][0]:
                if mode_id == 1:
                    item['uuid'] = players[j][2]
                elif mode_id == 2:
                    item['uuid'] = players[j][1]
with open(usercache_path, 'w') as file:
    json.dump(usercache, file, indent=4)

#根据模式改写ops.json的每项uuid
ops_path = Info['root_dir'] + "/" + "ops.json"
with open(ops_path, 'r') as file:
    ops = json.load(file)
for item in ops:
    for j in range(len(players)):
        if item['name'] == players[j][0]:
            if mode_id == 1:
                item['uuid'] = players[j][2]
            elif mode_id == 2:
                item['uuid'] = players[j][1]
with open(ops_path, 'w') as file:
    json.dump(ops, file, indent=4)                                                     

#根据模式改写usernamecache.json的每项uuid
usernamecache_path = Info['root_dir'] + "/" + "usernamecache.json"
with open(usernamecache_path, 'r') as file:
    usernamecache = json.load(file)
for key, value in list(usernamecache.items()):
    for j in range(len(players)):
        if value == players[j][0]:
            if mode_id == 1:
                usernamecache[players[j][2]] = usernamecache.pop(key)
            elif mode_id == 2:
                usernamecache[players[j][1]] = usernamecache.pop(key)
with open(usernamecache_path, 'w') as file:
    json.dump(usernamecache, file, indent=4)                                 


#根据模式改写的文件名的uuid
for k in range(len(dirs)):
    for filename in os.listdir(dirs[k]):
        if filename.endswith('.json'):
            name = filename[:-5]
            for j in range(len(players)):
                if name == players[j][mode_id] and mode_id == 1:
                    new_name = players[j][2] + ".json"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))
                elif name == players[j][mode_id] and mode_id == 2:
                    new_name = players[j][1] + ".json"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))
        elif filename.endswith('.dat_old'):
            name = filename[:-8]
            for j in range(len(players)):
                if name == players[j][mode_id] and mode_id == 1:
                    new_name = players[j][2] + ".dat_old"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))
                elif name == players[j][mode_id] and mode_id == 2:
                    new_name = players[j][1] + ".dat_old"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))
        elif filename.endswith('.dat'):
            name = filename[:-4]
            for j in range(len(players)):
                if name == players[j][mode_id] and mode_id == 1:
                    new_name = players[j][2] + ".dat"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))
                elif name == players[j][mode_id] and mode_id == 2:
                    new_name = players[j][1] + ".dat"
                    file_path = os.path.join(dirs[k], filename)
                    os.rename(file_path, os.path.join(dirs[k], new_name))

print("Done!")