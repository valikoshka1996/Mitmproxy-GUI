import tkinter as tk
from tkinter import messagebox
import socket
import subprocess
import os
import shutil
import threading
import signal
import time
import sys

proxy_process = None  # глобальна змінна для зберігання процесу

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def copy_certs():
    cert_dir = os.path.expanduser("~/.mitmproxy")
    android_cert = os.path.join(cert_dir, "mitmproxy-ca-cert.cer")
    ios_cert = os.path.join(cert_dir, "mitmproxy-ca-cert.pem")

    targets = {
        "certs_android": ("Android", [android_cert]),
        "certs_ios": ("iOS", [ios_cert]),
        "certs_general": ("General", [cert_dir])  # копіюємо всю папку
    }

    for folder, (label, paths) in targets.items():
        dst = os.path.join(os.getcwd(), folder)
        try:
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.makedirs(dst)

            for path in paths:
                if os.path.isdir(path):
                    shutil.copytree(path, os.path.join(dst, os.path.basename(path)))
                else:
                    shutil.copy2(path, dst)

            os.startfile(dst)
        except Exception as e:
            messagebox.showwarning("Увага", f"[{label}] Не вдалося скопіювати сертифікати:\n{e}")

def resource_path(relative_path):
    """ Отримати абсолютний шлях до ресурсу, працює і в .exe, і при запуску з .py """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def start_proxy():
    global proxy_process

    port = port_entry.get()
    domains = domain_entry.get("1.0", "end").strip()

    if not port.isdigit():
        messagebox.showerror("Помилка", "Порт має бути числом.")
        return

    copy_certs()

    # Використовуємо правильні шляхи
    mitmdump_exec = resource_path("mitmdump.exe")
    logger_path = resource_path("logger.py")
    filter_script_path = os.path.join(os.getcwd(), "filter_domains.py")  # генеруємо в поточній робочій директорії

    command = [
        mitmdump_exec,
        "-p", port,
        "--set", "confdir=" + os.path.expanduser("~/.mitmproxy"),
        "-s", logger_path
    ]

    # Генеруємо filter_domains.py у поточну директорію
    if domains:
        domain_list = [d.strip() for d in domains.split("\n") if d.strip()]
        with open(filter_script_path, "w") as f:
            f.write("from mitmproxy import http\n")
            f.write("def request(flow: http.HTTPFlow):\n")
            f.write("    allowed = [\n")
            for d in domain_list:
                f.write(f"        '{d}',\n")
            f.write("    ]\n")
            f.write("    if not any(domain in flow.request.pretty_host for domain in allowed):\n")
            f.write("        flow.response = http.Response.make(403, b'Blocked by filter', {})\n")
        command += ["-s", filter_script_path]

    proxy_process = subprocess.Popen(command)

def stop_proxy():
    global proxy_process
    if proxy_process and proxy_process.poll() is None:
        proxy_process.terminate()
        try:
            proxy_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proxy_process.kill()
        proxy_process = None
        messagebox.showinfo("Зупинено", "Проксі сервер зупинено.")
    else:
        messagebox.showinfo("Інформація", "Проксі сервер не запущений.")

def run_start_thread():
    threading.Thread(target=start_proxy).start()

# === GUI ===
root = tk.Tk()
root.title("Proxy Server GUI")
root.geometry("500x500")

tk.Label(root, text="Локальна IP-адреса:").pack()
ip_label = tk.Label(root, text=get_local_ip(), font=("Courier", 12))
ip_label.pack(pady=5)

tk.Label(root, text="Порт для проксі:").pack()
port_entry = tk.Entry(root)
port_entry.insert(0, "8080")
port_entry.pack(pady=5)

tk.Label(root, text="Дозволені домени (по одному на рядок, залиш порожнім для всіх):").pack()
domain_entry = tk.Text(root, height=8)
domain_entry.pack(pady=5)

start_button = tk.Button(root, text="▶️ Запустити Проксі", command=run_start_thread)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="⏹ Зупинити Проксі", command=stop_proxy)
stop_button.pack(pady=5)

tk.Label(root, text="⚠️ Сертифікати будуть скопійовані у папки: Android, iOS, General").pack()

root.mainloop()
