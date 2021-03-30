from os import listdir

def main():
	files = [f for f in listdir('normal') if '.gif' in f]
	files.sort()
	for file in files:
		with open(f'normal/{file}', 'rb') as f:
			hexdata = f.read().hex()
		if hexdata[:12] != '474946383961':
			print(file)
			continue
		for m in re.findall(r'21f904[0-9a-f]{8}00', hexdata, re.I):
			st, _ = 
			hexdata[st+6:st+8] = '09'
		with open(f'normal/{file}', 'wb') as f:
			f.write(bytes.fromhex(''.join(hexdata)))

if __name__ == '__main__':
	main()