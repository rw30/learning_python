## dupa dupa dupa
import smtplib
from  datetime import date, timedelta
import urllib.request
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#SET DATES
today = date.today()
yesterday = today + timedelta(-2)
#today = now.day
#print (today)
#print (today.year)

results = []
resultsFormatted = []

#SET URLs
resultsPageURL="http://www.basketball-reference.com/boxscores/?month=" + str(yesterday.month) + "&day=" + str(yesterday.day) + "&year=" + str(yesterday.year)

print (resultsPageURL)

#Read HTML
pageHtmlCode=urllib.request.urlopen(resultsPageURL)
srcCode = pageHtmlCode.read()

parsedCode= BeautifulSoup(srcCode,"lxml")
#parseHTML to string
parsedCodeString=srcCode.decode("utf-8")

pageStartSeparator="NBA Games</h2>" #here start the table with results
pageEndSeparator="Division Standings" # here finishes table with results

#removes unwanted HTML code, leaving only content between start & end separators

result2 = parsedCodeString.split(pageStartSeparator)[-1].split(pageEndSeparator)[0]

#this takes parsedString and puts it to list, splitting by keyword before each cell containing result
#so each line is actually one result:
multilineString = result2.split('<div class="game_summary expanded nohover">')
i=0

print ('\n\n\n')
#print (multilineString[1].split(lineStartSeparator)[-1].split(lineEndSeparator)[0] )
for listelem in  multilineString[1:] :

		homeTeamIsWinnerMarker = ""
		visitorTeamIsWinnerMarker = ""
	#if len(listelem) > 50 :
		#	print (listelem.split(homeTeamStartSeparator)[-1].split(homeTeamEndSeparator)[0] + " " +  listelem.split(visitorTeamStartSeparator)[-1].split(visitorTeamEndSeparator)[0])
		#print (listelem)
		htmlCode=BeautifulSoup(listelem,"lxml")
		listTeams = htmlCode.findAll('a')
		listScores = htmlCode.findAll('td')
		trs = htmlCode.findAll ('tr')
		for tr in trs:
			 if tr.has_attr('class') and tr['class'][0]=='winner':
			 	#print (tr.td.text)
					if tr.td.text == listTeams[2].text : #home team won game
						homeTeamIsWinnerMarker = "*"
					else: visitorTeamIsWinnerMarker = "*"
		homeTeam = listTeams[2].text
		homeTeamScore = listScores[4].text
		visitorTeam = listTeams[0].text
		visitorTeamScore = listScores[1].text

		results.append(visitorTeam +   " @ " +  homeTeam + " " + visitorTeamScore + " : " + homeTeamScore)
		resultsFormatted.append(visitorTeam +   " @ " +  homeTeam + " " + visitorTeamScore + " : " + homeTeamScore + "<br>")
		if homeTeamIsWinnerMarker == "*" :
			resultsFormatted[i] = resultsFormatted[i].replace (homeTeam, "<b>" + homeTeam + "</b>")
			print (resultsFormatted[i])
		else:
			resultsFormatted[i] = resultsFormatted[i].replace (visitorTeam, "<b>" + visitorTeam + "</b>")
		i=i+1

print (*resultsFormatted, sep="\n")
#print (results[0])
print ('\n\n\n')

### MAIL CONTENT:
recipients=["karol.kanicki@gmail.com"]#, "inigo.hernaez@clearpeaks.com"]
sender="cp.redmine.test@gmail.com"
subject = "NBA Results "
content =  ''.join(resultsFormatted)
print (type (content))

### CREATING EMAIL FROM CONTENT ABOVE
body = MIMEText(content,'html')
#msg = MIMEText(body)
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = ", ".join(recipients)
msg.attach(body)


server = smtplib.SMTP ('smtp.gmail.com', 587)
server.starttls()
server.login (sender, "admin2000")

server.sendmail(sender, recipients, msg.as_string())
server.quit()
