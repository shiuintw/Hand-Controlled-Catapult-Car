import threading
import time
import web_server
import sg90
import wheels


def clean_up():
    sg90.clean_up()
    wheels.clean_up()


# ======================================================================================
#  Program Entry
# ======================================================================================
if __name__ == '__main__':
    threading.Thread(target=web_server.web_boot, daemon=True).start()

    try:
        while True:
            r = web_server.get_latest()
            if r['hands_detected']:
                g = r['hands'][0]['gesture']
                if g == 'open':
                    wheels.forward()
                elif g == 'fist':
                    wheels.stop()
                elif g == 'point':
                    pass
                    # sg90.fire()
            else:
                wheels.stop()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        clean_up()