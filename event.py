import angel_link_request
import random
import time

def get_current_stamina(token):
    return angel_link_request.post_req('Player', 'getInitData', {'params': {}, 'attr': {}}, token)['result']['player_data']['action_energy']['now']


def skip_event_quest(event_id, token):
    stamina = get_current_stamina(token)
    print("current stamina is", stamina)
    if(stamina < 10):
        print("now enough stamina to skip event")
        return 1
    angel_link_request.post_req('BattleEvent', 'skip', {'params': {'du_lv': 20,'st_lv': 12,'difficulty': 1,'skip_num': int(stamina/10),'category': None,'event_id': 'EVE'+str(event_id)}}, token)
    print(event_id, "quest cleared times", int(stamina/10))
    return 0


def clear_event_quest(event_id, token):
    stamina = get_current_stamina(token)
    print("current stamina is", stamina)
    if(stamina < 120):
        print("not enough stamina to clear event")
        return 1
    for i in range(1, 13):
        battle_info = angel_link_request.post_req('BattleEvent', 'start', {'params': {'du_lv': 20,'st_lv': i,'difficulty': 1,'deck': {'c1': {'chara_id': '000000'},'c2': {'chara_id': '094PSW'},'c3': {'chara_id': '116UHJ'},'c4': {'chara_id': '112STE'},'c5': {'chara_id': '034ICX'},'c6': {'chara_id': '155ZDR'}},'enchant': {'c1': '087GJX','c2': '173SDI','c3': '161ZEF','c4': '069JTH','c5': '031VTK','c6': '019IAC'},'cheer': [],'event_id': 'EVE'+str(event_id)}}, token)
        if(battle_info['error']!=None):
            print(event_id, "event battle failed")
            return -1
        angel_link_request.post_req('BattleEvent', 'exec', {'params': {'battle_id': battle_info['result']['battle_id'], 'battle_key': battle_info['result']['battle_key']}}, token)
        print(event_id, "event quest begin", i, "consider delay several seconds  simulate reality battle")
        time.sleep(30)
        damage = random.randint(80000,105000)
        angel_link_request.post_req('BattleEvent', 'end', {'params': {'battle_id': battle_info['result']['battle_id'], 'battle_key': battle_info['result']['battle_key'], 'result': 1, 'star': 3, 'pcrash': 1, 'progress': '[[[4,4,4,4,4,4],'+str(damage)+']]'}}, token)
        print(i, "quest cleared deal overkill crash damage", damage)
    return 0

def get_event_id(token):
    # 返回-1当前没有可用的活动
    f = open(r'.\event.txt')
    event_id = int(f.readline())
    f.close()
    for i in range(10):
        event_string = 'EVE' + str(event_id + i)
        a = {'params': {'event_id': event_string}}
        b = angel_link_request.post_req('BattleEvent', 'getProgress', a, token)
        if(b['error']==None):
            print(event_string, "is available event id")
            f = open(r'.\event.txt', 'r+')
            f.write(str(event_id + i))
            f.close()
            return event_id + i
        else:
            print(event_string, "event id is not available")
    print("now no event is available")
    return -1


def event(token):
    event_id = get_event_id(token)
    event_info = angel_link_request.post_req('Mission', 'getStatusEvent', {'params': {'event_id': 'EVE'+str(event_id)}}, token)
    if(event_info['result']['mission']['m4']['clear'] == True):
        print(event_id, "event normal quest already cleared trying to skip")
        skip_event_quest(event_id, token)
        return 0
    else:
        print(event_id, "event normal quest is not finish yet trying to clear")
        clear_event_quest(event_id, token)
        print(event_id, "event clear success now trying to skip")
        skip_event_quest(event_id, token)
        return 0


    # mission.receive_event_mission_reward({'params': {'event_id': "EVE"+str(event_id)}}, token)
