function func1(name){
    const cha_table  = {
        "悟空": [0, 0],
        "特南克斯": [1, -2],
        "貝吉塔": [-4, -1],
        "辛巴": [-3, 3],
        "丁滿": [-1, 4],
        "弗利沙": [4, -1]
    };

   let target = cha_table[name];
   target ?? console.log("查無此人");

   let dis_list ={};
   let target_side = (-1.3 * target[0]) - target[1] + 1.7 > 0 ? false: true;
   for (const i in cha_table){
       if (name === i) continue;
       const vector = cha_table[i]
       cha_side =  (-1.3 * vector[0]) - vector[1] + 1.7 > 0 ? false: true;

       let dis = Math.abs(target[0] - vector[0]) + Math.abs(target[1] - vector[1]);
       if (target_side !== cha_side) dis += 2;
       dis_list[i] = dis ; 
   }
   const dis_pairs = Object.entries(dis_list); 

   const maxDis = Math.max(...dis_pairs.map(x => x[1]));
   const minDis = Math.min(...dis_pairs.map(x => x[1]));

   const maxDisL = dis_pairs.filter(x => x[1] === maxDis).map(i => i[0]);
   const minDisL = dis_pairs.filter(x => x[1] === minDis).map(i => i[0]);
   console.log(`最遠${maxDisL.join("、")}；最近${minDisL.join("、")}`);
}
func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")

const services=[
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
];
let oList =[]
function func2(ss, start, end, criteria){

    let criteria_arr= criteria.match(/([A-Za-z]+)\s*(>=|<=|==|!=|>|<|=)\s*(.+)/);
    const [_,type,opretor,value] = criteria_arr;
    
    if (type === "name" && (!(value.startsWith("'")) || !(value.startsWith('"')))){
        criteria = `"${name}"==="${value}"`;
    }
    const service = ss.filter(x => {
        const {name,r,c } = x ;
        return eval(criteria);
        }
    );
    if (service.length === 0) {
        console.log("Sorry");
        return;
    }
    function find_service(services,oprator){
        may= {}
        switch (oprator){
            case ">=":
                may = services.reduce((p, c) => p[type] < c[type] ? p : c);
                break;
            case "<=":
                may = services.reduce((p, c) => p[type] > c[type] ? p : c);
                break;
            case "=":
                may = service[0]
                break;

        }
        return may
    }
    function check_time(n,s,e,oList){
        if (!(ss.some( x => x["name"] === n))) {
            return true;
        }
        for (const o of oList) {
        if (n in o) {
                const bookedStart = o[n][0]; 
                const bookedEnd = o[n][1];   

                if (s < bookedEnd && e > bookedStart) {
                    return false; // 有重疊，直接淘汰
                }
            }
        }
         return true;
    }
    let loop_service = service;
    while (loop_service.length > 0){
        let ans = find_service(loop_service,opretor);
        if (!ans){
            console.log("Sorry");
            break;

        }
        if (check_time(ans.name,start,end,oList)){
            oList.push({[ans.name]: [start, end]});
            console.log(ans.name);
            break;
        }else{
            loop_service = loop_service.filter(item => item.name !== ans.name);
            continue;
        }
    }
}
func2(services, 15, 17, "c>=800");// S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2
func2(services, 8, 9, "c<=1500"); // S1

function func3(index){
    let ans = 25;
    const times = Math.floor(index / 4);
    const left = index %4;
    const loop = [-2,-3,1,2]
    const loopSum = loop.slice(0, left).reduce((sum, c) => sum + c, 0);
    ans = (ans+times* loop.reduce((sum,c) => sum + c,0)) + loopSum;
    console.log(ans);
}
func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6

function func4(sp, stat, n){
    let state = []
    let stat_arr = [...stat]
    let can_sp = []
    for (const s of stat_arr){
        if (s === "0"){
            state.push(true);
        }else{
            state.push(false);
        }
    }
    console.log(state)
    for(const [i,v] of sp.entries()){
        if (state[i]){
            can_sp.push([i,v]);
        }
        
    }
    console.log("can_sp",can_sp)
    let ans = can_sp.filter(x => x[1] >= n).sort((a,b) => a[1] - b[1]);
    console.log("ans",ans)
    if (ans.length === 0){
        let max = can_sp.reduce((p, c) => p[1] > c[1] ? p : c);
        console.log(max[0]);
    }else{  
        console.log(ans[0][0]);
    }


}
func4([3, 1, 5, 4, 3, 2], "101000", 2); // print 5
func4([1, 0, 5, 1, 3], "10100", 4); // print 4
func4([4, 6, 5, 8], "1000", 4); // print 2
