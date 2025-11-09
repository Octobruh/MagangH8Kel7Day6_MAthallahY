# emulator_script.py (Corrected)
import serial
import time

PORT_B = 'COM8'
BAUD_RATE = 9600

try:
    with serial.Serial(PORT_B, BAUD_RATE, timeout=1) as ser:
        print(f"Emulator listening on {ser.name}...")
        
        object_count = 0 # Keep track of how many objects we've received
        
        while True:
            # Check if there's data waiting
            if ser.in_waiting > 0:
                
                # Read one full line, ending in '\n'
                line = ser.readline()
                line_str = line.decode('utf-8').strip()

                # If the line isn't empty
                if line_str:
                    
                    # Check if this is the "DONE" marker
                    if line_str == "DONE":
                        print("Emulator received DONE signal.")
                        print(f"Total objects processed: {object_count}")
                        
                        # Send our single acknowledgment
                        response_msg = f"OK, {object_count} PROCESSED\n"
                        ser.write(response_msg.encode('utf-8'))
                        
                        object_count = 0 # Reset for the next batch
                        
                    else:
                        # This is an object packet
                        object_count += 1
                        print(f"Emulator received object {object_count}: {line_str}")
                        
                        # --- On the ESP32, you would parse the data here ---
                        # parts = line_str.split(',')
                        # label = parts[0]
                        # x = float(parts[1])
                        # y = float(parts[2])
                        # ---------------------------------------------------

            time.sleep(0.01) # Prevent the loop from using 100% CPU

except serial.SerialException as e:
    print(f"Emulator error: {e}")
except KeyboardInterrupt:
    print("\nEmulator stopped.")