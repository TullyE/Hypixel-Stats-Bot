from matplotlib import pyplot as plt
import numpy as np
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv() #take envirment variables from .env
import gspread #pip install gspread
from datetime import date, datetime

gc = gspread.service_account_from_dict(json.loads(os.environ.get('credentials'))) 
sh = gc.open_by_key('119aFQyS4gKwkqjDKhrxLkEuEA5WxFfz5rNm8OiPI4T0')
worksheet = sh.sheet1 #set the worksheet within google sheets
lstRows = worksheet.get_all_values() #list of rows

intDay = datetime.now().timetuple().tm_yday

API_KEY = os.environ.get('API_KEY')

dictGames = {'d':'Duels', 'D':'Duels', 'duels':'Duels', 'Duels':'Duels','bw':'Bedwars', 'BW':'Bedwars', 'Bw':'Bedwars', 'bW':'Bedwars'}
dictGameStats = {"Duels":["bridge_doubles_wins", "bridge_four_wins", "bridge_3v3v3v3_losses", "bridge_3v3v3v3_wins", "bridge_2v2v2v2_losses", "bridge_2v2v2v2_wins", "bridge_doubles_losses", "bridge_four_losses","bridge_duel_wins", "bridge_duel_losses"]}

strPlayer = input("Who should we look up? ")
strPlayer2 = input("Who should we look up? ")
strGame = dictGames[input('What Game? ')]

def getInfo(call):
    r = requests.get(call)
    return r.json()
def graph(x1, y1, x2 = [], y2 = [], title = ''):
    styles = plt.style.available
    plt.style.use(styles[8])

    axes = plt.gca()
    axes.yaxis.grid() #Set horizontal gridlines only
    if x2 and y2:
             plt.plot(x2, y2, color = 'r', marker = 'o') #plot the data
    plt.plot(x1, y1, color = 'k', linestyle='-', marker = 'o') #plot the data
    plt.tick_params(axis = "x", which = "both", bottom = True, top = False)#only want ticks on the bottem not the top
    plt.tick_params(axis = "y", which = "both", left = True, right = False) #only want ticks on the left not the right
    #plt.xticks(np.arange(x1[2], x1[-1]+1, 10.0)) ##How often I want a tick on the x axis

    i = 0
    for spine in plt.gca().spines.values():
        if i == 2:
            spine.set_visible(True)
        else:
            spine.set_visible(False)
        i += 1

    #plt.axis(xmin=, xmax=35, ymin=40000, ymax=80000)
    plt.savefig(f'{title}.png',bbox_inches='tight',transparent=True, pad_inches=0)
    plt.show()
def updateSheet(player, game):
    url = f'https://api.hypixel.net/player?key={API_KEY}&name={player}'
    data = getInfo(url)
    if data == {'success': False, 'cause': 'You have already looked up this name recently'}:
        print('you already entered this username recently')
        stat = ''
    else:
        for stats in dictGameStats[strGame]:
            try:
                stat = data['player']['stats'][game][stats] 
                lstSheetRow = [intDay, player, game, stats, stat]
                worksheet.insert_row(lstSheetRow, 2)
            except:
                lstSheetRow = [intDay, player, game, stats, 0]
def purge(Day):
    lstRows = worksheet.get_all_values()
    if int(Day) == 0:
        i = 1
        while i < len(lstRows):
            worksheet.delete_rows(i+1, len(lstRows))
            break
    i = 1
    while i < len(lstRows):
        if int(Day)-14 > int(lstRows[i][0]):
            worksheet.delete_rows(i+1, len(lstRows))
        i += 1
def duelsToXY(player, targetStat):
    x = []
    y = []
    for rows in lstRows:
        if (rows[1] == player) and (rows[3] == targetStat):
            y.append(rows[4])
            x.append(rows[0])
    return x, y
for stats in dictGameStats['Duels']:
    x2 = duelsToXY(strPlayer2, stats)[0]
    y2 = duelsToXY(strPlayer2, stats)[1]
    print(x2, y2)
    graph(duelsToXY(strPlayer, stats)[0], duelsToXY(strPlayer, stats)[1], x2, y2, stats) #duelsToXY(strPlayer2, stats)[0], duelsToXY(strPlayer2, stats)[1],
#client.run(os.environ.get('DiscordToken'))