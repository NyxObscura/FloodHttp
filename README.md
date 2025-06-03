---

<div align="center">
  <img src="https://raw.githubusercontent.com/NyxObscura/FloodHttp/main/x.png" alt="FloodHTTP" width="1080"/>
  <h1>FloodHTTP</h1>
  <h3>⚡ Advanced Asynchronous HTTP Load Tester ⚡</h3>
  
  <p>An aggressive, high-concurrency, and multi-process Python-based HTTP stress testing tool.</p>

  <p>
    <a href="https://github.com/NyxObscura/FloodHttp"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/NyxObscura/FloodHttp?style=social"></a>
    <a href="https://github.com/NyxObscura/FloodHttp"><img alt="GitHub forks" src="https://img.shields.io/github/forks/NyxObscura/FloodHttp?style=social"></a>
    <a href="https://github.com/NyxObscura/FloodHttp/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/NyxObscura/FloodHttp"></a>
    <a href="https://www.python.org/"><img alt="Python Version" src="https://img.shields.io/badge/Python-3.7%2B-blue.svg"></a>
  </p>
</div>

---

## ⚠️ Disclaimer

> 💀 **WARNING: THIS TOOL IS EXTREMELY POWERFUL AND CAN CAUSE SERVICE DISRUPTION**  
> Use only for ethical and authorized testing on systems you own or have explicit permission to test. Unauthorized usage may lead to legal consequences.  
> Ensure your `ulimit -n` is sufficiently high before performing high-concurrency tests.

---

## ✨ Features

- ⚙️ **High Concurrency:** Multiprocessing + AsyncIO for massive parallelism  
- 📡 **HTTP/2 Ready:** Uses `httpx` with HTTP/2 support  
- 🔧 **Highly Customizable:** Duration, thread count, process count, UA list, concurrency  
- 🎭 **Realistic Headers:** Rotating `User-Agent`, `Referer`, `X-Forwarded-For`, and more  
- 📊 **Live Metrics:** Real-time request counter and RPS display  
- ⚡ **Optional `uvloop`:** Enhanced event loop for Linux/macOS  
- 🛠️ **Robust Error Handling:** Retries, graceful shutdown, and connection tuning  

---

## 🧪 Usage

### 🔧 Requirements

- Python 3.7+
- Install dependencies:
```bash
pip install httpx uvloop
```
A text file containing User-Agent strings (ua.txt) is optional. If not found, a default set is used.


---

## ▶️ Example Usage
```bash
python3 flood.py https://target.example.com -d 300 -p 4 -t 2000 -c 1000 -ua ./ua.txt
```
## ⚙️ Command Line Options

Argument	Description	Default

url	Required – Target URL	—
-d, --duration	Test duration (in seconds)	120
-p, --processes	Number of CPU processes	CPU cores
-t, --threads	Async coroutines per process	1000
-c, --concurrency	Concurrent requests per process (≤ threads)	500
-ua, --user_agents	Path to UA list file (ua.txt)	./ua.txt



---

## 🔍 How It Works

> 📦 Initialization

> Parse CLI arguments

> Load User-Agent strings from file or use fallback list


## ⚙️ Multiprocessing & AsyncIO

Spawns multiple processes

Each process runs its own event loop with async workers


## 🌐 HTTP Requesting

Uses httpx.AsyncClient for non-blocking requests

HTTP/2 enabled when available

Randomized headers per request


## 📈 Concurrency Control

asyncio.Semaphore limits active tasks per process


## 📊 Status Reporting

Shared counter via multiprocessing.Value

Main process prints:
Elapsed time:
Total successful requests:
Requests per second (RPS):


---



👤 Author: [Obscuraworks, Inc.](www.obscuraworks.com) 

💻 GitHub: [@NyxObscura](github.com/NyxObscura)

🌐 Website: [www.obscuraworks.com](www.obscuraworks.com) 

📱 WhatsApp: [+62 851-8334-3636](wa.me/6285183343636) 



---

📜 License

This project is licensed under the terms of the [MIT License.](LICENSE)

## > ⚠️ This project is strictly for educational and ethical purposes only. The author is not responsible for misuse.

---
