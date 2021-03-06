#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime
import colorama
from colorama import Style
from urllib.request import urlopen

os.chdir('/opt/wr')
import joblib
from auxiliary import *

colorama.init()

help_string = """
The wr command collects a weather report from OpenWeatherMap and prints it to the terminal in a concise format.
Users can modify the behavior of the program with the following flags:

-f			  displays temps in fahrenheit
--today		  displays the three-hourly forecast for the day
--zip		  specifiy location with ZIP code
--coords	  or with lat/lon
--save		  saves the location specified so you don't have to enter it again
--show-loc	  shows the name of the city along with the weather report
"""


def default():
	api_url = generate_url()
	json_str = urlopen(api_url).read().decode()
	json_dict = json.loads(json_str)
	weekday = datetime.datetime.today().weekday()

	descripts = [day['weather'][0]['description'] for day in json_dict['list'][0:9]]
	max_desc_len = max(map(len, descripts))

	expl_string = Style.BRIGHT + "Weekday" + Style.RESET_ALL + "    │ " + Style.BRIGHT + \
		"Temp" + Style.RESET_ALL + "  │ " + Style.BRIGHT + "Info" + Style.RESET_ALL

	print()
	if '--show-loc' in sys.argv:
		print(Style.BRIGHT + json_dict['city']['name'] + Style.RESET_ALL + '\n')
	print(expl_string)

	for i, day in zip(range(7), json_dict['list']):
		k_temp = float(day['temp']['day'])
		if '-f' in sys.argv:
			conv_temp = convert_kelvin(k_temp, 'f')
		else:
			conv_temp = convert_kelvin(k_temp)

		description = day['weather'][0]['description']
		description = description[0].upper() + description[1:]

		if '-f' in sys.argv:
			temp_string = temp_colorizer(conv_temp, 'f') + "°" + (' ' * (5 - len(str(conv_temp)))) + '│ '
		else:
			temp_string = temp_colorizer(conv_temp) + "°" + (' ' * (5 - len(str(conv_temp)))) + '│ '
		# TODO fix that redundancy

		print('─' * 11, '┼', '─' * 7, '┼', '─' * (max_desc_len + 5), sep='')
		print(date_indexer((weekday + i) % 7), temp_string + description)
	print()


def hourly():
	api_url = generate_url(forecast=Weather.HOURLY)
	json_str = urlopen(api_url).read().decode()
	json_dict = json.loads(json_str)

	expl_string = Style.BRIGHT + "Time" + Style.RESET_ALL + "  │ " + Style.BRIGHT + \
		"Temp" + Style.RESET_ALL + "  │ " + Style.BRIGHT + "Info" + Style.RESET_ALL

	descripts = [day['weather'][0]['description'] for day in json_dict['list'][0:9]]
	max_desc_len = max(map(len, descripts))

	print()
	if '--show-loc' in sys.argv:
		print(Style.BRIGHT + json_dict['city']['name'] + Style.RESET_ALL + '\n')
	print(expl_string)

	for day in json_dict['list'][0:9]:
		time = ("%02d" % datetime.datetime.fromtimestamp(day['dt']).hour) + ":00"

		if '-f' in sys.argv:
			conv_temp = convert_kelvin(day['main']['temp'], 'f')
		else:
			conv_temp = convert_kelvin(day['main']['temp'])

		if '-f' in sys.argv:
			temp_string = temp_colorizer(conv_temp, 'f') + "°" + (' ' * (5 - len(str(conv_temp)))) + '│ '
		else:
			temp_string = temp_colorizer(conv_temp) + "°" + (' ' * (5 - len(str(conv_temp)))) + '│ '

		description = day['weather'][0]['description']
		description = description[0].upper() + description[1:]

		print('─' * 6, '┼', '─' * 7, '┼', '─' * (max_desc_len + 5), sep='')
		print(time, " │ ", temp_string, description, sep='')
	print()


def main():
	if '--help' in sys.argv:
		print(help_string)
		exit(0)
	else:
		try:
			if '--today' in sys.argv:
				hourly()
			else:
				default()
		except urllib.error.URLError:
			print("You must be connected to the Internet to use this program.")
			exit(-1)


if __name__ == '__main__':
	main()
