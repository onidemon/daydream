from excel_parser import Planner

p = Planner()
p.fetch_schedule()
p.schedule_all()
p.send_to_teams()
