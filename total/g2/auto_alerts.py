from teams_bot import G2SmartBot
import schedule
import time
s = G2SmartBot()

def job():
    G2SmartBot.s.location = "TE61"
    G2SmartBot.s.parse_url()
    time.sleep(5)
    G2SmartBot.s.send_to_teams()
    G2SmartBot.s.location = "HPC France"
    G2SmartBot.s.parse_url()
    time.sleep(5)
    G2SmartBot.s.send_to_teams()

 
schedule.every(1).hour.do(job)



while True:
    schedule.run_pending()
    time.sleep(1)
