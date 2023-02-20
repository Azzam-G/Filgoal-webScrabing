import requests
from bs4 import BeautifulSoup
import csv

# Check the month and day Entered
while True:
  date = input("Please Enter a Date in the Following Format YYYY-MM-DD: ")
  year,month,day = date.split('-')
  year = int(year)
  month = int(month)
  day = int(day)
  if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
      max_days = 31
  elif month == 4 or month == 6 or month == 9 or month == 11:
      max_days = 30
  elif year%4==0 and year%100!=0 or year%400==0:
      max_days = 29
  else:
      max_days = 28

  if month < 1 or month > 12:
      print("Entered Date is InValid!")
      print("Check The Range of Month")

  elif day < 1 or day > max_days:
      print("Entered Date is InValid!")
      print("Check The Range of Day")
  else:
      break

page = requests.get(f"https://www.filgoal.com/matches/?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src,"lxml")
    matches_detailes = []
    filter_soup = soup.find("div", {'id': 'match-list-viewer'})
    champioships = filter_soup.find_all("div", {'class': 'mc-block'})

    def get_match_info(champioships):
        champioship_title = champioships.contents[1].find("span").text.strip() #.text() to get the text only & .strip() to delete the space in both side so only return the text
        all_matches = champioships.find_all("div", {'class': 'cin_cntnr'})
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
          # get teems names
          team_A = all_matches[i].find("div", {'class': 'c-i-next'}).find("div", {'class': 'f'}).find("strong").text.strip()
          team_B = all_matches[i].find("div", {'class': 'c-i-next'}).find("div", {'class': 's'}).find("strong").text.strip()

          # get scores
          score_A = all_matches[i].find("div", {'class': 'c-i-next'}).find("div", {'class': 'f'}).find("b").text.strip()
          score_B = all_matches[i].find("div", {'class': 'c-i-next'}).find("div", {'class': 's'}).find("b").text.strip()
          match_result =  "{} - {}".format(score_A, score_B)

          # get match time
          match_time_find = all_matches[i].find("div", {'class': 'match-aux'}).find_all('span')
          match_time = match_time_find[-1].text.strip()

          # add matches info to matches_detailes
          matches_detailes.append({"نوع البطولة": champioship_title,"الفريق الأول": team_A, "الفريق الثاني": team_B, "موعد المباراة": match_time, "النتيجة": match_result})

    for i in range(len(champioships)):
      get_match_info(champioships[i])

    keys = matches_detailes[0].keys()

    with open('/Users/azzamgarwan/Desktop/PythonProjects/filgoal/matches-details.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_detailes)
        print("file created")


main(page)
