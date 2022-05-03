#from micropython import const
def const(a): return a

# Macro definitions

# API success code
OK = const(0)

# API error codes
E_ID_NOT_CONFORM = const(-1)
E_INVALID_CONFIG = const(-2)
#BMM150_E_ID_WRONG = -3

# API warning codes
W_NORMAL_SELF_TEST_YZ_FAIL = const(1)
W_NORMAL_SELF_TEST_XZ_FAIL = const(2)
W_NORMAL_SELF_TEST_Z_FAIL = const(3)
W_NORMAL_SELF_TEST_XY_FAIL = const(4)
W_NORMAL_SELF_TEST_Y_FAIL = const(5)
W_NORMAL_SELF_TEST_X_FAIL = const(6)
W_NORMAL_SELF_TEST_XYZ_FAIL = const(7)
W_ADV_SELF_TEST_FAIL = const(8)

I2C_Address = const(0x10)

# CHIP ID & SOFT RESET VALUES
CHIP_ID = const(0x32)
SET_SOFT_RESET = const(0x82)

# POWER MODE DEFINTIONS
NORMAL_MODE = const(0x00)
FORCED_MODE = const(0x01)
SLEEP_MODE = const(0x03)
SUSPEND_MODE = const(0x04)

# PRESET MODE DEFINITIONS
PRESETMODE_LOWPOWER = const(0x01)
PRESETMODE_REGULAR = const(0x02)
PRESETMODE_HIGHACCURACY = const(0x03)
PRESETMODE_ENHANCED = const(0x04)

# Power mode settings
POWER_CNTRL_DISABLE = const(0x00)
POWER_CNTRL_ENABLE = const(0x01)

# Sensor delay time settings
SOFT_RESET_DELAY = const(1)
NORMAL_SELF_TEST_DELAY = const(2)
START_UP_TIME = const(3)
ADV_SELF_TEST_DELAY = const(4)

# ENABLE/DISABLE DEFINITIONS
XY_CHANNEL_ENABLE = const(0x00)
XY_CHANNEL_DISABLE = const(0x03)

# Register Address
CHIP_ID_ADDR = const(0x40)
DATA_X_LSB = const(0x42)
DATA_X_MSB = const(0x43)
DATA_Y_LSB = const(0x44)
DATA_Y_MSB = const(0x45)
DATA_Z_LSB = const(0x46)
DATA_Z_MSB = const(0x47)
DATA_READY_STATUS = const(0x48)
INTERRUPT_STATUS = const(0x4A)
POWER_CONTROL_ADDR = const(0x4B)
OP_MODE_ADDR = const(0x4C)
INT_CONFIG_ADDR = const(0x4D)
AXES_ENABLE_ADDR = const(0x4E)
LOW_THRESHOLD_ADDR = const(0x4F)
HIGH_THRESHOLD_ADDR = const(0x50)
REP_XY_ADDR = const(0x51)
REP_Z_ADDR = const(0x52)

# DATA RATE DEFINITIONS
DATA_RATE_10HZ = const(0x00)
DATA_RATE_02HZ = const(0x01)
DATA_RATE_06HZ = const(0x02)
DATA_RATE_08HZ = const(0x03)
DATA_RATE_15HZ = const(0x04)
DATA_RATE_20HZ = const(0x05)
DATA_RATE_25HZ = const(0x06)
DATA_RATE_30HZ = const(0x07)

# TRIM REGISTERS
#Trim Extended Registers
DIG_X1 = const(0x5D)
DIG_Y1 = const(0x5E)
DIG_Z4_LSB = const(0x62)
DIG_Z4_MSB = const(0x63)
DIG_X2 = const(0x64)
DIG_Y2 = const(0x65)
DIG_Z2_LSB = const(0x68)
DIG_Z2_MSB = const(0x69)
DIG_Z1_LSB = const(0x6A)
DIG_Z1_MSB = const(0x6B)
DIG_XYZ1_LSB = const(0x6C)
DIG_XYZ1_MSB = const(0x6D)
DIG_Z3_LSB = const(0x6E)
DIG_Z3_MSB = const(0x6F)
DIG_XY2 = const(0x70)
DIG_XY1 = const(0x71)

# PRESET MODES - REPETITIONS-XY RATES
LOWPOWER_REPXY = const(1)
REGULAR_REPXY = const(4)
ENHANCED_REPXY = const(7)
HIGHACCURACY_REPXY = const(23)

# PRESET MODES - REPETITIONS-Z RATES
LOWPOWER_REPZ = const(2)
REGULAR_REPZ = const(14)
ENHANCED_REPZ = const(26)
HIGHACCURACY_REPZ = const(82)


# OVERFLOW DEFINITIONS
XYAXES_FLIP_OVERFLOW_ADCVAL = const(-4096)
ZAXIS_HALL_OVERFLOW_ADCVAL = const(-16384)
OVERFLOW_OUTPUT = const(-32768)
NEGATIVE_SATURATION_Z = const(-32767)
POSITIVE_SATURATION_Z = const(32767)
#ifdef BMM150_USE_FLOATING_POINT
OVERFLOW_OUTPUT_FLOAT = 0.0
#endif

# Register read lengths
SELF_TEST_LEN = const(5)
SETTING_DATA_LEN = const(8)
XYZR_DATA_LEN = const(8)

# Self test selection macros
NORMAL_SELF_TEST = const(0)
ADVANCED_SELF_TEST = const(1)

# Self test settings
DISABLE_XY_AXIS = const(0x03)
SELF_TEST_REP_Z = const(0x04)

# Advanced self-test current settings
DISABLE_SELF_TEST_CURRENT = const(0x00)
ENABLE_NEGATIVE_CURRENT = const(0x02)
ENABLE_POSITIVE_CURRENT = const(0x03)

# Normal self-test status
SELF_TEST_STATUS_XYZ_FAIL = const(0x00)
SELF_TEST_STATUS_SUCCESS = const(0x07)

# _MSK = 0, _POS = 1
PWR_CNTRL          = bytearray([0x01])
CONTROL_MEASURE    = bytearray([0x38, 0x03])
POWER_CONTROL_BIT  = bytearray([0x01, 0x00])
OP_MODE            = bytearray([0x06, 0x01])
ODR                = bytearray([0x38, 0x03])
DATA_X             = bytearray([0xF8, 0x03])
DATA_Y             = bytearray([0xF8, 0x03])
DATA_Z             = bytearray([0xFE, 0x01])
DATA_RHALL         = bytearray([0xFC, 0x02])
SELF_TEST          = bytearray([0x01])
ADV_SELF_TEST      = bytearray([0xC0, 0x06])
DRDY_EN            = bytearray([0x80, 0x07])
INT_PIN_EN         = bytearray([0x40, 0x06])
DRDY_POLARITY      = bytearray([0x04, 0x02])
INT_LATCH          = bytearray([0x02, 0x01])
INT_POLARITY       = bytearray([0x01])
DATA_OVERRUN_INT   = bytearray([0x80, 0x07])
OVERFLOW_INT       = bytearray([0x40, 0x06])
HIGH_THRESHOLD_INT = bytearray([0x38, 0x03])
LOW_THRESHOLD_INT  = bytearray([0x07])
DRDY_STATUS        = bytearray([0x01])

# trim register names
dig_x1   = const(0)
dig_y1   = const(1)
dig_x2   = const(2)
dig_y2   = const(3)
dig_z1   = const(4)
dig_z2   = const(5)
dig_z3   = const(6)
dig_z4   = const(7)
dig_xy1  = const(8)
dig_xy2  = const(9)
dig_xyz1 = const(10)

# settings names
xyz_axes_control = const(0)
pwr_cntrl_bit    = const(1)
pwr_mode         = const(2)
data_rate        = const(3)
xy_rep           = const(4)
z_rep            = const(5)
preset_mode      = const(6)

# mag_data names
x = const(0)
y = const(1)
z = const(2)
