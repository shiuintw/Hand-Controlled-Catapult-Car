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
            steering = web_server.get_gripping()
            lever = web_server.get_lever()

            if steering or lever:
                # Driving mode
                angle = web_server.get_steer() if steering else 0
                speed = web_server.get_speed() if lever else 0

                if abs(speed) < 10:
                    wheels.stop()
                elif speed > 0:
                    wheels.steer(angle, base_speed=speed)
                else:
                    # Backward with steering
                    wheels.steer(angle, base_speed=speed)

                # Fire
                r = web_server.get_latest()
                if r['hands_detected'] and  (r['hands'][0]['gesture'] == 'point' or r['hands'][1]['gesture'] == 'point'):
                    sg90.fire()

            elif False: # disable
                # No wheel or lever → gesture mode
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
                else:
                    wheels.stop()

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        clean_up()