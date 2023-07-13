import serial
import time
import serial.tools.list_ports


# Function to detect the Arduino port
def detect_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description:
            return port.device
    return None


# Function to send the target and speed values over serial connection
def send_data(msg, ser):
    # Open the serial connection
    # ser = serial.Serial(port, 115200)

    # Construct the message string
    message = f"<{msg}>"
    print("Sending:", message)

    # Send the message over serial
    ser.write(message.encode())
    ser.reset_input_buffer()
    response = ser.readline().decode().strip()

    # response is space separated, in this format: m1 m2 m3 m4 iteration
    response = response.split(" ")
    m1 = response[0]
    m2 = response[1]
    m3 = response[2]
    m4 = response[3]
    iteraton = response[4]
    print(f"m1: {m1} m2: {m2} m3: {m3} m4: {m4} iteration: {iteraton}")

    # Close the serial connection
    # ser.close()


# Main function
def main():
    try:
        # Detect the Arduino port
        arduino_port = detect_arduino_port()
        if arduino_port is None:
            print("Error: Arduino port not found.")
            return

        ser = serial.Serial(arduino_port, 115200, timeout=1)

        while True:
            # Get input from the user
            msg = input("Enter the control signal [num][speed]: ")

            # Send the data
            send_data(msg, ser)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...")
        ser.close()


# Run the main function
if __name__ == "__main__":
    main()
