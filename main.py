import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

names = {
    "Mikaela": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=164835&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Lindsey": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=30368&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Renate": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=20775&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Anja": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&competitorid=45786&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Mariles": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&competitorid=54421&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Lara": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=125871&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Janica": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&seasoncode=&competitorid=32044&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Maria": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=50980&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Tina": "https://www.fis-ski.com/DB/general/athlete-biography.html?sector=AL&competitorid=38837&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Petra": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=168809&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",

    "Marcel": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=106332&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Hermann": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&competitorid=36996&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Alberto": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&competitorid=61842&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Benjamin": "https://www.fis-ski.com/DB/general/athlete-biography.html?sector=AL&competitorid=49658&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Aksel": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=59877&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Alexis": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=127048&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Bode": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&competitorid=40317&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Henrik": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=154950&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000",
    "Marco": "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=AL&competitorid=190231&type=result&categorycode=&sort=&place=&disciplinecode=&position=&limit=5000"
}
res = pd.DataFrame()
for name in names:

    URL = names[name]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="resultdata")
    results_elements = results.find_all("div", class_="container g-xs-24")

    r = []
    for result_element in results_elements:
        r.append(
            {
                "Name": name,
                "Date": result_element.find("div", class_="g-xs-4 g-sm-4 g-md-4 g-lg-4 justify-left").text.strip(),
                "Location": result_element.find("div", class_="g-md g-lg justify-left hidden-sm-down").text.strip(),
                "Category": result_element.find("div", class_="g-md-5 g-lg-5 justify-left hidden-sm-down").text.strip(),
                "Discipline": result_element.find("div", class_="g-xs-24 justify-left clip-xs gray").text.strip(),
                "Place": result_element.find("div", class_="g-xs-24 g-sm g-md g-lg justify-right").text.strip()
            }
        )
    wc = pd.DataFrame(r).loc[pd.DataFrame(r)["Category"].isin(['World Cup', 'World Cup'])]
    wc['Date'] = pd.to_datetime(wc['Date'], format='%d-%m-%Y')
    wc['Place'] = pd.to_numeric(wc['Place'], errors='coerce')
    res = res.append(wc.sort_values(by=['Date']).reset_index(drop=True).reset_index())

# print(res)

def wins(name):
    win = ((res.loc[(res["Name"] == name) & (res["Place"] == 1)]).reset_index(drop=True).reset_index())
    win["index"] = win["index"] + 1
    win["level_0"] = win["level_0"] + 1
    return win

def podiums(name):
    win = ((res.loc[(res["Name"] == name) & (res["Place"] < 4)]).reset_index(drop=True).reset_index())
    win["index"] = win["index"] + 1
    win["level_0"] = win["level_0"] + 1
    return win

# print(podiums("Mikaela"))

# plt.plot(podiums("Mikaela")["index"], podiums("Mikaela")["level_0"], label='Shiffrin')
# plt.plot(podiums("Lindsey")["index"], podiums("Lindsey")["level_0"], label='Vonn')
# # plt.plot(podiums("Renate")["index"], podiums("Renate")["level_0"], label='Götschl')
# plt.plot(podiums("Anja")["index"], podiums("Anja")["level_0"], label='Pärson')
# # plt.plot(podiums("Mariles")["index"], podiums("Mariles")["level_0"], label='Schild')
# # plt.plot(podiums("Lara")["index"], podiums("Lara")["level_0"], label='Gut-Behrami')
# # plt.plot(podiums("Janica")["index"], podiums("Janica")["level_0"], label='Kostelic')
# # plt.plot(podiums("Maria")["index"], podiums("Maria")["level_0"], label='Höfl-Riesch')
# plt.plot(podiums("Petra")["index"], podiums("Petra")["level_0"], label='Vlhova')
# plt.plot(podiums("Marcel")["index"], podiums("Marcel")["level_0"], label='Hirscher')
# plt.plot(podiums("Hermann")["index"], podiums("Hermann")["level_0"], label='Maier')
# plt.plot(podiums("Alberto")["index"], podiums("Alberto")["level_0"], label='Tomba')
# # plt.plot(podiums("Benjamin")["index"], podiums("Benjamin")["level_0"], label='Raich')
# # plt.plot(podiums("Aksel")["index"], podiums("Aksel")["level_0"], label='Svindal')
# # plt.plot(podiums("Alexis")["index"], podiums("Alexis")["level_0"], label='Pinturault')
# # plt.plot(podiums("Bode")["index"], podiums("Bode")["level_0"], label='Miller')
# # plt.plot(podiums("Henrik")["index"], podiums("Henrik")["level_0"], label='Kristoffersen')
# plt.plot(podiums("Marco")["index"], podiums("Marco")["level_0"], label='Odermatt')
# plt.xlabel("Number of starts")
# plt.ylabel("Number of podiums")
# plt.grid()
# plt.legend()
# plt.show()
#
# plt.plot(podiums("Mikaela")["index"], podiums("Mikaela")["level_0"], label='Shiffrin')
# plt.plot(podiums("Lindsey")["index"], podiums("Lindsey")["level_0"], label='Vonn')
# plt.plot(podiums("Renate")["index"], podiums("Renate")["level_0"], label='Götschl')
# plt.plot(podiums("Anja")["index"], podiums("Anja")["level_0"], label='Pärson')
# plt.plot(podiums("Mariles")["index"], podiums("Mariles")["level_0"], label='Schild')
# plt.plot(podiums("Lara")["index"], podiums("Lara")["level_0"], label='Gut-Behrami')
# plt.plot(podiums("Janica")["index"], podiums("Janica")["level_0"], label='Kostelic')
# plt.plot(podiums("Maria")["index"], podiums("Maria")["level_0"], label='Höfl-Riesch')
# plt.plot(podiums("Petra")["index"], podiums("Petra")["level_0"], label='Vlhova')
# plt.xlabel("Number of starts")
# plt.ylabel("Number of podiums")
# plt.grid()
# plt.legend()
# plt.show()
#
#
# plt.plot(podiums("Marcel")["index"], podiums("Marcel")["level_0"], label='Hirscher')
# plt.plot(podiums("Hermann")["index"], podiums("Hermann")["level_0"], label='Maier')
# plt.plot(podiums("Alberto")["index"], podiums("Alberto")["level_0"], label='Tomba')
# plt.plot(podiums("Benjamin")["index"], podiums("Benjamin")["level_0"], label='Raich')
# plt.plot(podiums("Aksel")["index"], podiums("Aksel")["level_0"], label='Svindal')
# plt.plot(podiums("Alexis")["index"], podiums("Alexis")["level_0"], label='Pinturault')
# plt.plot(podiums("Bode")["index"], podiums("Bode")["level_0"], label='Miller')
# plt.plot(podiums("Henrik")["index"], podiums("Henrik")["level_0"], label='Kristoffersen')
# plt.plot(podiums("Marco")["index"], podiums("Marco")["level_0"], label='Odermatt')
# plt.xlabel("Number of starts")
# plt.ylabel("Number of podiums")
# plt.grid()
# plt.legend()
# plt.show()

# plt.plot(wins("Mikaela")["index"], wins("Mikaela")["level_0"], label='Shiffrin')
# plt.plot(wins("Lindsey")["index"], wins("Lindsey")["level_0"], label='Vonn')
# # plt.plot(wins("Renate")["index"], wins("Renate")["level_0"], label='Götschl')
# plt.plot(wins("Anja")["index"], wins("Anja")["level_0"], label='Pärson')
# # plt.plot(wins("Mariles")["index"], wins("Mariles")["level_0"], label='Schild')
# # plt.plot(wins("Lara")["index"], wins("Lara")["level_0"], label='Gut-Behrami')
# # plt.plot(wins("Janica")["index"], wins("Janica")["level_0"], label='Kostelic')
# # plt.plot(wins("Maria")["index"], wins("Maria")["level_0"], label='Höfl-Riesch')
# plt.plot(wins("Petra")["index"], wins("Petra")["level_0"], label='Vlhova')
# plt.plot(wins("Marcel")["index"], wins("Marcel")["level_0"], label='Hirscher')
# plt.plot(wins("Hermann")["index"], wins("Hermann")["level_0"], label='Maier')
# plt.plot(wins("Alberto")["index"], wins("Alberto")["level_0"], label='Tomba')
# # plt.plot(wins("Benjamin")["index"], wins("Benjamin")["level_0"], label='Raich')
# # plt.plot(wins("Aksel")["index"], wins("Aksel")["level_0"], label='Svindal')
# # plt.plot(wins("Alexis")["index"], wins("Alexis")["level_0"], label='Pinturault')
# # plt.plot(wins("Bode")["index"], wins("Bode")["level_0"], label='Miller')
# # plt.plot(wins("Henrik")["index"], wins("Henrik")["level_0"], label='Kristoffersen')
# plt.plot(wins("Marco")["index"], wins("Marco")["level_0"], label='Odermatt')
# plt.xlabel("Number of starts")
# plt.ylabel("Number of wins")
# plt.grid()
# plt.legend()
# plt.show()

plt.plot(wins("Mikaela")["index"], wins("Mikaela")["level_0"], label='Shiffrin')
plt.plot(wins("Lindsey")["index"], wins("Lindsey")["level_0"], label='Vonn')
plt.plot(wins("Renate")["index"], wins("Renate")["level_0"], label='Götschl')
plt.plot(wins("Anja")["index"], wins("Anja")["level_0"], label='Pärson')
plt.plot(wins("Mariles")["index"], wins("Mariles")["level_0"], label='Schild')
plt.plot(wins("Lara")["index"], wins("Lara")["level_0"], label='Gut-Behrami')
plt.plot(wins("Janica")["index"], wins("Janica")["level_0"], label='Kostelic')
plt.plot(wins("Maria")["index"], wins("Maria")["level_0"], label='Höfl-Riesch')
plt.plot(wins("Petra")["index"], wins("Petra")["level_0"], label='Vlhova')
plt.xlabel("Number of starts")
plt.ylabel("Number of wins")
plt.grid()
plt.legend()
plt.show()


plt.plot(wins("Marcel")["index"], wins("Marcel")["level_0"], label='Hirscher')
plt.plot(wins("Hermann")["index"], wins("Hermann")["level_0"], label='Maier')
plt.plot(wins("Alberto")["index"], wins("Alberto")["level_0"], label='Tomba')
plt.plot(wins("Benjamin")["index"], wins("Benjamin")["level_0"], label='Raich')
plt.plot(wins("Aksel")["index"], wins("Aksel")["level_0"], label='Svindal')
plt.plot(wins("Alexis")["index"], wins("Alexis")["level_0"], label='Pinturault')
plt.plot(wins("Bode")["index"], wins("Bode")["level_0"], label='Miller')
plt.plot(wins("Henrik")["index"], wins("Henrik")["level_0"], label='Kristoffersen')
plt.plot(wins("Marco")["index"], wins("Marco")["level_0"], label='Odermatt')
plt.xlabel("Number of starts")
plt.ylabel("Number of wins")
plt.grid()
plt.legend()
plt.show()