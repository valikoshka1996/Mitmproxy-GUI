# 🔍 MitmProxy GUI Tool for Domain Filtering and Logging

This project provides a graphical interface for running a local MITM (man-in-the-middle) proxy using [mitmproxy](https://mitmproxy.org/). It allows easy certificate distribution, optional domain filtering, and detailed logging of HTTP requests and responses to a file.

## 🧰 Features

- ✅ GUI-based proxy controller using `tkinter`
- ✅ Filter traffic by allowed domains
- ✅ Automatically logs HTTP requests and responses to `proxy_log.txt`
- ✅ Automatically copies mitmproxy certificates for Android, iOS, and general use
- ✅ Generates a `filter_domains.py` script dynamically
- ✅ Built-in IP address display and port selector

## 📁 Project Structure

project-root/
│
├── Mani.py              # Main GUI and proxy controller
├── logger.py            # MITM logging script
├── mitmdump.exe         # mitmproxy executable (required)
└── \~/.mitmproxy/        # mitmproxy certificate directory (auto-created)



## ⚙️ Requirements

- Python 3.x
- `mitmproxy` installed
- `mitmdump.exe` available in the working directory
- Windows OS (due to use of `os.startfile()`)

Install dependencies with:

```bash
pip install mitmproxy
````

## 🚀 Usage

1. **Run the application**

```bash
python Mani.py
```

2. **Configure the Proxy**

   * Choose a **port** (e.g., `8080`)
   * Optionally, enter **allowed domains**, one per line. Leave empty to allow all traffic.

3. **Start the Proxy**

   * Click `▶️ Start Proxy` to launch mitmproxy.
   * The GUI copies certificates to `certs_android/`, `certs_ios/`, and `certs_general/`.

4. **Stop the Proxy**

   * Click `⏹ Stop Proxy` to safely terminate mitmproxy.

## 🧪 Log Output

Logs are saved in `proxy_log.txt` and include:

* Request and response timestamp
* Method, URL, headers, and body (truncated to 1000 chars)

## 🔐 Certificates

Certificates are copied from `~/.mitmproxy` into three folders:

* `certs_android/` – contains `mitmproxy-ca-cert.cer`
* `certs_ios/` – contains `mitmproxy-ca-cert.pem`
* `certs_general/` – contains the entire `~/.mitmproxy` directory

These can be used to install the CA certificate on test devices.

## 📜 File Descriptions

### `Mani.py`

* Creates the GUI interface with input for port and domain filter.
* Handles starting and stopping the mitmproxy subprocess.
* Copies certificates to platform-specific folders.
* Dynamically generates a `filter_domains.py` file if domain filters are provided.

### `logger.py`

* Used by mitmdump to log all HTTP requests and responses.
* Appends formatted logs to `proxy_log.txt`.

### `filter_domains.py` (Generated Automatically)

* Filters all requests to only allow domains specified in the GUI.
* If a request’s host does not match allowed domains, a `403 Blocked by filter` response is returned.

## 📝 Example Log Output

```
[ЗАПИТ] 2025-05-17 12:34:56
Метод:      GET
URL:        http://example.com/api/data
Заголовки:
  Host: example.com
  User-Agent: Mozilla/5.0
Тіло:
[порожнє]
--------------------------------------------------------------------------------
[ВІДПОВІДЬ] 2025-05-17 12:34:57
Статус:     200
Заголовки:
  Content-Type: application/json
Тіло:
{"data": "sample"}
--------------------------------------------------------------------------------
```

## ⚠️ Notes

* This project is designed for **educational and testing purposes** only.
* Do not intercept or analyze traffic without proper legal authorization.
* Certificates must be installed on the target device for HTTPS interception.

## 📌 To-Do / Future Ideas

* Add cross-platform support (Linux/macOS)
* Improve GUI with status indicators
* Add HTTPS certificate installation helper

## 🧑‍💻 Author

Developed by \[Your Name Here]

---

MIT License – free to use and modify
