from services import workflow_serv as service

def stats_app_check():
    for proc in service.raw_stats_app_check():
        yield {
            "pid": proc.info["pid"],
            "name": proc.info["name"],
            "status": proc.info["status"],
            "exe": proc.info["exe"]
        }
        