import threading

def dead_loop():
    while True:
        pass

for i in range(0):
    t = threading.Thread(target=dead_loop)
    t.start()

dead_loop()