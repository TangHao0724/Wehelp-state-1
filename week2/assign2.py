import re


def func1(name: str):
    # 流程
    # 1.判斷輸入角色取得角色座標
    # 2.使用for迴圈遍歷所有角色距離
    #  a. 取近似值畫黑線去判斷
    #  b. isR去設定左右區域位置 (如果改位置會出事)
    # 3. 取最大值與最小值print

    cha_table = {
        "悟空":(0,0),
        "特南克斯":(1, -2),
        "貝吉塔":(-4, -1),
        "辛巴":(-3, 3),
        "丁滿":(-1, 4),
        "弗利沙":(4, -1),
    }
    # 所選角色座標
    target = cha_table.get(name)
    if target == None:
        print("查無此人")
        return
    
    # 查詢所有位置表
    distance_list = []
    target_side = True if (-1.3 * target[0]) - target[1] + 1.7 > 0 else False
    for namel, vector in cha_table.items():
        if namel != name:
            cha_side = True if (-1.3 * vector[0]) - vector[1] + 1.7 > 0 else False
            dis = abs(target[0] - vector[0]) + abs(target[1] - vector[1])
            if target_side != cha_side:
                dis += 2
            distance_list.append([namel, dis])
                
    # 尋找極端值
    maxdis:list = max(d for _, d in distance_list)
    mindis:list = min(d for _, d in distance_list)
    # 列表顯示
    maxdis_li:list  = [n for n, d in distance_list if d == maxdis]
    mindis_li:list  = [n for n, d in distance_list if d == mindis]
    print("最遠"+("、".join(maxdis_li))+"；最近"+("、".join(mindis_li)))

func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")

services=[
        {"name":"S1", "r": 4.5 , "c":1000},
        {"name":"S2", "r":3, "c":1200},
        {"name":"S3", "r":3.8, "c":800}
    ]
o_list = []
def func2(ss, start, end, criteria):
    # 範例中：Ｃ：價格　criteria：條件
    # 定位練習，先查早是否可以訂，確認定位後加入list(由前往後查)。加入list前檢查是否可以，如果無法回傳sorry
    # { "services[name]" : (start,end)}
    # return 字串
    # 流程
    # 1. 建立預約表(start, end, criteria)
    # 2. 檢查時間(這裡return sorry)
    # 3. 檢查預約條件(這裡return sorry)獲得service[name] 寫regex判斷
    # 4. 添加予許預約的預約
    type = ""
    oprator = ""
    value = ""
    criteria_match = re.search(r"([A-Za-z]+)\s*(>=|<=|==|!=|>|<|=)\s*(.+)",criteria)
    if criteria_match:
        type = criteria_match.group(1)
        oprator = criteria_match.group(2)
        value = criteria_match.group(3)
    else:
        return print("Sorry")
    if type == "name" and not (value.startswith("'") or value.startswith('"')):
        criteria = f"{type}=='{value}'"
    service = list(filter(lambda x:eval(criteria,{},x),services))
    if not service:
        return print("Sorry")
    
    def find_service(service,oprator):
        may = {}
        match oprator:
            case ">=":
                may = min(service, key=lambda x: x[type])
            case "<=":
                may = max(service, key=lambda x: x[type])
            case "=":
                may = service[0]
        return may
    
    def check_time(name,s,e ,o_list):
        if not any(item["name"] == name for item in services):
            return True
        order_TRan= range(s,e)
        total_Tlist = [ range(o[name][0], o[name][1]) for o in o_list if name in o]
        # 若有任一重疊回傳 False
        for ran in total_Tlist:
            # 檢查是否有交集
            if (order_TRan.start < ran.stop and ran.start < order_TRan.stop):
                return False
        return True
    
    loop_service = service.copy()
    while len(loop_service) > 0 :
        ans  = find_service(loop_service,oprator)
        if not ans :
            print("Sorry")
            break
        if check_time(ans["name"],start, end, o_list):
            o_list.append({ans["name"]:(start, end)})
            print(ans["name"])
            break
        else:
            loop_service.remove(ans)
            continue
    else:
        print("Sorry")


        

func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2
func2(services, 8, 9, "c<=1500")


def func3(index:int):
    # 從25開始-2、-3、+1、+2的數列。
    # 尋找建立數列的方法，輸入指定位置，回傳該位置的數值
    ans = 25
    times = int((index)/4)
    left = (index) % 4
    # print("index",index,"times",times,"left",left)
    loop= [-2,-3,1,2]
    ans = (ans + times* sum(loop)) + sum(loop[0:left])
    print(ans)

func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6

# sp是一個list[]代表目前車廂的最大載客狀態 ,
# stat代表目前可否載客0是true可以服務，1是false不能服務。 
# n代表需求人數，
def func4(sp, stat, n):
    state = [not bool(int(s)) for s in stat]
    can_sp = []

    for i,v in enumerate(sp):
        if state[i]:
            can_sp.append((i,v))
    ans = sorted(list(filter(lambda x : x[1] >= n , can_sp)) ,key=lambda x:x[1])
    if ans == []:
        print(max(can_sp, key=lambda x: x[1])[0])
    else:
        print(ans[0][0])

func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4) # print 4
func4([4, 6, 5, 8], "1000", 4) # print 2