import asyncio
from tasks.render_pdf import start_zmq_client


if __name__ == "__main__":
    print("starting worker")
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_zmq_client())
    except KeyboardInterrupt:
        print("exiting gracefully")
