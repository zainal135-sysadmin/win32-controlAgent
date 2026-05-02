from services import workflow_serv as service

class ControlLogic:
    def __init__(self):
        self.uname = uname
    def stats_app_check(self):
        for proc in service.raw_stats_app_check():
            yield {
                "pid": proc.info["pid"],
                "name": proc.info["name"],
                "status": proc.info["status"],
                "exe": proc.info["exe"]
            }
            
