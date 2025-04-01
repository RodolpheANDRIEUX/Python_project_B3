import threading
from reader import start_reader
from web.app import start_web_server
import web.scrap

if __name__ == "__main__":
    web.scrap.fetch_fide_rating()
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()

    start_reader()
