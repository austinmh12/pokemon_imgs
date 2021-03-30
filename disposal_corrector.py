from os import listdir

def unsigned_bit(bits):
	return int(''.join([bits[1], bits[0]]), 16)

def unpack_bit(bit):
	return bin(int(bit, 16))[2:].zfill(8)

def pack_bit(bit):
	return hex(int(bit, 2))[2:].zfill(2)

class GIF:
	def __init__(self, file):
		with open(file, 'rb') as f:
			hb = f.read().hex()
			self.hb = list(map(''.join, zip(hb[::2], hb[1::2])))
		self.header = self.hb[:6]
		logical_screen_descriptor = self.hb[6:13]
		self.parse_logical_screen_descriptor(logical_screen_descriptor)
		if self.global_colour_table_flag:
			self.colours = self.hb[13:13 + self.colour_table_size]
		else:
			self.colours = []
		if self.colours:
			netscape_start = 13 + self.colour_table_size
		else:
			netscape_start = 13
		self.gce_start = netscape_start + 19
		self.graphics_control_extension = self.hb[self.gce_start:self.gce_start + 8]
		self.parse_graphics_control_extension(self.graphics_control_extension)
		if self.disposal_method != '010':
			self.fix_disposal()
			self.fixed = True
		else:
			self.fixed = False

	@property
	def packed_transpareny_info(self):
		return pack_bit('00001001')

	def parse_logical_screen_descriptor(self, logical_screen_descriptor):
		self.width = unsigned_bit(logical_screen_descriptor[:2])
		self.height = unsigned_bit(logical_screen_descriptor[2:4])
		colour_info_unpacked = unpack_bit(logical_screen_descriptor[4])
		self.global_colour_table_flag = colour_info_unpacked[0] == '1'
		if self.global_colour_table_flag:
			self.sort_flag = colour_info_unpacked[4] == '1'
			self.colour_table_size = (2 ** (int(''.join(colour_info_unpacked[5:]), 2) + 1)) * 3
		self.bg_colour_index = int(logical_screen_descriptor[5], 16)

	def parse_graphics_control_extension(self, graphics_control_extension):
		transparency_info_unpacked = unpack_bit(graphics_control_extension[3])
		self.disposal_method = transparency_info_unpacked[3:6]
		self.transparent = transparency_info_unpacked[-1] == '1'
		self.delay = unsigned_bit(graphics_control_extension[4:6])
		self.transparency_index = int(graphics_control_extension[6], 16)

	def fix_disposal(self):
		self.hb[self.gce_start + 3] = self.packed_transpareny_info

	def save(self, fn):
		with open(fn, 'wb') as f:
			f.write(bytes.fromhex(''.join(self.hb)))

def main():
	files = [f for f in listdir('normal') if '.gif' in f]
	files.sort()
	for file in files:
		g = GIF(f'normal/{file}')
		if ''.join(g.header) != '474946383961':
			print(file)
		if g.fixed:
			g.save(f'normal/{file}')


if __name__ == '__main__':
	main()