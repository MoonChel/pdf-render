import asyncio
from tasks.render_pdf import start_zmq_client


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_zmq_client())
