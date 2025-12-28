import datetime
# 日期工具
def get() -> str:
    date = datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S').split('-')
    date = '20'+date[0]+'年'+date[1]+'月'+date[2]+'日'+date[3]+'时'+date[4]+'分'
    week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    week = week_list[datetime.date.today().weekday()]
    return f'日期:{date}星期{week}'