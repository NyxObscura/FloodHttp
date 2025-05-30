# Advanced Asynchronous HTTP Load Tester

An aggressive, multi-process, and asynchronous Python-based load testing script designed for high-performance HTTP stress testing. This tool leverages `asyncio`, `httpx`, and `multiprocessing` for generating substantial load on web servers. It optionally uses `uvloop` for enhanced asyncio performance if available.

**Contributor:** Gemini

## Disclaimer

**💀 CRITICAL WARNING: THIS SCRIPT IS EXTREMELY POWERFUL & POTENTIALLY HARMFUL 💀**

This tool is designed for legitimate load testing purposes on infrastructure you own or have explicit permission to test. Unauthorized use against systems you do not own can lead to service disruption and may have legal consequences. **Use responsibly and ethically.**

**Ensure you have increased your system's `ulimit -n` (file descriptor limit) before running high-concurrency tests to prevent errors.**

## Features

* **High Concurrency:** Utilizes `multiprocessing` to leverage multiple CPU cores and `asyncio` for concurrent I/O-bound tasks within each process.
* **HTTP/2 Support:** Leverages HTTP/2 for more efficient connections when supported by the target server.
* **Customizable:**
    * Target URL
    * Test duration
    * Number of processes
    * Number of asynchronous threads (coroutines) per process
    * Concurrency level per process
    * Custom User-Agent lists
* **Realistic Headers:** Sends a variety of randomized, yet common, HTTP headers, including `User-Agent`, `Referer`, `Accept` types, and `X-Forwarded-For`.
* **Shared Request Counter:** Accurately tracks the total number of successful requests across all processes.
* **Performance Monitoring:** Displays real-time Requests Per Second (RPS) and total requests.
* **Optional `uvloop`:** Automatically uses `uvloop` for faster asyncio event loop performance if installed.
* **Robust Error Handling:** Includes retries for network-related issues and graceful shutdown.

## Prerequisites

* Python 3.7+
* Required Python libraries (install via pip):
    * `httpx`
    * `uvloop` (optional, but recommended for performance on Linux/macOS)

```bash
pip install httpx uvloop
```
 * A text file containing User-Agent strings (e.g., ua.txt). If not provided or found, a default list will be used. Each User-Agent should be on a new line.
Usage
```bash
python your_script_name.py <URL> [OPTIONS]
```
Example:
```bash
python3 flood.py https://target.example.com -d 300 -p 4 -t 2000 -c 1000 -ua ./ua.txt
```
Command-Line Arguments:
 * url: (Required) The target URL to test.
 * -d, --duration: Test duration in seconds.
   * Default: 120
 * -p, --processes: Number of processes to spawn.
   * Default: Number of CPU cores.
 * -t, --threads: Number of asynchronous coroutines (threads) per process.
   * Default: 1000
 * -c, --concurrency: Number of concurrent requests per process. This value should not exceed the number of threads.
   * Default: 500
 * -ua, --user_agents: Path to the file containing User-Agent strings.
   * Default: ./ua.txt
  
  
How It Works
 * Initialization: The script parses command-line arguments and loads User-Agent strings.
 * Multiprocessing: It spawns a specified number of worker processes.
 * Asynchronous Workers: Each process runs an asyncio event loop, managing multiple asynchronous "attack workers" (coroutines).
 * HTTP Requests:
   * Each attack worker continuously sends HTTP GET requests to the target URL until the test duration expires.
   * Requests are made using httpx.AsyncClient with HTTP/2 enabled and customized connection limits.
   * Randomized headers are generated for each request to simulate diverse clients.
 * Concurrency Control: An asyncio.Semaphore within each process limits the number of concurrent active requests to the specified concurrency level.
 * Status & Reporting:
   * A shared counter (multiprocessing.Value) tracks the total number of successful requests across all processes.
   * The main process displays the elapsed time, total successful requests, and current RPS.
   * Upon completion or interruption (Ctrl+C), it provides a summary of the test.
  
 
Author & Contact
 * GitHub: [NyxObscura](github.com/NyxObscura)
 * Website: [www.obscuraworks.com](https://www.obscuraworks.com)
 * WhatsApp: [+62 851-8334-3636](wa.me/6285183343636)
[License](LICENSE)
This project is intended for educational and ethical testing purposes. Please ensure you have proper authorization before using it. The author or contributors are not responsible for any misuse or damage caused by this script.

