#!/usr/bin/env python3
import minimalmodbus
import serial

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)

instrument.serial.baudrate = 115200         # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.2          # seconds

instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True

PV_VOLTAGE = 0x3100
PV_CURRENT = 0x3101
PV_POWERL = 0x3102
PV_POWERH = 0x3103
BAT_VOLTAGE = 0x331A
BAT_POWERL = 0x3106
BAT_POWERH = 0x3107
LOAD_VOLTAGE = 0x310C
LOAD_CURRENT = 0x310D
LOAD_POWERL = 0x310E
LOAD_POWERH = 0x310E
BAT_TEMP = 0x3110
EQUIPMENT_TEMP = 0x3111
BAT_SOC = 0x311A
BAT_RATED_VOLTAGE = 0x9067

# Print panel info
pv_voltage = instrument.read_register(PV_VOLTAGE, 2, 4, False)  # Registernumber, number of decimals
print("Panel voltage:\t" + str(pv_voltage) + "V")
pv_current = instrument.read_register(PV_CURRENT, 2, 4, False)  # Registernumber, number of decimals
print("Panel current:\t" + str(pv_current) + "A")

# Print battery info
bat_voltage = instrument.read_register(BAT_VOLTAGE, 2, 4, False)  # Registernumber, number of decimals
print("Batt. voltage:\t" + str(bat_voltage) + "V")
temperature = instrument.read_register(BAT_TEMP, 2, 4, False)  # Registernumber, number of decimals
print("Batt. temp:\t" + str(temperature) + "C")

# Set battery type, 1 = Sealed
battery_type = instrument.read_register(0x9000, 0, 3, False)  # Registernumber, number of decimals
type_string = ""
if battery_type == 1:
    type_string = "Sealed"
elif battery_type == 2:
    type_string = "Gel"
elif battery_type == 3:
    type_string = "Flooded"
elif battery_type == 4:
    type_string = "User defined"
print("Battery type:\t" + type_string)

# Set capacity to 105 Ah
instrument.write_register(0x9001, 105, 0, functioncode=0x10, signed=False)
battery_capacity = instrument.read_register(0x9001, 0, 3, False)  # Registernumber, number of decimals
print("Battery capac.:\t" + str(battery_capacity) + "Ah")

# Set battery voltage, 0 = auto detect, 1 = 12 V, 2 = 24V
instrument.write_register(BAT_RATED_VOLTAGE, 1, 0, functioncode=0x10, signed=False)
battery_rated_volt = instrument.read_register(BAT_RATED_VOLTAGE, 0, 3, False)  # Registernumber, number of decimals
volt_string = ""
if battery_rated_volt == 0:
    volt_string = "autodetect"
else:
    volt_string = str(12 * battery_rated_volt)

print("System voltage:\t" + volt_string + "V")

