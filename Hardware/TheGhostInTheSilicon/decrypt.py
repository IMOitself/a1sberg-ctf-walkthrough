import pandas as pd

def decode_pwm_led(file_path):
    print("Loading data...")
    df = pd.read_csv(file_path)
    times = df['Time'].values
    states = df['GPIO_LED'].values
    
    # 1. Find all transitions (when the signal changes from 0 to 1 or 1 to 0)
    transitions = []
    for i in range(1, len(states)):
        if states[i] != states[i-1]:
            transitions.append((times[i], states[i]))
            
    print(f"Found {len(transitions)} state transitions.")
    
    bits = []
    
    # 2. Measure the width of every HIGH pulse
    for i in range(len(transitions) - 1):
        time, state = transitions[i]
        next_time, _ = transitions[i+1]
        
        # We only care about how long the line was HIGH (1)
        if state == 1:
            pulse_width = next_time - time
            
            # Short pulse (~0.00025s) -> '0'
            if 0.00015 < pulse_width < 0.00035:
                bits.append(0)
            # Long pulse (~0.00075s) -> '1'
            elif 0.00065 < pulse_width < 0.00085:
                bits.append(1)

    print(f"Recovered {len(bits)} bits.")

    # 3. Chunk the bits into bytes (8 bits per character)
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        
        if len(byte_bits) == 8:
            # Try MSB (Most Significant Bit) first
            byte_str = "".join(map(str, byte_bits))
            byte_val = int(byte_str, 2)
            chars.append(chr(byte_val))
            
    flag = "".join(chars)
    return flag

# Run the decoder
flag = decode_pwm_led('led_capture.csv')
print("\n--- DECODED OUTPUT ---")
print(flag)