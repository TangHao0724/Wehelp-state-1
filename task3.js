
const url31 ="https://cwpeng.github.io/test/assignment-3-1";
const url32 ="https://cwpeng.github.io/test/assignment-3-2";
let count = 3;
let limit = 13;
export async function main() {
    let baseData = await getData(url31);
    let imgData = await getData(url32);
    let bWebData = await setData(baseData,imgData,0,3);
    let cWebData = await setData(baseData,imgData,count,limit);
    // console.log(count);
    // console.log(limit);

    for(const i in bWebData){
        createBar(i,bWebData);
    }
    for(const i in cWebData){
        createContent(i,cWebData)
    }
}
async function getData(url) {
    try {
        const response = await fetch(url);
        if(!response.ok){
            throw new Error(`state：${response.status}`);
        }
        const result = await response.json();
        // console.log(result);
        return result;
        
    }
    catch(err){
        // console.error(err);
    }
    
}

// 先加limit，從count開始增加webdata,在執行createContent
export async function load(add){
    let baseData = await getData(url31);
    let imgData = await getData(url32);
    count += add+3;
    limit += add+3;
    let data = await setData(baseData,imgData,count,limit);
    
    for(const i in data){
        createContent(i,data);
    }
        if (data.length < 10){
        document.getElementById("more-bt").remove();
    }

}

async function setData(baseData,imgData,count, limit) {
    let webData = [];

    for (let row of baseData["rows"].slice(count, limit)) {  
        let data = {};
        data.name = String(row["sname"]);
        let findPic = imgData["rows"].find(x => x.serial === row.serial);
        let img;
        if (findPic) {
            const imgArray = findPic["pics"].split(/(?=\/resources\/images\/)/);
            img = imgArray[0];
        }
        data.imgUrl = `${imgData["host"]}${img}`;
        webData.push(data);
    }
    return webData;
}
function createBar(index,webData){
    let pBar = document.createElement("div");
    pBar.classList.add("promotion-bars",(`bar-${Number(index)+1}`));

    let pImg = document.createElement("img");
    pImg.classList.add("promotion-img");
    pImg.src = webData[index]["imgUrl"]

    let pContent = document.createElement("span");
    pContent.classList.add("promotion-content");
    const content = document.createTextNode(webData[index]["name"]);

    pContent.appendChild(content);
    pBar.appendChild(pImg);
    pBar.appendChild(pContent);

    let pSection = document.getElementById("promotion-section");
    pSection.appendChild(pBar);
}
function createContent(index,webData){
    let cArt = document.createElement("article");
    cArt.classList.add("content-block");

    let cImg = document.createElement("img");
    cImg.classList.add("content-img");
    cImg.src = webData[index]["imgUrl"]

    let cStar = document.createElement("img");
    cStar.classList.add("content-star");
    cStar.src = "star.png";

    let cContent = document.createElement("span");
    cContent.classList.add("content-img-title");
    const content = document.createTextNode(webData[index]["name"]);

    cContent.append(content);
    cArt.append(cImg);
    cArt.append(cStar);
    cArt.append(cContent);

    let cSection = document.getElementById("content-section");
    cSection.appendChild(cArt);
}
