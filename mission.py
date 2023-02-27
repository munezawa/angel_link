import angel_link_request
# 领取日常任务
def receive_mission_reward(token):
    mission_info = angel_link_request.post_req('Mission', 'getStatusDaily', {'params': {}}, token)
    cleared_mission_list = []
    for i in mission_info['result']['mission']:
        if(mission_info['result']['mission'][i]['clear'] == True and mission_info['result']['mission'][i]['receive'] == False):
            cleared_mission_list.append(i[1:])
    print(cleared_mission_list, "are cleared daily missions")
    if(len(cleared_mission_list) <= 0):
        print("no daily mission cleared")
        return 0
    data = {'params': {'mission': []}}
    data['params']['mission'] = cleared_mission_list
    reward_info = angel_link_request.post_req('Mission', 'execClearDaily', data, token)
    try:
        print(reward_info['result']['reward'], "daily mission rewards received")
    except Exception:
        print("unknow error cause daily mission reward receive fail")
    return 0


# 领取活动任务
def receive_event_mission_reward(params, token):
    mission_info = angel_link_request.post_req('Mission', 'getStatusEvent', params, token)
    cleared_mission_list = []
    for i in mission_info['result']['mission']:
        if(mission_info['result']['mission'][i]['clear'] == True and mission_info['result']['mission'][i]['receive'] == False):
            cleared_mission_list.append(i[1:])
    print(cleared_mission_list, "are cleared event missions")
    if(len(cleared_mission_list) <= 0):
        print("no event mission cleared")
        return 0
    data = {'params': {'event_id': params['params']['event_id'], 'mission': []}}
    data['params']['mission'] = cleared_mission_list
    reward_info = angel_link_request.post_req('Mission', 'execClearEvent', data, token)
    try:
        print(reward_info['result']['reward'], "event mission rewards received")
    except Exception:
        print("unknow error cause event mission reward receive fail")
    return 0