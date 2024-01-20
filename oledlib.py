def get_the_current_time(type="time", flash=0):

	# Do the time stuff
	current_time = datetime.now()
	#    current_time = time.localtime(time.time())
	#    print(current_time)
	if type == "time":
		if flash == 0:
			return "{:02d}:{:02d}.{:02d}".format(
				current_time.hour,
				current_time.minute,
				current_time.second,
			 )
		else:
			return "{:02d} {:02d}.{:02d}".format(
				current_time.hour,
				current_time.minute,
				current_time.second,
			)
	elif type == "date":
		return "{} {} {}, {}".format(
			day_name(current_time.weekday()),
			month_name(current_time.month),
			current_time.day,
			current_time.year,
		)
	elif type == "uptime":
		return dump_uptime_string()
	else:
		return current_time

# -------------------------------------------------------------------------------

def month_name(month):
    if month == 1:
        return str("Jan")
    elif month == 2:
        return str("Feb")
    elif month == 3:
        return str("Mar")
    elif month == 4:
        return str("Apr")
    elif month == 5:
        return str("May")
    elif month == 6:
        return str("Jun")
    elif month == 7:
        return str("Jly")
    elif month == 8:
        return str("Aug")
    elif month == 9:
        return str("Sep")
    elif month == 10:
        return str("Oct")
    elif month == 11:
        return str("Nov")
    elif month == 12:
        return str("Dec")

# -------------------------------------------------------------------------------

def full_month_name(month):
    if month == 1:
        return str("January")
    elif month == 2:
        return str("February")
    elif month == 3:
        return str("March")
    elif month == 4:
        return str("April")
    elif month == 5:
        return str("May")
    elif month == 6:
        return str("June")
    elif month == 7:
        return str("July")
    elif month == 8:
        return str("August")
    elif month == 9:
        return str("September")
    elif month == 10:
        return str("October")
    elif month == 11:
        return str("November")
    elif month == 12:
        return str("December")

# -------------------------------------------------------------------------------

def day_name(day):
    #    print("[" + str(day) + "]")
    if str(day) == "0":
        return str("Mon")
    elif str(day) == "1":
        return str("Tue")
    elif str(day) == "2":
        return str("Wed")
    elif str(day) == "3":
        return str("Thu")
    elif str(day) == "4":
        return str("Fri")
    elif str(day) == "5":
        return str("Sat")
    elif str(day) == "6":
        return str("Sun")
    else:
        return str("")

# -------------------------------------------------------------------------------

def full_day_name(day):
    #    print("[" + str(day) + "]")
    if str(day) == "0":
        return str("Monday")
    elif str(day) == "1":
        return str("Tuesday")
    elif str(day) == "2":
        return str("Wednesday")
    elif str(day) == "3":
        return str("Thursday")
    elif str(day) == "4":
        return str("Friady")
    elif str(day) == "5":
        return str("Saturday")
    elif str(day) == "6":
        return str("Sunday")
    else:
        return str("")

# -------------------------------------------------------------------------------

def show_image(image_name, off_x, off_y):
    for y, row in enumerate(image_name):
        for x, c in enumerate(row):
            oled.pixel(x + off_x, y + off_y, c)

# -------------------------------------------------------------------------------

def display_string_to_oled(x_start, y_start, y_shift, x_shift, display_string):
    for number_displayed in display_string:
        number_print = str(number_displayed)
        show_image(
            character_image(number_print), x_start, y_start
        )  # Put an "image" onto the screen a pixel at a time!
        x_start += x_shift
        y_start += y_shift

# -------------------------------------------------------------------------------

def display_clear():
    display.fill(0)  # Clear the display
    display.show()

# -------------------------------------------------------------------------------

def display_coypte_productions_logo():
    display.fill(0)  # Clear the display
    display_image(cp_logo(), 0, 0)  # Put an "image" onto the screen a pixel at a time!
    display.text("COYOTE", 47, 5, 1)
    display.text("PRODUTIONS", 35, 15, 1)
    display.show()

# -------------------------------------------------------------------------------
