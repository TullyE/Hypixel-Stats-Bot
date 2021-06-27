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
worksheet = sh.sheet1

intDay = datetime.now().timetuple().tm_yday

#res = worksheet.get_all_records() #Dict
#res = worksheet.get_all_values() #list of rows
#res = worksheet.row_values(1) #prints the row that we want
#res = worksheet.col_values(1) #prints the column that we want
#res = worksheet.get('B2') #print the content of the specified row you can also print range
#print(res)
#stats = ['6/27/2021', '_vv_', 'Bedwars', 'FKDR', 94]
#worksheet.insert_row(stats, 2)

#worksheet.delete_row(2)
API_KEY = os.environ.get('API_KEY')
strPlayer = input("Who should we look up? ")

dictGames = {'d':'Duels', 'D':'Duels', 'duels':'Duels', 'Duels':'Duels','bw':'Bedwars', 'BW':'Bedwars', 'Bw':'Bedwars', 'bW':'Bedwars'}
dictGameStats = {"Duels":["bridge_doubles_wins", "bridge_four_wins", "bridge_3v3v3v3_losses", "bridge_3v3v3v3_wins", "bridge_2v2v2v2_losses", "bridge_2v2v2v2_wins", "bridge_doubles_losses", "bridge_four_losses","bridge_duel_wins", "bridge_duel_losses"]}

strGame = dictGames[input('What Game? ')]

def getInfo(call):
    r = requests.get(call)
    return r.json()

url = f'https://api.hypixel.net/player?key={API_KEY}&name={strPlayer}'
data = getInfo(url)
if data == {'success': False, 'cause': 'You have already looked up this name recently'}:
    print('you already entered this username recently')
    stat = ''
else:
    for stats in dictGameStats[strGame]:
        try:
            stat = data['player']['stats'][strGame][stats] 
            lstSheetRow = [intDay, strPlayer, strGame, stats, stat]
            worksheet.insert_row(lstSheetRow, 2)
        except:
            print(f'No data for {stats}')


#for key in stat:
#    print(key)

styles = plt.style.available
plt.style.use(styles[8])

x = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
y = [42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752]

axes = plt.gca()
axes.yaxis.grid() #Set horizontal gridlines only

plt.plot(x, y, color = '#5865f2', linestyle='-', marker = 'o', label = 'All Devs') #plot the data
plt.tick_params(axis = "x", which = "both", bottom = True, top = False)#only want ticks on the bottem not the top
plt.tick_params(axis = "y", which = "both", left = True, right = False) #only want ticks on the left not the right
plt.xticks(np.arange(x[2], x[-1]+1, 3.0)) ##How often I want a tick on the x axis

i = 0
for spine in plt.gca().spines.values():
    if i == 2:
        spine.set_visible(True)
    else:
        spine.set_visible(False)
    i += 1

plt.axis(xmin=26, xmax=35, ymin=40000, ymax=80000)
plt.savefig('test2.png',bbox_inches='tight',transparent=True, pad_inches=0)
plt.show()

#client.run(os.environ.get('DiscordToken'))