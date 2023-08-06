# Suluoya

### This is a package written by Suluoya not just for fun!

------

## Upgrade Suluoya

```python
import Suluoya as sly
sly.upgrade()
```

## Welcome

```python
import Suluoya as sly
sly.welcome()
```

## 1. Log

If you wanna print colorful text...

```python
from Suluoya.log import sprint
sprint = sprint()
#red, green, yellow, blue, magenta, cyan, white
sprint.red('Suluoya')
#hide and show text
sprint.hide()
sprint.show()
```

if you wanna log something...

```python
from Suluoya.log import slog
slog = slog('Suluoya')
#mode=0 --> \n{content}\n
#mode=1 --> {content}\n
#mode=2 --> {content}
slog.log(content='Suluoya', mode=0)
```

## 2. Stock

###                                            **surprise**!

```python
from Suluoya.stock import gui
gui()
```

### (1)Date and Holiday information

```python
from Suluoya.stock import GetDate
# if end == 'None' --> end=time.strftime("%Y%m%d", time.localtime())
StockDate = GetDate(start='20000101', end=None)
print(StockDate.start, StockDate.end, StockDate.date)
print(StockDate.holiday)
print(StockDate.day)
print(StockDate.week)
print(StockDate.month)
print(StockDate.year)
print(StockDate.weekofyear)
print(StockDate.dayofyear)
print(StockDate.Date)  # conclude all above
```

### (2)Stock Data

Reference :  http://mtw.so/5PHTs1

#### 1. Stock Data

```python
from Suluoya.stock import StockData
StockData = StockData(names=['贵州茅台', '隆基股份'],
                      start_date='2020-12-01', end_date='2020-12-31',
                      frequency="w")
stock_pair = StockData.stock_pair
codes, stock_pair, stock_data = StockData.stock_data
'''
codes --> ['sh.600519', 'sh.601012']
stock_pair --> {'贵州茅台': 'sh.600519', '隆基股份': 'sh.601012'}
stock_data --> a dataframe contained all stock data
'''
StockData.quit()  # Please don't forget it!
```

#### 2. Holiday Stock Data

```python
from Suluoya.stock import HolidayStockData
HolidayStockData = HolidayStockData(names=['隆基股份', '贵州茅台'],
                       start_date='2020-01-01',
                       end_date='2021-01-01',
                       frequency='d',
                       holiday='国庆节',
                       before=-21,
                       after=21)

HolidayNearbyDate = HolidayStockData.HolidayNearbyDate
'''
return
eg.
    start before       start            end          end after
0    2020-09-10      2020-10-01      2020-10-08      2020-10-29
'''

codes, stock_pair, stock_data = HolidayStockData.HolidayNearbyData
```

#### 3. Quarterly Stock Capacity Data

```python
from Suluoya.stock import StockAbility
sa = StockAbility(names=['贵州茅台', '隆基股份'],
                  start_year=2018, start_quater=1,
                  end_year=2019, end_quater=4)
print(sa.Range)  # [[2018, 1], [2018, 2], [2018, 3], [2018, 4], [2019, 1]]
print(sa.stock_pair)  # {'贵州茅台': 'sh.600519', '隆基股份': 'sh.601012'}
print(sa.profit)  # 盈利能力
print(sa.operation)  # 营运能力
print(sa.growth)  # 成长能力
print(sa.balance)  # 偿债能力
print(sa.cash_flow)  # 现金流量
print(sa.dupont_data)  # 杜邦指数
print(sa.AllAbility)  # above all
```

#### 4. Stock Industry and Constituent Stock

```python
from Suluoya.stock import ConstituentStock
cs = ConstituentStock()
# if names == None --> 所有股票
print(cs.StockIndustry(names=['贵州茅台', '五粮液']))  # 行业分类
print(cs.sz50)  # 上证50成分股
print(cs.hs300)  # 沪深300成分股
print(cs.zz500)  # 中证500成分股
```

### (3)calculate

#### 1. Correlation Coefficient

```python
from Suluoya.stock import calculate
calculator = calculate()
corr = calculator.correlation(x=[1, 2], y=[2, 3])
# return 2.0
```

#### 2. Random Weight

```python
from Suluoya.stock import calculate
calculator = calculate()
weights = calculator.weight(lists=['A', 'B', 'C'], mode='dict')
'''
return:
mode = dict --> 
{'A': 0.49242348564753674, 'B': 0.11949480937223582, 'C': 0.3880817049802275}
mode = list --> 
[0.6763490711333962, 0.1493319273625324, 0.17431900150407148]
'''
```

### (3) Markovitz 

#### 1. initialize

```python
from Suluoya.stock import Markovitz
Markovitz = Markovitz(names=['贵州茅台', '隆基股份'],
                      start_date='2019-01-01',
                      end_date='2020-01-01',
                      frequency="w",  # d→day,w→week，m→month
                      holiday=False,
                      holiday_name='国庆节',  # '国庆节'，'春节'...
                      before=-21, after=21,
                      no_risk_rate=0.45/5200  # 无风险利率
                      )
print(
    Markovitz.codes,
    Markovitz.stock_pair,
    Markovitz.stock_data
)
```

#### 2. calculate sharp ratio

```python
# dic_sharp contains weights,risk,rate of return and sharp ratio
# eg. weights=[0.1,0.2,0.3,0.4],stock_list=['隆基股份','五粮液','贵州茅台','宁德时代']
# if weights = [] --> weights equally!
# The stock_list should be in the names!
print(Markovitz.sharp(weights=[], stock_list=[]))
'''
return:
{'sharp': 0.08981065592712364, 
'rate': 1.349320862745098, 'risk': 15.02309843253331, 
'weight': {'贵州茅台': 0.5, '隆基股份': 0.5}}
'''
```

#### 3. portfolio

```python
# accurate=True
print(Markovitz.portfolio())
'''
return:
[{'贵州茅台': 0.7955425960965814, '隆基股份': 0.20445740390341863}, 
0.11591565430112734]
'''
# accurate=False
# The stock_list should be in the names!
# number=500 --> 500 random weights
print(Markovitz.portfolio(stock_list=[], accurate=False, number=500))
```

#### 4. example

```python
from Suluoya.stock import Markovitz
Markovitz = Markovitz(names=['贵州茅台', '隆基股份'],
                      start_date='2019-01-01',
                      end_date='2020-01-01',
                      frequency="w",
                      holiday=False,
                      holiday_name='国庆节',
                      before=-21, after=21,
                      no_risk_rate=0.45/5200
                      )
print(Markovitz.portfolio())
```

### (4) choose stocks

```python
# get data from "http://fund.eastmoney.com/data/rankhandler.aspx"
from Suluoya.stock import GetGoodStock
GetGoodStock(page=5) # page --> number of funds
```

## 3. Charts

### (1)HTML charts

```python
from Suluoya.chart import html_charts
chart = html_charts(width='1440px', height='720px',
                    page_title="Suluoya-charts",
                    theme='LIGHT')  
'''
theme:
LIGHT,DARK,CHALK,ESSOS,INFOGRAPHIC,MACARONS,PURPLE_PASSION,ROMA,ROMANTIC,SHINE,VINTAGE,WALDEN,WESTEROS,WONDERLAND
'''

x = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
y = {"商家A": [5, 20, 36, 10, 75, 90], "商家B": [6, 18, 34, 12, 55, 96]}

pie = chart.pie(weights={'A': 1, 'B': 2, 'C': 3}, label=True)

bar = chart.bar(x=x, y=y,
                reverse=False,  # 坐标轴翻转
                pictorial=False,  # 象形柱状图
                , label=True)

scatter = chart.scatter(x=x, y=y, label=False)

effect_scatter = chart.effect_scatter(x=x, y=y, label=False)

line = chart.line(x=x, y=y,
                  smooth=False,  # 曲线是否平滑
                  step=False,  # 阶梯形状
                  , label=True)

barline = chart.barline(x=x, y_bar=y, y_line=y)

river = chart.river(x=["DQ", "TY"],
                    y=[["2015/11/08", 10, "DQ"], ["2015/11/09", 15, "DQ"], ["2015/11/10", 35, "DQ"], ["2015/11/08", 35, "TY"], ["2015/11/09", 36, "TY"], ["2015/11/10", 37, "TY"]])

# Don't forget to save your chart!
chart.save(chart=pie,  # 传入之前的图形对象
           path='render')
```

### (2)cute charts

```python
#pip install cutecharts
from Suluoya.chart import cute_charts
chart = cute_charts(width="1440px", height="720px")

x = ["a", "b", "c", "d", "e", "f", "g"]
y = {"series-A": [57, 134, 137, 129, 145, 60, 49],
     "series-B": [114, 55, 27, 101, 125, 27, 105]}

line = chart.line(name='line', x=x, y=y,
                  x_label="I'm xlabel",
                  y_label="I'm ylabel")

bar = chart.bar(name='bar', x=x, y=y,
                x_label="I'm xlabel",
                y_label="I'm ylabel")

pie = chart.pie(name='pie',
                weights={'A': 1, 'B': 2, 'C': 3})

scatter = chart.scatter(name='scatter',
                        data={"series-A": [(79, 123), (76, 128)],
                              "series-B": [(112, 20), (119, 113)]
                              },
                        x_label="I'm xlabel",
                        y_label="I'm ylabel",
                        dot_size=1.5,  # 点大小
                        x_tick_count=3,  # X 轴刻度分割段数
                        y_tick_count=3,  # Y 轴刻度分割段数
                        line=False  # 是否连线
                        )

# Don't forget to save your chart!
chart.save(chart=line, path='render')
```

## 4. Crawl

### (1)crawl

```python
from Suluoya.crawl import SlyCrawl as sc
sc=sc(url='',headers={},params={},cookies={},timeout=5)
print(sc.url)
print(sc.response)
print(sc.html)
print(sc.headers)
print(sc.params)
print(sc.cookies)
'''generate a fake useragent'''
print(sc.useragent) # pip install fake_useragent
'''parsel.css'''
print(sc.selector)
'''BeautifulSoup'''
print(sc.soup)
'''it will return a **dic** which contain title,text,description,keywords,tags,image,infomation and the raw_html'''
print(sc.get_text()) # pip install goose3
'''it will return a dictionary which contain text,title,html,author,image,movies,keywords and summary.'''
print(sc.news) # pip install newspaper
'''url links'''
print(sc.links)
'''pandas.read_html'''
print(sc.tables)
```

### (2)get proxies

```python
from Suluoya.crawl import GetProxy as gp
proxies=gp(number=1)
print(proxies)
```

## 5. Download

```python
from Suluoya.crawl import SlyDownload
sd=SlyDownload(url='')
```

### (1)download music

```python
sd.download_music(path='d:\\')
```

### (2)download video

```python
# pip install you-get
sd.download_video()
```

### (3)download anything you want with an URL

```python
# pip install wget
sd.download()
```

### (4)download a big file

```python
sd.download_big_file()
```

### (5)download novel

```python
# gui 
from Suluoya.crawl import NovelDownloadGui as ndg
ndg()
```

## 6. Text

### (1)initialize

```python
from Suluoya.text import SlyText as st
st=st('Suluoya','苏洛雅')
```

### (2)translate

```python
# pip install translators
st=st('苏洛雅')
translate=st.translate
print(translate)
```

### (3)gender guess

name should be a Chinese name!

```python
# pip install ngender
st=st('苏洛雅')
gender=st.gender
print(gender)
```

### (4)text compare

accurate=True --> accurate match mode

accurate=False --> fuzzy match mode

```python
# pip install fuzzywuzzy
st=st('Suluoya','suluoya')
text_compare = st.compare(accurate=True)
print(text_compare)
```

### (5)sentiment

To download the necessary data, 

simply run "python -m textblob.download_corpora" before using it,

if something goes wrong,

then click http://mtw.so/5PIAuz, http://mtw.so/5AGaDp or http://mtw.so/5PIAyL 

```python

st = st('hello','sad')
# language='C'-->Chinese # pip install snownlp
# language='E'-->English # pip install textblob
sentiment = st.sentiment(language='E')
print(sentiment)
```
### (6)draw a heart

```python
st=st('Suluoya','苏洛雅')
st.heart
```

### (7)voice synthesis

```python
# pip install pyttsx3
st=st('Suluoya','苏洛雅')
st.voice
```
### (8)traditional Chinese to simplified Chinese

```python
# pip install zhconv
st=st('開放中文轉換')
result=st.traditional_simplified_chinese(mode='zh-hans')
print(result)
'''
zh-cn 大陆简体
zh-tw 台灣正體
zh-hk 香港繁體
zh-sg 马新简体
zh-hans 简体
zh-hant 繁體
'''
```

### (9)file statistics

word frequency statistics

```python
# pip install jieba, pdfplumber, python-docx, zhon
from Suluoya.text import file_statistics as fs
fs()
```

## 7. DataFrame

### (1)initialize

```python
from Suluoya.dataframe import SlyDataFrame as sdf
import pandas as pd
df = pd.read_csv('https://sakai.unc.edu/access/content/group/3d1eb92e-7848-4f55-90c3-7c72a54e7e43/public/data/bycatch.csv')
sdf=sdf(df)
print(sdf.df)
```

### (2)report

```python
# pip install pandas_profiling
sdf.report
#This will make a html,just look for and open it!
```

### (3)gui

```python
#pip install pandasgui
sdf.gui
```

### (4)sweetviz

```python
# pip install sweetviz
sdf.sweetviz
#This will also make a html,just look for and open it!
```

## 8. Others


### (1)If you wanna get text from your clipboard...

```python
import Suluoya as sly
sly.get_clipboard(show=True)
a = sly.get_clipboard()
print(a)
```

### (2)If you wanna get content from a file...

Currently support 'doc','docx','ppt','pptx','txt'

```python
# pip install textract
import Suluoya as sly
content = sly.get_content(file=r'c:\lalala\1.docx')
print(content)
```

### (3) make a QRcode

fill in an url or some strings in content

fill in the path of the png in name

```python
# pip install MyQR
import Suluoya as sly
sly.QRcode(content='', name='')
```

### (4)auto import

If you wanna auto import some packages...

use"import Suluoya.Import as SI" instead of "import pandas as pd"...

```python
#pip install pyforest
#pass
import pandas as pd
import numpy as np
...
df = pd.Dataframe()
#now
import Suluoya.Import as SI
df = pd.Dataframe() # directly
SI.check() # just to check your import by using SI,can be omitted
# ps. go and see a file named "auto_imports.py"!
```
