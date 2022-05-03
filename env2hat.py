import time
from array import array
from machine import I2C
from bmm150_defs import CHIP_ID, CHIP_ID_ADDR, DATA_RATE_10HZ, DATA_RATE_20HZ, DATA_RHALL, DATA_X, DATA_X_LSB, DATA_Y, DATA_Z, DIG_X1, DIG_Z2_LSB, DIG_Z4_LSB, ENHANCED_REPXY, ENHANCED_REPZ, FORCED_MODE, HIGHACCURACY_REPXY, HIGHACCURACY_REPZ, I2C_Address, LOWPOWER_REPXY, LOWPOWER_REPZ, NORMAL_MODE, ODR, OP_MODE, OP_MODE_ADDR, POWER_CNTRL_DISABLE, POWER_CNTRL_ENABLE, POWER_CONTROL_ADDR, PRESETMODE_ENHANCED, PRESETMODE_HIGHACCURACY, PRESETMODE_LOWPOWER, PRESETMODE_REGULAR, PWR_CNTRL, REGULAR_REPXY, REGULAR_REPZ, REP_XY_ADDR, REP_Z_ADDR, SLEEP_MODE, START_UP_TIME, SUSPEND_MODE, XYZR_DATA_LEN, data_rate, dig_x1, dig_x2, dig_xy1, dig_xy2, dig_xyz1, dig_y1, dig_y2, dig_z1, dig_z2, dig_z3, dig_z4, xy_rep, z_rep

def set_bits_pos_0(reg_data, bitname, data):
	return (reg_data & bitname[0]) | (data & bitname[0])


def set_bits(reg_data, bitname, data):
	return (reg_data & bitname[0]) | ((data << bitname[1]) & bitname[0])


def get_bits(reg_data, bitname):
	return (reg_data & bitname[0]) >> bitname[1]


def print_devices():
	i2c = I2C(freq=400000, sda=0, scl=26) # scan hat I2C devices
	devices = i2c.scan()

	if len(devices) == 0:
		print("no i2c devs found")
	else:
		print("i2c devs found: " + str(len(devices)))

	for device in devices:
		print(str(hex(device)))



class BMM150:
	def __init__(self, i2c, calibrate_ms=10):
		self.trim     = [0]*11
		self.settings = [0]*7
		self.reg_data = bytearray(1)

		self.mag_data_raw = array('h', [0]*4)
		self.mag_data     = array('h', [0]*3)
		self.mag_offsets  = array('h', [0]*3)

		self.calibrated = False


		self.i2c = i2c
		self.set_op_mode(SLEEP_MODE)
		time.sleep_ms(START_UP_TIME)

		self.i2c_read(CHIP_ID_ADDR, self.reg_data)
		if self.reg_data[0] != CHIP_ID:
			raise ValueError("Got chip ID %s but expected %s" % (self.reg_data[0], CHIP_ID))

		print("BMM150 successfully initialized")

		self.read_trim_registers()
		self.set_op_mode(NORMAL_MODE)
		self.set_presetmode(PRESETMODE_LOWPOWER)

		self.calibrate(calibrate_ms)


	def i2c_read(self, address, buffer):
		self.i2c.readfrom_mem_into(I2C_Address, address, buffer)


	def i2c_write(self, address, data):
		self.i2c.writeto_mem(I2C_Address, address, data)


	def i2c_bit_op0(self, address, bitname, data):
		self.i2c_read(address, self.reg_data)
		self.reg_data[0] = set_bits_pos_0(self.reg_data[0], bitname, data)
		self.i2c_write(address, self.reg_data)


	def i2c_bit_op(self, address, bitname, data):
		self.i2c_read(address, self.reg_data)
		self.reg_data[0] = set_bits(self.reg_data[0], bitname, data)
		self.i2c_write(address, self.reg_data)


	def set_op_mode(self, power_mode):
		if power_mode in [NORMAL_MODE, FORCED_MODE, SLEEP_MODE]:
			self.suspend_to_sleep_mode()
			self.write_op_mode(power_mode)
		elif power_mode == SUSPEND_MODE:
			self.set_power_control_bit(POWER_CNTRL_DISABLE)


	def suspend_to_sleep_mode(self):
		self.set_power_control_bit(POWER_CNTRL_ENABLE)
		time.sleep_ms(3)


	def set_power_control_bit(self, bit):
		self.i2c_bit_op0(POWER_CONTROL_ADDR, PWR_CNTRL, bit)


	def write_op_mode(self, op_mode):
		self.i2c_bit_op(OP_MODE_ADDR, OP_MODE, op_mode)
		# self.i2c_read1(OP_MODE_ADDR)
		# self.reg_data1[0] = set_bits(self.reg_data1[0], OP_MODE, op_mode)
		# self.i2c_write(OP_MODE_ADDR, self.reg_data1)


	def read_trim_registers(self):
		temp_msb      = 0
		trim_x1y1     = bytearray(2)
		trim_xyz_data = bytearray(4)
		trim_xy1xy2   = bytearray(10)

		#Read trim register value
		self.i2c_read(DIG_X1,     trim_x1y1)
		self.i2c_read(DIG_Z4_LSB, trim_xyz_data)
		self.i2c_read(DIG_Z2_LSB, trim_xy1xy2)

		#Update trim data in device structure
		trim_data = self.trim

		trim_data[dig_x1]   = trim_x1y1[0]
		trim_data[dig_y1]   = trim_x1y1[1]
		trim_data[dig_x2]   = trim_xyz_data[2]
		trim_data[dig_y2]   = trim_xyz_data[3]
		temp_msb             = trim_xy1xy2[3] << 8
		trim_data[dig_z1]   = temp_msb | trim_xy1xy2[2]
		temp_msb             = trim_xy1xy2[1] << 8
		trim_data[dig_z2]   = temp_msb | trim_xy1xy2[0]
		temp_msb             = trim_xy1xy2[7] << 8
		trim_data[dig_z3]   = temp_msb | trim_xy1xy2[6]
		temp_msb             = trim_xyz_data[1] << 8
		trim_data[dig_z4]   = temp_msb | trim_xyz_data[0]
		trim_data[dig_xy1]  = trim_xy1xy2[9]
		trim_data[dig_xy2]  = trim_xy1xy2[8]
		temp_msb             = trim_xy1xy2[5] & 0x7F << 8
		trim_data[dig_xyz1] = temp_msb | trim_xy1xy2[4]


	def set_presetmode(self, preset_mode):
		settings = self.settings
		if preset_mode == PRESETMODE_LOWPOWER:
			settings[data_rate] = DATA_RATE_10HZ;
			settings[xy_rep]    = LOWPOWER_REPXY;
			settings[z_rep]     = LOWPOWER_REPZ;
			self.set_odr_xyz_rep();
		elif preset_mode == PRESETMODE_REGULAR:
			settings[data_rate] = DATA_RATE_10HZ;
			settings[xy_rep]    = REGULAR_REPXY;
			settings[z_rep]     = REGULAR_REPZ;
			self.set_odr_xyz_rep();
		elif preset_mode == PRESETMODE_HIGHACCURACY:
			settings[data_rate] = DATA_RATE_20HZ;
			settings[xy_rep]    = HIGHACCURACY_REPXY;
			settings[z_rep]     = HIGHACCURACY_REPZ;
			self.set_odr_xyz_rep();
		elif preset_mode == PRESETMODE_ENHANCED:
			settings[data_rate] = DATA_RATE_10HZ;
			settings[xy_rep]    = ENHANCED_REPXY;
			settings[z_rep]     = ENHANCED_REPZ;
			self.set_odr_xyz_rep();


	def set_odr_xyz_rep(self):
		self.i2c_bit_op(OP_MODE_ADDR, ODR, self.settings[data_rate])
		self.i2c_write(REP_XY_ADDR, bytes([self.settings[xy_rep]]))
		self.i2c_write(REP_Z_ADDR, bytes([self.settings[z_rep]]))


	def read_mag_data(self):
		reg_data = bytearray(XYZR_DATA_LEN)

		self.i2c_read(DATA_X_LSB, reg_data)

		reg_data[0] = get_bits(reg_data[0], DATA_X)
		self.mag_data_raw[0] = (reg_data[1]*32) | reg_data[0]

		reg_data[2] = get_bits(reg_data[2], DATA_Y)
		self.mag_data_raw[1] = (reg_data[3]*32) | reg_data[2]

		reg_data[4] = get_bits(reg_data[4], DATA_Z)
		self.mag_data_raw[2] = (reg_data[5]*128) | reg_data[4]

		reg_data[6] = get_bits(reg_data[6], DATA_RHALL)
		self.mag_data_raw[3] = (reg_data[7] << 6) | reg_data[6]

		if self.calibrated:
			self.mag_data[0] = self.mag_data_raw[0] - self.mag_offsets[0]
			self.mag_data[1] = self.mag_data_raw[1] - self.mag_offsets[1]
			self.mag_data[2] = self.mag_data_raw[2] - self.mag_offsets[2]
			return self.mag_data

		return self.mag_data_raw


	def calibrate(self, timeout=10):
		if timeout <= 0:
			return

		self.read_mag_data()

		xmin = xmax = self.mag_data_raw[0]
		ymin = ymax = self.mag_data_raw[1]
		zmin = zmax = self.mag_data_raw[2]

		time.sleep_ms(100)

		start = time.ticks_ms()
		while time.ticks_diff(time.ticks_ms(), start) < timeout:
			self.read_mag_data()
			xmin = min(xmin, self.mag_data_raw[0])
			xmax = max(xmax, self.mag_data_raw[0])
			ymin = min(ymin, self.mag_data_raw[1])
			ymax = max(ymax, self.mag_data_raw[1])
			zmin = min(zmin, self.mag_data_raw[2])
			zmax = max(zmax, self.mag_data_raw[2])

		time.sleep_ms(1)

		self.mag_offsets[0] = int(xmin + (xmax - xmin) / 2)
		self.mag_offsets[1] = int(ymin + (ymax - ymin) / 2)
		self.mag_offsets[2] = int(zmin + (zmax - zmin) / 2)

		self.calibrated = True



def run():
	from machine import I2C
	i2c = I2C(freq=400000, sda=0, scl=26)
	bmm150 = BMM150(i2c)
	print("Mag data:")
	print(bmm150.read_mag_data())
	return bmm150


if __name__ == "__main__":
	run()
