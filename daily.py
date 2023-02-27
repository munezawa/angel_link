import angel_link_request


def daily_resource(token):
    for i in range(2):
        golden_info = angel_link_request.post_req('BattleDaily', 'skip', {'params': {'du_lv': 1, 'st_lv': 8, 'difficulty': 1, 'skip_num': 1, 'category': None, 'event_id': None}}, token)
        if(golden_info['error']!=None):
            print("golded quest skip failed")
            break
        print("golden quest skip once")
    for i in range(2):
        experience_info = angel_link_request.post_req('BattleDaily', 'skip', {'params': {'du_lv': 2, 'st_lv': 8, 'difficulty': 1, 'skip_num': 1, 'category': None, 'event_id': None}}, token)
        if(experience_info['error']!=None):
            print("experience quest skip failed")
            break
        print("experience quest skip once")
    return 0


def daily_knockout(token):
    knockout = angel_link_request.post_req('BattleKnockout', 'skip', {'params': {'du_lv': 3, 'difficulty': 1}}, token)
    if(knockout['error']!=None):
        print("knockout quest skip failed")
        return -1
    print("knockout quest skip success")
    return 0


def daily_breedbattle(token):
    breedbattle_info = angel_link_request.post_req('BattleBreed', 'getRivals', {'params': {}}, token)
    data = {'params': {'season_id': 7,'rivals_key': 'ue7FRiFGTB8l','rivals_id': 3,'deck': {'c1': {'chara_id': '000000'},'c2': {'chara_id': '019IAC'},'c3': {'chara_id': '151FFU'},'c4': {'chara_id': '164WYV'},'c5': {'chara_id': '003BOS'},'c6': {'chara_id': '015LCY'}},'enchant': {'c1': '036LLU','c2': '039MZS','c3': '094PSW','c4': '005OGC','c5': '001IUX','c6': '087GJX'},'cheer': []}}
    data['params']['rivals_key'] = breedbattle_info['result']['rivals_key']
    battle_info = angel_link_request.post_req('BattleBreed', 'start', data, token)
    print("try initialize breed battle")
    if(battle_info['error']!=None):
        print("daily breed battle failed")
        return -1
    angel_link_request.post_req('BattleBreed', 'exec', {'params': {'battle_id': battle_info['result']['battle_id'], 'battle_key': battle_info['result']['battle_key']}}, token)
    print("breed battle started")
    # 直接投降
    angel_link_request.post_req('BattleBreed', 'end', {'params': {'battle_id': battle_info['result']['battle_id'],'battle_key': battle_info['result']['battle_key'],'result': 4,'star': 0,'pcrash': 2,'progress': '[]','damage_give': 0,'damage_take': 0}}, token)
    print("breed battle finished")
    return 0