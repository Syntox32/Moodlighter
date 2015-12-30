#
# https://github.com/Syntox32/Audiolyser/blob/master/ledserver.py
#
import os, sys, time, spidev #, fcntl

class LEDStrip(object):
	"""
	Wrapper class for simpler interaction with the WS2801 led-strip
	"""

	def __init__(self, numleds, x=0, d=0):
		"""
		Initalize an LEDDevice with the number of LEDs to control

		Parameter x and d are representative of the location of the device:
		/dev/spidev{bus=x}.{device=d}

		Credits to Doceme for the spidev python port
		https://github.com/doceme/py-spidev

		Credits to Scott Gibson for the gamma correction
		https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py#L604
		"""
		self._spi = spidev.SpiDev()
		self._open = False
		self.x = x
		self.d = d
		self.chip_name = "WS2801"
		self.brightness = 1.0
		self.bits_per_pixel = 3
		self.num_leds = numleds

		# Gamma correction for the LEDs
		self.gamma_table = bytearray(256)
		for i in range(256):
			self.gamma_table[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

	def open(self, speed=1000000):
		"""
		Open an spi device
		"""
		try:
			print("Creating LED device for chip:{0}".format(self.chip_name))
			self._spi.open(self.x, self.d)
			self._spi.max_speed_hz = speed
			self._spi.bits_per_word = 8
			self._spi.mode = 2 # SPI_CPOL - high bit order
			self._open = True
			print("SPI Interface ready -> /dev/spidev{0}.{1}".format(str(self.x), str(self.d)))
			print("SPI Mode:", str(self._spi.mode))
			print("SPI Bits Per Word:{0}".format(str(self._spi.bits_per_word)))
			print("SPI Max Speed: {0}Hz ({1}KHz)".format(str(self._spi.max_speed_hz), 
			str(self._spi.max_speed_hz / 1000)))
			return True
		except IOError as e:
			print("IO Error opening SPI Device: {0}".format(e))
			return False
		except Exception as e:
			print("Error opening SPI Device: {0}".format(e))
			return False

	def write(self, intarray):
		"""
		Write a byte array to the device

		The WS2801 chip uses simple 24-bit RGB color for each LED
		A byte-array should be like this: rgbrgbrgr...
		"""
		self._spi.writebytes(intarray)

	def write_gc(self, intarray):
		"""
		Write a gamma corrected array of rgb colors
		"""
		self._spi.writebytes([self.gamma_table[intarray[i]] for i in range(0, len(intarray))])

	def write_gc_wb(self, intarray, brightness=1.0):
		"""
		Write a gamma corrected array of rgb colors with shitty brightness
		"""
		self._spi.writebytes([
		self.gamma_table[int(intarray[i] * brightness)] for i in range(0, len(intarray))])

	def all_on(self):
		"""
		Turn on all the LEDS
		"""
		self._spi.writebytes([0xFF for _ in range(0, self.num_leds * self.bits_per_pixel)])

	def all_off(self):
		"""
		Turn of all the LEDs
		"""
		self._spi.writebytes([0x00 for _ in range(0, self.num_leds * self.bits_per_pixel)])

	def close(self):
		"""
		Close the spi device and turn off all the lights
		"""
		print("Closing SPI interface..")
		if self._spi.open:
			self.all_off()
			self._spi.close()
			self.open = False