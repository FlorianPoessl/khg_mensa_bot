import urllib.request
import telegram
import config

from datetime import datetime

def dayToWrite(line):
    if 'Montag' in line:
        return 0
    elif 'Dienstag' in line:
        return 1
    elif 'Mittwoch' in line:
        return 2
    elif 'Donnerstag' in line:
        return 3
    elif 'Freitag' in line:
        return 4

weekday = datetime.today().weekday()

fp = urllib.request.urlopen("https://www.dioezese-linz.at/khg/mensa/menueplan")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()


test = mystr.splitlines()
write = False
days = ['']*7
day = []

dayToWriteVar = 0;

for i in test:
    if 'table ' in i and write == False:
        write = True
    elif '/table' in i:
        write = False
    if write:
        print(i)
        if 'sweTableRow1' in i:
            if len(day) != 0:
                days[dayToWriteVar] = day
                day = []
            dayToWriteVar = dayToWrite(i)
        if '</tr><tr><td>' in i:
            food = ''
            writeFood = True
            for char in i:
                if char == '<':
                    writeFood = False
                if writeFood:
                    food = food + char
                elif char == '>':
                    writeFood = True
            food = food.strip()
            food = food.replace('ä', 'ae')
            food = food.replace('ö', 'oe')
            food = food.replace('ü', 'ue')
            food = food.replace('ß', 'ss')
            day.append(food)
days[dayToWriteVar] = day
output = '';

mealDay = days[weekday]

if mealDay == '':
    output += 'Die Mensa hat heute leider geschlossen'

for idx, meal in enumerate(mealDay):
    menu = idx+1
    output += '<b>Option ' + str(menu) + '</b>' + '\n'
    output += meal + '\n' + '\n'

bot = telegram.Bot(token=config.bot_token)
bot.sendMessage(chat_id=-580726026, text=output, parse_mode=telegram.ParseMode.HTML)
bot.sendMessage(chat_id=-1001584796761, text=output, parse_mode=telegram.ParseMode.HTML)




