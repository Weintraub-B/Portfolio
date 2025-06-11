import sounddevice as sd

def list_input_devices():
    """
    Lists all available input audio devices.
    """
    devices = sd.query_devices()
    input_devices = [(i, dev['name']) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]
    for index, name in input_devices:
        print(f"{index}: {name}")
    return input_devices

def select_input_device():
    """
    Prompts the user to select an input device from the list.
    """
    input_devices = list_input_devices()
    while True:
        try:
            choice = int(input("Enter the number of the input device to use: "))
            if 0 <= choice < len(sd.query_devices()):
                return choice
            else:
                print("Invalid choice. Please enter a valid device number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_wasapi_loopback_device():
    print("Available WASAPI Loopback Devices:\n")
    loopbacks = []
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()

    for i, dev in enumerate(devices):
        hostapi_name = hostapis[dev['hostapi']]['name']
        if 'WASAPI' in hostapi_name and dev['max_input_channels'] > 0:
            loopbacks.append((i, dev['name']))

    if not loopbacks:
        print("No WASAPI loopback devices found. Please ensure your system supports WASAPI and that loopback devices are enabled.")
        return None

    for idx, (dev_index, name) in enumerate(loopbacks):
        print(f"{idx}: {name} (index {dev_index})")

    while True:
        try:
            choice = int(input("Enter the number of the loopback device to use: "))
            if 0 <= choice < len(loopbacks):
                return loopbacks[choice][0]
            else:
                print("Invalid selection. Please enter a valid number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")