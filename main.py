# 不知道怪物戰傳傳遞的參數pcrash的意思是什麽 目前填個2就好了 注意到活动关卡的pcrash值是1
# 如果活動不能戰鬥但可以領取獎勵的話 獲取當前活動的方法能正常運行嗎
# 自動打完活動關卡的功能還未測試過
import angel_link_login
import angel_link_request
import mission
import daily
import event
# {'code': -32522} 认证过期
# {'code': -32570} 无效的认证
# {'code': -32601} 写在头部的调用方法不正确
# {'code': -280104} 没有可以领取的广播道具(执行的操作不合法)
# {'code': 160008} 不在BattleEvent(活动关卡)开放的时间之内
token = angel_link_login.get_angel_link_token("braveteen@outlook.com", "pqowieu1234")
# 日常登录
login_info = angel_link_request.post_req('Player', 'getInitData', {'params': {}, 'attr': {}}, token)
print("angel link daily login success, stamina is", login_info['result']['player_data']['action_energy']['now'])
# 获取广播
radio_info = angel_link_request.post_req('Harvest', 'getStatus', {'params': {}}, token)
print("radio stocked stamina is", radio_info['result']['generator']['g3']['amount'])
# 收获广播
radio_result = angel_link_request.post_req('Harvest', 'execReceive', {'params': {'generators': [1, 2, 3, 4]}}, token)
try:
    print("radio receive successed now stamina is", radio_result['result']['player_data']['action_energy']['now'])
except Exception:
    print("radio receive stamina failed")
daily.daily_resource(token)
daily.daily_knockout(token)
daily.daily_breedbattle(token)
event.event(token)
# 领取所有可以领取的任务奖励
mission.receive_mission_reward(token)
# 考虑到完成任务可能领取了体力 再打一次活动
event.event(token)