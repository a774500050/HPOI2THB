import requests
from bs4 import BeautifulSoup


def getHTMLText(url, code="utf-8", timeout=30):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        r.encoding = code
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except Exception as e:
        print('Error while getting html text: ', e)
        return ""


def processTDLeft(tdObject):
    """
    turn TDLeft's value into infoDict's Key
    :param tdObject:
    :return:formatted text
    """
    text = tdObject.text.replace(": ", "")
    refDict = {
        "名称": "name",
        "定价": "price",
        "发售日": "data",
        "比例": "scale",
        "原型": "prototyper",
        "原画": "illust",
        "角色": "chara",
        "尺寸": "size"
    }
    if text in refDict:
        return refDict[text]
    else:
        return None


def processTDRight(tdObject):
    alist = tdObject.find_all('a')
    if alist:
        text = "，".join([a.text.strip() for a in alist])
    else:
        text = tdObject.text.strip()
    # print(text)
    return text


def processKeyValue(key, value):
    """
    process certain key's value
    :param key:
    :param value:
    :return:formatted key and value
    """
    if key == "size":
        value = value[2:]
        return key, value
    if key == "price":
        value = value.replace(",", "")[:value.find("日元") + 1]
        return key, value
    return key, value


def getPVCInfo(url):
    infoDict = {
        "name": "",
        "price": "",
        "data": "",
        "scale": "",
        "prototyper": "",
        "illust": "",
        "chara": "",
        "size": ""
    }
    html = getHTMLText(url)
    mainTable = html.select(
        "body > div.container.container-main > div.row > div.col-md-17 > div:nth-child(1) > div > div > "
        "div.col-xs-24.col-sm-15.col-md-15.col-lg-16 > table")
    #   select mainTable
    trList = mainTable[0].find_all("tr")  # form trList
    for tr in trList:
        left = tr.select("td.info-box-left")
        if len(left) != 0:
            # print(left)
            key = processTDLeft(left[0])
        else:
            continue
        right = tr.select("td.info-box-right")
        if len(right) != 0:
            value = processTDRight(right[0])
        else:
            continue
        if key is not None and value is not None:
            key, value = processKeyValue(key, value)
            infoDict[key] = value
    out = formResult(infoDict)
    return out


def formResult(infoDict):
    result = f'''{{{{周边头部}}}}
    
== 模型信息 ==
{{{{模型周边信息|
| 类别 = PVC
| 系列 = 无
| 译名 = 
| 原型师 = {infoDict.get('prototyper')}
| 原画师 = {infoDict.get('illust')}
| 比例 = {infoDict.get('scale')}
| 尺寸 = {infoDict.get('size')}
| 状态 = 
| 发售价格 = {infoDict.get('price')}
| 发售日期 = {infoDict.get('data')}
| 公式网站 = 
| 备注 = 
}}}}

== 参考图片 ==
{{{{#vardefine:图片名|{{{{去杠|{{{{FULLPAGENAME}}}}}}}}}}}}'''

    return result


# url for test
# url = "https://www.hpoi.net/hobby/38120"
url = input("Please input HPOI Wiki URL:")

print(getPVCInfo(url))
