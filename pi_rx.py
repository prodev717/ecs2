from machine import ADC, Pin
import time

# --- Configuration ---
SENSOR_PIN = 28          # ADC0 (GP28)
THRESHOLD = 60000        # adjust based on your LDR readings
INTERVAL = 0.03           # must match transmitter interval
adc = ADC(Pin(SENSOR_PIN))

previous_state = 0
detection_started = False
test_string = ""
decoded_text = ""

def delay(seconds):
    time.sleep(seconds)

def get_ldr_state(value):
    """Convert LDR reading to binary (1 if light detected)."""
    return 1 if value > THRESHOLD else 0

def convert_binary_to_ascii(bits):
    """Convert 8-bit binary string to character."""
    try:
        return chr(int(bits, 2))
    except:
        return '?'

def get_byte():
    global test_string
    delay(INTERVAL * 1.5)  # wait for stable start bit

    for i in range(8):
        value = adc.read_u16()
        bit = str(get_ldr_state(value))
        test_string += bit
        delay(INTERVAL)

    char = convert_binary_to_ascii(test_string)
    print(char, end='')  # live output to REPL
    test_string = ""

def main():
    global previous_state, detection_started

    print("Receiver ready... waiting for signal")

    while True:
        light_value = adc.read_u16()
        current_state = get_ldr_state(light_value)

        # Detect transition (light ON → OFF)
        if not current_state and previous_state:
            detection_started = True
            get_byte()
            detection_started = False

        previous_state = current_state
        delay(INTERVAL*0.1)  # sampling interval

main()
