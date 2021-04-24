#!/usr/bin/env python3
import minimalmodbus
import serial
import struct

#Support functions

def convertToFloat(input_int):
	#read_long returns a 32-bit int, convert to float...
	packed_v = struct.pack('>l', input_int)
	output_float =  struct.unpack('>f', packed_v)[0]
	return output_float


# Set to true to edit values
WRITE = True

instrument = minimalmodbus.Instrument(
    "/dev/ttyXRUSB0", 1
)  # port name, slave address (in decimal)

instrument.serial.baudrate = 115200  # Baud
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.2  # seconds

instrument.mode = minimalmodbus.MODE_RTU  # rtu or ascii mode
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

BAT_VOLTAGE_MAX_DAY = 0x3302# 00: 00 Refresh every day V 100
BAT_VOLTAGE_MIN_DAY = 0x3303# 00: 00 Refresh every day V 100
CONS_ENERGY_TODAY_L = 0x3304# 00: 00 Clear every day KWH 100
CONS_ENERGY_TODAY_H = 0x3305# 100
CONS_ENERGY_MONTH_L = 0x3306# 00: 00 Clear on the first day of month 100
CONS_ENERGY_MONTH_H = 0x3307# KWH 100
CONS_ENERGY_YEAR_L = 0x3308# 00: 00 Clear on 1, Jan. 100
CONS_ENERGY_YEAR_H = 0x3309# 100
CONS_ENERGY_TOTAL_L = 0x330A# 100
CONS_ENERGY_TOTAL_H = 0x330B# KWH 100
GEN_ENERGY_TODAY_L = 0x330C# 00: 00 Clear every day. 100
GEN_ENERGY_TODAY_H = 0x330D# 100
GEN_ENERGY_MONTH_L = 0x330E# 00: 00 Clear on the first day of month. 100
GEN_ENERGY_MONTH_H = 0x330F# KWH 100
GEN_ENERGY_YEAR_L  = 0x3310# 00: 00 Clear on 1, Jan. 100
GEN_ENERGY_YEAR_H  = 0x3311# KWH 100
GEN_ENERGY_TOTAL_L  = 0x3312# KWH 100
GEN_ENERGY_TOTAL_H  = 0x3313# 100


# Print panel info
pv_voltage = instrument.read_register(
    PV_VOLTAGE, 2, 4, False
)  # Registernumber, number of decimals
print("Panel voltage:\t" + str(pv_voltage) + "V")
pv_current = instrument.read_register(
    PV_CURRENT, 2, 4, False
)  # Registernumber, number of decimals
print("Panel current:\t" + str(pv_current) + "A")

# Print battery info
bat_voltage = instrument.read_register(
    BAT_VOLTAGE, 2, 4, False
)  # Registernumber, number of decimals
print("Batt. voltage:\t" + str(bat_voltage) + "V")
temperature = instrument.read_register(
    BAT_TEMP, 2, 4, False
)  # Registernumber, number of decimals
print("Batt. temp:\t" + str(temperature) + "C")

gen_energy_day=instrument.read_long(
GEN_ENERGY_TODAY_L, 4, False, 0)  # Registernumber, number of decimals
f = convertToFloat(gen_energy_day)
print("Energy today:\t" + str(f) + str("kWh"))

gen_energy_month=instrument.read_long(
GEN_ENERGY_MONTH_L, 4, False, 0)  # Registernumber, number of decimals
f = convertToFloat(gen_energy_month)
print("Energy month:\t" + str(f) + str("kWh"))

gen_energy_year=instrument.read_long(
GEN_ENERGY_YEAR_L, 4, False, 0)  # Registernumber, number of decimals
f = convertToFloat(gen_energy_year)
print("Energy year:\t" + str(f) + str("kWh"))


if WRITE:
    # Set battery type, 1 = Sealed
    sealed = 1
    instrument.write_register(0x9000, 1, 0, functioncode=0x10, signed=False)
battery_type = instrument.read_register(
    0x9000, 0, 3, False
)  # Registernumber, number of decimals
type_string = ""
if battery_type == 1:
    type_string = "Sealed"
elif battery_type == 2:
    type_string = "Gel"
elif battery_type == 3:
    type_string = "Flooded"
elif battery_type == 0:
    type_string = "User defined"
print("Battery type:\t" + type_string)

if WRITE:
    # Set capacity
    capacity = 75
    instrument.write_register(0x9001, capacity, 0, functioncode=0x10, signed=False)
battery_capacity = instrument.read_register(
    0x9001, 0, 3, False
)  # Registernumber, number of decimals
print("Battery capac.:\t" + str(battery_capacity) + "Ah")

if WRITE:
    # Set battery voltage, 0 = auto detect, 1 = 12 V, 2 = 24V
    v_auto = 0
    v_12 = 1
    v_24 = 2
    instrument.write_register(BAT_RATED_VOLTAGE, v_12, 0, functioncode=0x10, signed=False)
battery_rated_volt = instrument.read_register(
    BAT_RATED_VOLTAGE, 0, 3, False
)  # Registernumber, number of decimals
volt_string = ""
if battery_rated_volt == 0:
    volt_string = "autodetect"
else:
    volt_string = str(12 * battery_rated_volt)

print("System voltage:\t" + volt_string + "V")


print("Voltage configuration:")
val = instrument.read_register(0x900E, 2, 3, False)
print(val)

