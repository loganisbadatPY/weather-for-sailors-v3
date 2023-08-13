from tkinter import *
import tkinter.font as font
import requests
from datetime import datetime

TIDE_API_URL = "https://api.niwa.co.nz/tides/data?lat=-36.8667&long=174.7667&apikey=AVSnwX4R53kB1Yh17vY2zs1qGibFGw0Y"
weather_api_key = "9522fe2047582e922d19ac9849c35ee6"
city = "Auckland"

def get_wind_speed_category(speed):
    if speed < 5:
        return "Light"
    elif 6 <= speed <= 14:
        return "Normal"
    else:
        return "Windy"
    
logged_in_username = ""
logged_in_user_choice1 = ""
logged_in_user_choice2 = ""
logged_in_user_choice3 = ""

user_file = open("last_user.txt", "r+")
lines = user_file.readlines()

for username in lines:
    if username.strip():
        logged_in_username = username.strip()
        break

user_file.close()

if not (logged_in_username == ""):
    choices_file = open("db/choices.txt", "r+")
    choices_lines = choices_file.readlines()

    for line in choices_lines:
        if (logged_in_username.strip() in line):
            user_choices_string = line.split("=")
            logged_in_user_choice1 = user_choices_string[1].strip()
            logged_in_user_choice2 = user_choices_string[2].strip()
            logged_in_user_choice3 = user_choices_string[3].strip()

            print(logged_in_user_choice1, logged_in_user_choice2, logged_in_user_choice3)
            break

    choices_file.close()

# Create the Tkinter window
tkWindow = Tk()
tkWindow.geometry("1400x800")
tkWindow.title('Weather For Sailors')

high_tide_text = StringVar()
high_tide_text.set("")

low_tide_text = StringVar()
low_tide_text.set("")

normal_font = font.Font(family="Arial", size=20)
bold_font = font.Font(family="Arial", size=24, weight="bold")

frame1 = Frame(tkWindow, bg="#0b419e", width=450, height=660)
frame1.place(x=10, y=100)

frame2 = Frame(tkWindow, bg="#2473d4", width=470, height=660)
frame2.place(x=470, y=100)

frame3 = Frame(tkWindow, bg="#40aadb", width=440, height=660)
frame3.place(x=949, y=100)

def get_weather_conditions():
    base_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    response = requests.get(base_weather_url).json()
    wind_speed = response['wind']['speed']
    temperature = response['main']['temp']
    weather = response['weather'][0]['description']
    return wind_speed, temperature, weather


def get_tide_data():
    response = requests.get(TIDE_API_URL)
    data = response.json()
    return data["values"]

def find_next_high_low_tides(tide_data):
    high_tides = []
    low_tides = []
    
    for entry in tide_data:
        if entry["value"] > 2.0:
            high_tides.append(entry)
        elif entry["value"] < 1.0:
            low_tides.append(entry)
    
    return high_tides, low_tides

def get_time_string(timestamp):
    time = datetime.fromisoformat(timestamp[:-1])
    return time.strftime("%H:%M")

def display_next_tides():
    tide_data = get_tide_data()
    high_tides, low_tides = find_next_high_low_tides(tide_data)
    
    next_high_tide = high_tides[0] if high_tides else None
    next_low_tide = low_tides[0] if low_tides else None
    
    high_tide_text.set(f"Next High Tide: {get_time_string(next_high_tide['time'])}" if next_high_tide else "No High Tide Today")
    low_tide_text.set(f"Next Low Tide: {get_time_string(next_low_tide['time'])}" if next_low_tide else "No Low Tide Today")

    #high_tide_label.config(text=f"Next High Tide: {get_time_string(next_high_tide['time'])}" if next_high_tide else "No High Tide Today")
    #low_tide_label.config(text=f"Next Low Tide: {get_time_string(next_low_tide['time'])}" if next_low_tide else "No Low Tide Today")

def choice_wind_speed(wind_speed):
    if logged_in_user_choice1 == 'Windspeed':
        sailing_variable1 = Label(frame1, text=f"Wind Speed: {wind_speed} m/s", fg="white", bg="#0b419e", font=bold_font)
        sailing_variable1.place(x=10, y=10)

    elif logged_in_user_choice2 == 'Windspeed':
        sailing_variable1 = Label(frame2, text=f"Wind Speed: {wind_speed} m/s", fg="white", bg="#0b419e", font=bold_font)
        sailing_variable1.place(x=10, y=10)

    elif logged_in_user_choice3 == 'Windspeed':
        sailing_variable1 = Label(frame3, text=f"Wind Speed: {wind_speed} m/s", fg="white", bg="#40aadb", font=bold_font)
        sailing_variable1.place(x=10, y=10)



def choice_tide_time():
    if logged_in_user_choice1 == 'Tide':
        tide_variable = Frame(frame1, bg="#0b419e", width=470, height=660)
        tide_variable.place(x=0, y=0)

        high_tide_label = Label(tide_variable, textvariable=high_tide_text, font=bold_font, bg="#0b419e", fg="white")
        high_tide_label.place(x=10, y=10)
    
        low_tide_label = Label(tide_variable, textvariable=low_tide_text, font=bold_font, bg="#0b419e", fg="white")
        low_tide_label.place(x=10, y=50)

        print("Created")
    
    elif logged_in_user_choice2 == 'Tide':
        tide_variable = Frame(frame2, bg="#2473d4", width=470, height=660)
        tide_variable.place(x=0, y=0)

    
        high_tide_label = Label(tide_variable, textvariable=high_tide_text, font=bold_font, bg="#2473d4", fg="white")
        high_tide_label.place(x=10, y=10)
    
        low_tide_label = Label(tide_variable, textvariable=low_tide_text, font=bold_font, bg="#2473d4", fg="white")
        low_tide_label.place(x=10, y=50)

        print("Created2")

    elif logged_in_user_choice3 == 'Tide':
        tide_variable = Frame(frame3, bg="#40aadb", width=470, height=660)
        tide_variable.place(x=0, y=0)

   
        high_tide_label = Label(tide_variable, textvariable=high_tide_text, font=bold_font, bg="#40aadb", fg="white")
        high_tide_label.place(x=10, y=10)
    
        low_tide_label = Label(tide_variable, textvariable=low_tide_text, font=bold_font, bg="#40aadb", fg="white")
        low_tide_label.place(x=10, y=50)

        print("Created3")

    display_next_tides()

def choice_temperature(temperature):
    rounded_temperature = round(temperature - 273, 3)  # Round to 3 decimal places
    if logged_in_user_choice1 == 'Temperature':     
        temperature_variable = Label(frame1, text=f"Temperature: {rounded_temperature} °C", fg="white", bg="0b419e", font=bold_font)
        temperature_variable.place(x=10, y=10)

    if logged_in_user_choice2 == 'Temperature':     
        temperature_variable = Label(frame2, text=f"Temperature: {rounded_temperature} °C", fg="white", bg="#2473d4", font=bold_font)
        temperature_variable.place(x=10, y=10)

    if logged_in_user_choice3 == 'Temperature':     
        temperature_variable = Label(frame3, text=f"Temperature: {rounded_temperature} °C", fg="white", bg="#40aadb", font=bold_font)
        temperature_variable.place(x=10, y=10)

def choice_weather(weather):
    if logged_in_user_choice1 == 'Weather': 
        weather_variable = Label(frame1, text =f"Weather: {weather}", fg= 'white', bg = "#0b419e",font=bold_font)
        weather_variable.place(x=10,y=10)

    elif logged_in_user_choice2 == 'Weather': 
        weather_variable = Label(frame2, text =f"Weather: {weather}", fg= 'white', bg = "#2473d4",font=bold_font)
        weather_variable.place(x=10,y=10)

    elif logged_in_user_choice3 == 'Weather': 
        weather_variable = Label(frame3, text =f"Weather: {weather}", fg= 'white', bg = "#40aadb",font=bold_font)
        weather_variable.place(x=10,y=10) 

    else:
        weather_variable = Label( text =f"Weather: {weather}", fg= 'white', bg = "#40aadb",font=bold_font)
        weather_variable.place(x=10,y=10)


def set_frames():

    wind_speed, temperature, weather = get_weather_conditions()

    # Set frame 1

    if logged_in_user_choice1 == "Windspeed":
        print("Frame 1 is Windspeed")
        choice_wind_speed(wind_speed)
    elif logged_in_user_choice1 == "Tide":
        print("Frame 1 is Tide")
        choice_tide_time()
    elif logged_in_user_choice1 == "Weather":
        print("Frame 1 is Weather")
        choice_weather(weather)
    elif logged_in_user_choice1 == "Temperature":
        print("Frame 1 is Temperature")
        choice_temperature(temperature)

    # Set frame 2

    if logged_in_user_choice2 == "Windspeed":
        print("Frame 2 is Windspeed")
        choice_wind_speed(wind_speed)
    elif logged_in_user_choice2 == "Tide":
        print("Frame 2 is Tide")
        choice_tide_time()
    elif logged_in_user_choice2 == "Weather":
        print("Frame 2 is Weather")
        choice_weather(weather)
    elif logged_in_user_choice2 == "Temperature":
        print("Frame 2 is Temperature")
        choice_temperature(temperature)

    # Set frame 3

    if logged_in_user_choice3 == "Windspeed":
        print("Frame 3 is Windspeed")
        choice_wind_speed(wind_speed)
    elif logged_in_user_choice3 == "Tide":
        print("Frame 3 is Tide")
        choice_tide_time()
    elif logged_in_user_choice3 == "Weather":
        print("Frame 3 is Weather")
        choice_weather(weather)
    elif logged_in_user_choice3 == "Temperature":
        print("Frame 3 is Temperature")
        choice_temperature(temperature)

set_frames()

'''
wind_speed, temperature, weather = get_weather_conditions()
choice_wind_speed(wind_speed)
choice_tide_time()
choice_temperature(temperature)
#choice_weather(weather)
'''

condition_text = StringVar()
condition_text.set("")

title_label = Label(tkWindow, textvariable=condition_text, font=("Arial", 50))
title_label.place(relx=0.5, y=45, anchor=CENTER)

tkWindow.mainloop()