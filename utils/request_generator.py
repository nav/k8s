#!/usr/bin/env python3
import argparse
import asyncio
import random
import sys
import urllib.request


# Source: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=""):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "#" * filled_len + "-" * (bar_len - filled_len)

    sys.stdout.write(f"{status} [{bar}] {percents}%\r")
    sys.stdout.flush()


async def send_requests(url: str, count: int = 100, lamda: float = 5.0) -> None:
    """Send HTTP get requests to a URL with a delay following Poisson distribution.

    Args:
        url: The URL to send requests.
        count: Total number of requests to send. Defaults to 100.
        lamda: Value to calculate exponential distribution of delay. Spelled
               incorrectly to not conflict with `lambda` keyword.

    Returns:
        `None` value when it finishes.
    """
    successful = failed = 0
    current = 0
    while count - current > 0:
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request)
        except Exception:
            failed += 1
        else:
            successful += 1

        await asyncio.sleep(random.expovariate(lamda))
        progress(current, count, status="Sending requests...")
        current += 1

    sys.stdout.flush()
    sys.stdout.write(f"Finished: Successful={successful} Failed={failed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate requests following a Poisson distribution"
    )
    parser.add_argument("url", help="url to send requests")
    parser.add_argument("count", type=int, help="number of requests to send")
    parser.add_argument(
        "--lambda",
        dest="lamda",
        type=float,
        default=5,
        help="average of requests per second",
    )

    args = parser.parse_args()

    try:
        asyncio.run(send_requests(args.url, args.count, args.lamda))
    except KeyboardInterrupt:
        print("Stopping...")
        sys.exit()
