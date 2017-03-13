#import
import nba_2_mail_functions as fn


def main() :
	yesterday = fn.setDate()
	NBAresults = fn.parseResults (yesterday)
	fn.sendMail(NBAresults)

#######-----------MAIN
main()
