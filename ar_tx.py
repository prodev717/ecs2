from pyfirmata2 import Arduino
import time

# --- Configuration ---
PORT = 'COM3'   # change to your Arduino port (e.g. 'COM3' on Windows)
PIN = 7                 # digital pin where LED is connected
INTERVAL = 0.03          # 100ms per bit

# --- Setup board ---
board = Arduino(PORT)
led = board.digital[PIN]
time.sleep(2)  # wait for board to initialize
led.write(1)

def delay(seconds):
    time.sleep(seconds)

def convert_to_binary(char):
    """Convert character to 8-bit binary string."""
    return format(ord(char), '08b')

def send_bytes(MESSAGE):
    for char in MESSAGE:
        # small gap before sending each character
        led.write(0)
        delay(INTERVAL)

        bits = convert_to_binary(char)
        if char != "\n":
            print(f"Sending '{char}' -> {bits}")

        for bit in bits:
            if bit == '1':
                led.write(1)
            else:
                led.write(0)
            delay(INTERVAL)

        # end-of-char signal (short ON pulse)
        led.write(1)
        delay(INTERVAL)

    # brief pause before repeating message
    delay(1)

if __name__ == "__main__":
    print("Starting transmission...")
    while True:
        inp = input("message: ")
        if inp=="exit":
            exit()
        send_bytes(inp+"\n")
