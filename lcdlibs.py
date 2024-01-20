################################################################################

def wake_the_screens(sleep_time = 3):

	# Clear the LCDs - Quicker than doing the in-built clear
	for x in range(4):
		clear_lcd_line(x, 20, lcd)
	for x in range(2):
		clear_lcd_line(x, 16, lcd2)

	# Get the OLED ready for something...
	oled.fill(0)

	display_image(mount_background(), 0, 0)
	display_image(cp_logo(), 0, 0)  # Put an "image" onto the screen a pixel at a time!
	oled.text("COYOTE", 47, 5, 1)
	oled.text("PRODUTIONS", 50, 15, 1)
	oled.show()

	sleep(sleep_time)
	oled.fill(0) # Wipe the screen before we load the time info
	oled.show()

################################################################################

def get_ip_address(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', bytes(ifname[:15], 'utf-8'))
		)[20:24])
	except OSError:
		return '???.???.???.???'
	except:
		return '???.???.???.???'

################################################################################

def ddhhmmss(seconds: int) -> tuple:
	(days, remainder) = divmod(seconds, 86400)
	(hours, remainder) = divmod(remainder, 3600)
	(minutes, seconds) = divmod(remainder, 60)

	return collections.namedtuple("uptime", ("day", "hour", "min", "sec"))(days, hours, minutes, seconds)

################################################################################

def get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])

	return int(uptime_seconds)

################################################################################

def get_size(bytes):
	"""
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
	"""
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}"
		bytes /= factor

################################################################################

def System_information():
	## Based on https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
	cpufreq = psutil.cpu_freq()
	net_io = psutil.net_io_counters()
	partitions = psutil.disk_partitions()
	environment_factors = temp_humidity()

	# Disk Information
	# get all disk partitions
	partitions = psutil.disk_partitions()
	for partition in partitions:
		if partition.mountpoint == '/':
			try:
				partition_usage = psutil.disk_usage(partition.mountpoint)
			except PermissionError:
				# this can be catched due to the disk that isn't ready
				continue

	cpu = CPUTemperature()
	la = LoadAverage()
	cpu_temp = round(cpu.temperature, 1)

	process = os.popen('cat /proc/loadavg | awk \'{print $1}\'')
	cmdread = process.read()
	process.close()
	cpu_usage = float(cmdread)
	number_of_logical_processors = psutil.cpu_count(logical=True)

	# Load percentage is load number [e.g.  0.44] divided by CPU count [RaspPi 5 = 4] times 100.
	load_ave = float( ( cpu_usage / number_of_logical_processors )* 100 )
	check_load_ave = int(float(load_ave))

	lcd.cursor_pos = (0,0)
	lcd.write_string('CPU' + str("{:.2f}".format(psutil.cpu_percent())).rjust(6) + "%")
	lcd.cursor_pos = (0,11)
	lcd.write_string(get_size(partition_usage.free).rjust(9))

	lcd.cursor_pos = (1,0)
	lcd.write_string("U" + get_size(net_io.bytes_sent).rjust(9))
	lcd.cursor_pos = (1,11)
	lcd.write_string("D" + get_size(net_io.bytes_recv).rjust(8))

	lcd.cursor_pos = (2,0)
	lcd.write_string('CPU')
	lcd.cursor_pos = (2,5)
	lcd.write_string(str(cpu_temp) + 'c')

	lcd.cursor_pos = (2,11)
	if check_load_ave < 5:
		load_ave_str = '\x00 LOW'.rjust(7)
	elif check_load_ave > 100:
		load_ave_str = '\x01 HIGH'.rjust(7)
	else:
		load_ave_str =  str( "{:.2f}".format(load_ave) ).rjust(6) + "%"
	lcd.write_string("LA" + load_ave_str)

	lcd.cursor_pos = (3,0)
	lcd.write_string('EXT')
	lcd.cursor_pos = (3,5)
	lcd.write_string(str(round(environment_factors.temp,1)) + 'c')
	lcd.cursor_pos = (3,11)
	lcd.write_string("HUM" + str(environment_factors.humid).rjust(5) + '%')

	show_ip_address(1, lcd2)

################################################################################

def show_ip_address(row, lcd_type = 'lcd2'):
	# Check that we have an IP address on wlan
	ip_address = get_ip_address('wlan0')
	lcd_type.cursor_pos = (row, center_text_start_pos(ip_address, 16))
	lcd_type.write_string(ip_address)

################################################################################

def get_the_cpu_bar(row = 1, col = 16, lcd_type = 'lcd2'):
	cpufreq = psutil.cpu_freq()
	percent_by_cell = 100 / col
	current_percentage = (cpufreq.current / cpufreq.max) * 100
	number_of_bars = int(current_percentage / percent_by_cell)
	lcd_type.cursor_pos = (row,0)
	number_of_boxes_string = ''
	for x in range(number_of_bars):
		number_of_boxes_string += '\x03'
	lcd_type.write_string(number_of_boxes_string)

################################################################################

def clear_lcd_line(line, col = 20, lcd_type = 'lcd'):
	for n in range(col) :
		lcd_type.cursor_pos = (line, n);
		lcd_type.write_string(" ");

################################################################################

def time_now(lcd_to_use, width = 20) :
	now = datetime.now()
	if width != 16:
		dt_string = now.strftime("%b %d %Y %H:%M:%S")
	else :
		dt_string = now.strftime("%Y-%m-%d %H:%M")
	lcd_to_use.cursor_pos = (1,0)
	lcd_to_use.write_string(dt_string)

################################################################################

def flash_char(char):
	lcd.cursor_pos = (0,0)
	lcd.write_string(char)
	lcd.cursor_pos = (0,19)
	lcd.write_string(char)

################################################################################

def printable_ascii_chars():

	chars = ''
	for c in (chr(i) for i in range(32, 127)):
		chars += c
	for c in (chr(i) for i in range(161, 255)):
		chars += c
	return chars

################################################################################

def id_generator(char_string, width = 20):
	return ''.join(random.choice(char_string) for _ in range(width))

################################################################################

def dump_uptime() :
	lcd.clear()
	uptime_array = ddhhmmss(get_uptime())

	text_string = 'Uptime'
	lcd.cursor_pos = (0, center_text_start_pos(text_string))
	lcd.write_string(text_string)

	lcd.cursor_pos = (1,0)
	lcd.write_string(str(uptime_array.day).rjust(3) + ' Day')
	lcd.cursor_pos = (1,9)
	lcd.write_string(str(uptime_array.hour).rjust(3) + ' Hour')

	lcd.cursor_pos = (2,0)
	lcd.write_string(str(uptime_array.min).rjust(3) + ' Min')
	lcd.cursor_pos = (2,9)
	lcd.write_string(str(uptime_array.sec).rjust(3) + ' Sec')

	sleep(2)

################################################################################

def dump_uptime_string() :

	uptime_array = ddhhmmss(get_uptime())
	uptime_format_string = 'Up '
	if uptime_array.day > 0:
		uptime_format_string += str(uptime_array.day) + 'D '
	if uptime_array.hour > 0:
		uptime_format_string += str(uptime_array.hour) + 'H '
	if uptime_array.min > 0:
		uptime_format_string +=  str(uptime_array.min) + 'M '
	uptime_format_string +=  str(uptime_array.sec) + 'S'

	return uptime_format_string

################################################################################

def do_matrix_thing(chars):
#	print(get_the_current_time("uptime"))
	for j in range(10):
		for k in range(4):
			lcd.cursor_pos = (k,0)
			lcd.write_string(id_generator(chars))
		sleep(1)
		lcd.clear()
		display_string_to_oled(2, 23, 0, 14, get_the_current_time("time", 0))
		oled.show()

		clear_lcd_line(1, 16, lcd2)
		get_the_cpu_bar(1, 16, lcd2)

		lcd2.cursor_pos = (1, 0)
	clear_lcd_line(1, 16, lcd2)

################################################################################

def center_text_start_pos(text_string, width = 20):
	string_length = len(text_string)
	return int((width - string_length)/2)

################################################################################

def who_am_i(text_string, lcd_to_use, width = 20):
	lcd_to_use.cursor_pos = (0, center_text_start_pos(text_string, width))
	lcd_to_use.write_string(text_string)

################################################################################

def temp_humidity():
	MeasureCmd = [0x33, 0x00]
	bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
	data = bus.read_i2c_block_data(0x38,0x00)
	temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
	ctemp = ((temp*200) / 1048576) - 50
	tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
	ctmp = int(tmp * 100 / 1048576)

	return collections.namedtuple("temp_hum", ("temp", "humid"))(ctemp, ctmp)

################################################################################

def generate_special_chars():

	# Happy face on 4x20
	smiley = (
		0b00000, 0b01010, 0b01010, 0b00000, 0b10001, 0b10001, 0b01110, 0b00000
	)

	# Sad face on 4x20
	sadney = (
		0b00000, 0b01010, 0b01010, 0b00000, 0b01110, 0b10001, 0b10001, 0b00000
	)

	# Person on 4x20
	person = (
		0b01110, 0b01110, 0b01110, 0b00100, 0b11111, 0b00100, 0b01010, 0b10001
	)

	# Set for both [4x20 & 2x16] LCDs at the same position
	full_box = (
		0b10101, 0b01010, 0b10101, 0b01010, 0b10101, 0b01010, 0b10101, 0b01010
	)

	lcd.create_char(0, smiley)
	lcd.create_char(1, sadney)
	lcd.create_char(2, person)

	lcd.create_char(3, full_box)
	lcd2.create_char(3, full_box)

################################################################################
