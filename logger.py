from mitmproxy import http
from datetime import datetime

def log_line(title, content=""):
    with open("proxy_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{title}\n")
        if content:
            f.write(f"{content}\n")
        f.write("-" * 80 + "\n")

def request(flow: http.HTTPFlow):
    req = flow.request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line(f"[ЗАПИТ] {timestamp}")
    log_line("Метод:      " + req.method)
    log_line("URL:        " + req.pretty_url)
    log_line("Заголовки:\n" + "\n".join([f"  {k}: {v}" for k, v in req.headers.items()]))
    log_line("Тіло:\n" + (req.text[:1000] if req.text else "[порожнє]"))

def response(flow: http.HTTPFlow):
    res = flow.response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line(f"[ВІДПОВІДЬ] {timestamp}")
    log_line("Статус:     " + str(res.status_code))
    log_line("Заголовки:\n" + "\n".join([f"  {k}: {v}" for k, v in res.headers.items()]))
    log_line("Тіло:\n" + (res.text[:1000] if res.text else "[порожнє]"))
