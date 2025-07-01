import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

deadlock_detected = threading.Event()

def thread_a():
    print('[Thread A] Starting...')
    print('[Thread A] Trying to acquire lock A...')
    lock_a.acquire()
    print('[Thread A] Acquired lock A.')
    time.sleep(2)

    print('[Thread A] Trying to acquire lock B...')
    acquired = lock_b.acquire(timeout=3)
    if not acquired:
        print('[Thread A] Timeout on lock B. Possible deadlock detected.')
        deadlock_detected.set()
        lock_a.release()
        print('[Thread A] Released lock A for recovery.')
        return

    print('[Thread A] Acquired lock B.')
    time.sleep(2)
    print('[Thread A] Releasing both locks.')
    lock_b.release()
    lock_a.release()

def thread_b():
    print('[Thread B] Starting...')
    print('[Thread B] Trying to acquire lock B...')
    lock_b.acquire()
    print('[Thread B] Acquired lock B.')
    time.sleep(5)

    print('[Thread B] Trying to acquire lock A...')
    acquired = lock_a.acquire(timeout=3)
    if not acquired:
        print('[Thread B] Timeout on lock A. Possible deadlock detected.')
        deadlock_detected.set()
        lock_b.release()
        print('[Thread B] Released lock B for recovery.')
        return

    print('[Thread B] Acquired lock A.')
    time.sleep(2)
    print('[Thread B] Releasing both locks.')
    lock_a.release()
    lock_b.release()

def monitor():
    time.sleep(6)
    if deadlock_detected.is_set():
        print('[Monitor] Deadlock detected and recovery attempted.')
    else:
        print('[Monitor] No deadlock. System completed smoothly.')

thread1 = threading.Thread(target=thread_a)
thread2 = threading.Thread(target=thread_b)
watchdog = threading.Thread(target=monitor)

thread1.start()
thread2.start()
watchdog.start()

thread1.join()
thread2.join()
watchdog.join()

print('\n Simulation finished.')