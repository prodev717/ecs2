from machine import Pin
import time
import sys

# --- Configuration ---
PIN = 15               # GPIO pin where LED is connected
INTERVAL = 0.03        # must match receiver's INTERVAL
led = Pin(PIN, Pin.OUT)

# LED ON by default (idle = HIGH)
led.value(1)

def delay(seconds):
    time.sleep(seconds)

def convert_to_binary(char):
    """Convert character to 8-bit binary string."""
    return "{:08b}".format(ord(char))

def send_bytes(message):
    for char in message:
        # small gap before sending each character (LED off)
        led.value(0)
        delay(INTERVAL)

        bits = convert_to_binary(char)
        if char != "\n":
            print(f"Sending '{char}' -> {bits}")

        # transmit each bit (light ON = 1, OFF = 0)
        for bit in bits:
            led.value(1 if bit == '1' else 0)
            delay(INTERVAL)

        # end-of-char signal (short ON pulse)
        led.value(1)
        delay(INTERVAL)

    # brief pause before next message
    delay(1)

def main():
    print("Starting transmission...")
    while True:
        # Read message line from serial input
        msg = sys.stdin.readline().strip()
        if not msg:
            continue

        if msg.lower() == "exit":
            print("Transmission ended.")
            break

        send_bytes(msg + "\n")

main()

