from os import listdir
import re

def main():
	files = [f for f in listdir('normal') if '.gif' in f]
	files.sort()
	for file in files:
		with open(f'normal/{file}', 'rb') as f:
			hexdata = f.read().hex()
		if hexdata[:12] != '474946383961':
			print(file)
			continue
		for m in re.finditer(r'21f904[0-9a-f]{8}00', hexdata, re.I):
			st, _ = m.span()
			hexdata = f'{hexdata[:st+6]}09{hexdata[st+8:]}'
		with open(f'normal/{file}', 'wb') as f:
			f.write(bytes.fromhex(''.join(hexdata)))

if __name__ == '__main__':
	main()