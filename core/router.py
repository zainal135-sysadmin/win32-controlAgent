#core/router
routes = {}

def register(command: str):
    def decorator(func):
        routes[command] = func
        return func
    return decorator

def resolve(parsed: dict):
    if not parsed:
        return {
            "status": "error",
            "handler": None,
            "args": [],
            "error": "input kosong"
        }
    command = parsed.get("command")
    args = parsed.get("args", [])
    if not command:
        return {
            "status": "error",
            "handler": None,
            "args": args,
            "error": "bukan command"
        }
    handler = routes.get(command)
    if not handler:
        return {
            "status": "error",
            "handler": None,
            "args": args,
            "error": f"command {command} tidak dikenal"
        }
    else:
        return {
            "status": "ok",
            "handler": handler,
            "args": args,
            "error": None
        }