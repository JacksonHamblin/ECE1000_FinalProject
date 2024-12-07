from machine import ADC, Pin
import utime

# What pins are hooked up to the sensor and pump?
soil_probe = ADC(Pin(27))  # Soil moisture sensor connected to GPIO 26
pump_pin = Pin(13, Pin.OUT)  # Pump connected to GPIO 15 (Make sure to use proper power control)

# Before we can show the moisture as a percentage, need to first get the minimum moisture value (when the probe is not in water) and the maximum moisture value (when the probe is in water)
max_moisture = 27574
min_moisture = 57100

# This function will fit the moisture level of the sensor to a line equation from ~0% to ~100% using the min and max moisture value measured with the sensor
def get_moisture_percentage(moisture_level):
    point_1_x = min_moisture
    point_2_x = max_moisture
    point_1_y = 0
    point_2_y = 100
    m = ((point_2_y - point_1_y) / (point_2_x - point_1_x))
    return int((m*moisture_level) - (m*min_moisture) + point_1_y)

# Function to check moisture level and control pump
def check_soil_and_control_pump():
    moisture_level = soil_probe.read_u16()  # Read the moisture level from the sensor
   
    # Convert the moisture level to a percentage
    moisture_percentage = get_moisture_percentage(moisture_level)
   
    # Print the moisture percentage for monitoring
    print(f"Moisture Level: {moisture_percentage}%")
   
   
    # If the moisture level is below 20%, turn the pump on
    if moisture_percentage < 20:
        print("Soil is dry. Turning pump ON.")
        pump_pin.on()  # Turn pump ON (set GPIO pin HIGH)
    else:
        print("Soil is sufficiently moist. Turning pump OFF.")
        pump_pin.off()  # Turn pump OFF (set GPIO pin LOW)
   
    utime.sleep(0.8)  # Sleep for a short time before taking another reading

# Main loop
while True:
    check_soil_and_control_pump()
    utime.sleep(1)
