import requests
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import json


tk_window = tk.Tk()
tk_menubar = tk.Menu(tk_window)
tk_main_frame = tk.Frame(tk_window)
top_frame = tk.Frame(tk_main_frame, name = "top_frame")
bottom_frame = tk.Frame(tk_main_frame, name = "bottom_frame")
tk_left_top_frame = tk.Frame(top_frame)
tk_city_name_entry = tk.Entry(tk_left_top_frame)
button = tk.Button(bottom_frame)
tk_city_entry_label = tk.Label(tk_left_top_frame)
tk_city_entry_button = tk.Button(tk_left_top_frame)
tk_city_results_treeview = ttk.Treeview(tk_left_top_frame)
tk_city_results_scrollbar = ttk.Scrollbar(tk_left_top_frame, orient = tk.VERTICAL, command = tk_city_results_treeview.yview)


colour_scheme_list=[[49,47,49],[91,83,81],[133,155,143],[226,209,167],[235,198,126]]
city_results_dict = []

def graph():

  return

# API functionality

def get_openmeteo_response(lat, lon):
  json_string_result = ""
  json_string_result_temp = ""
  response_openmeteo = requests.get('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&hourly=temperature_2m,relative_humidity_2m,rain,wind_speed_10m' % (lat, lon))
  print(response_openmeteo.status_code)
  for response_openmeteo_item in response_openmeteo:
    # print(response_openmeteo_item)
    json_string_result_temp = str(response_openmeteo_item)
    json_string_result += json_string_result_temp[2:-1]
  json_string_result = json_string_result.replace("\\xc2\\xb0C", "degC")
  print(json_string_result)
  # print(json_string_result)
  # print(json.loads(json_string_result))
  # data = json.loads(str(json_string_result))
  json_string_result = json.loads(json_string_result)
  print(json_string_result)
  for item in json_string_result: #["hourly"]:
      print(str(item) + " : " + str(json_string_result.get(item))) # keyerror????????????? key and list exist
      
  return

def get_location_openweathermap(city_to_find):
  global city_results_dict
  city_results_dict.clear()
  print(city_to_find)
  # {city name},{state code},{country code}
  response_openweathermap = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=5&appid=359c67281e6b54b3ad0545d3b88b02b6' % (city_to_find))
  print(response_openweathermap.status_code)
  # need to make a list and skip the local_names key
  #for result_number in range(6):
    #list(response_openweathermap.json()[result_number])

  for result_number in range(5):
    # print(result_number)
    city_results_dict.append(dict(response_openweathermap.json()[result_number]))
    city_results_dict[result_number].pop("local_names", "not found")
    city_results_dict[result_number]["lat"] = city_results_dict[result_number].pop("lat")
    city_results_dict[result_number]["lon"] = city_results_dict[result_number].pop("lon")
    #for city_item in response_openweathermap.json()[result_number]:
    #list(response_openweathermap.json()[result_number].values()).pop(1)
    #tk_city_results_treeview.insert('', tk.END, values=list(response_openweathermap.json()[result_number].values()))
    tk_city_results_treeview.insert('', tk.END, values=list(city_results_dict[result_number].values()))
  # city_name_typed = input("Type a City from the list: ")
  #for openweathermap_item in response_openweathermap.json():
   # if city_name_typed = openweathermap_item["name"]:
    #  for city_name_item in op
  return


def city_results_treeview_select(event):
  global tk_city_results_treeview
  for selected_item in tk_city_results_treeview.selection():
      item = tk_city_results_treeview.item(selected_item)
      record = item['values']
  # print(','.join(record))
  print(record[3] + "|" + record[4])
  get_openmeteo_response(record[3], record[4])
  return


def post_select_scheme_colormind(colour_scheme):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  data = '{"model":"%s"}' % colour_scheme
  response_scheme_colormind = requests.post('http://colormind.io/api/', headers=headers, data=data)
  if response_scheme_colormind.status_code == requests.codes.ok: #json()["result"] ==  "200":
    global colour_scheme_list
    colour_scheme_list.clear()
    colour_scheme_2d_list = list(map(list, response_scheme_colormind.json()["result"]))
    for colour_scheme_2d_item in colour_scheme_2d_list:
      rgb_colour = bytearray(colour_scheme_2d_item).hex()
      colour_scheme_list.append("#" + rgb_colour)
    print(colour_scheme_list)
    tk_main_frame.config(bg=colour_scheme_list[0])
    top_frame.config(bg=colour_scheme_list[1])
    bottom_frame.config(bg=colour_scheme_list[2])
    tk_left_top_frame.config(bg=colour_scheme_list[3])
    tk_city_name_entry.config(bg=colour_scheme_list[4], fg=colour_scheme_list[0])
    tk_window.update()
  return response_scheme_colormind.status_code


def get_scheme_colormind():
  response_scheme_colormind = requests.get("http://colormind.io/list/")
  if response_scheme_colormind.status_code == requests.codes.ok:
    return response_scheme_colormind.json()["result"]
  else:
    return response_scheme_colormind.status_code

#GUI UTILITY functions

def resize(event):
  for child in event.widget.pack_slaves(): # event.widget.children.values():
    # print("*******" + str(event.widget.winfo_width() - 10) + 
    #       "*******" + str(event.widget.winfo_height()) + "*******")
    new_width = event.widget.winfo_width() - 10
    total_height_used = event.widget.winfo_height()

    # print(str(child))

    if str(child) == ".!frame.top_frame":
      new_height = event.widget.winfo_height() - 10 - 200
      total_height_used -= event.widget.winfo_height() - 10 - 200
    elif str(child) == "!frame.bottom_frame":
       new_height = event.widget.winfo_height() - total_height_used - 10
       
    child.configure(width = new_width, height = new_height)
    
    # print(str(child.winfo_width()) + "x" + str(child.winfo_height()))
  return

# GUI setup here down

tk_window.attributes("-alpha", 0.0)
post_select_scheme_colormind("default")

starting_width = 1200
starting_height = 1024 

screen_width = tk_window.winfo_screenwidth()
screen_height = tk_window.winfo_screenheight()

starting_x = screen_width/2 - starting_width/2
starting_y = screen_height/2 - starting_height/2

tk_window.minsize(width = 800, height = 600)
tk_window.pack_propagate(0)

# center tk_window on screen
tk_window.geometry("%dx%d+%d+%d" % (starting_width, starting_height, starting_x, starting_y))

# menus
tk_colour_scheme_menu = tk.Menu(tk_menubar, tearoff=0)

scheme_repsonse = get_scheme_colormind()
if type(scheme_repsonse) is not int:
  for scheme_item in scheme_repsonse:
    tk_colour_scheme_menu.add_command(label=scheme_item, command=lambda: post_select_scheme_colormind(scheme_item))

tk_colour_scheme_menu.add_separator()
tk_colour_scheme_menu.add_command(label="Exit", command=tk_window.quit)
tk_menubar.add_cascade(label="Colour Scheme", menu=tk_colour_scheme_menu)

tk_main_frame.config(bg=colour_scheme_list[0])
tk_main_frame.pack(fill = "both", expand = True)
# tk_main_frame.pack_propagate(0)

tk_main_frame.bind("<Configure>", resize)
tk_main_frame.update()

top_frame.config(bg=colour_scheme_list[1])
top_frame.pack(padx = 5, pady = 5)
top_frame.pack_propagate(0)
top_frame.configure(width = tk_main_frame.winfo_width() - 10, height = tk_main_frame.winfo_height() - 210)

tk_left_top_frame.pack(side = "left", padx = 5, pady = 5, fill="y")

tk_city_entry_label.config(text = "Enter a city name")
tk_city_entry_label.grid(row=0, column=0)

tk_city_name_entry.config(width = 30, bg=colour_scheme_list[3], fg=colour_scheme_list[1], font=('times', 16, 'bold'))
tk_city_name_entry.grid(row=0, column=1)

tk_city_entry_button.config(text = "Get Location", padx = 10, command=lambda: get_location_openweathermap(tk_city_name_entry.get()))
tk_city_entry_button.grid(row=1, column=1, sticky="E")

tk_city_results_treeview.config(columns=('City', 'Country', 'State', 'Latitude', 'Longitude'), show='headings')
tk_city_results_treeview.heading('City', text='City')
tk_city_results_treeview.column('City', width = 30)
tk_city_results_treeview.heading('Country', text='Country')
tk_city_results_treeview.column('Country', width = 30)
tk_city_results_treeview.heading('State', text='State')
tk_city_results_treeview.column('State', width = 30)
tk_city_results_treeview.heading('Longitude', text='Longitude')
tk_city_results_treeview.column('Longitude', width = 30)
tk_city_results_treeview.heading('Latitude', text='Latitude')
tk_city_results_treeview.column('Latitude', width = 30)
tk_city_results_treeview.bind('<<TreeviewSelect>>', city_results_treeview_select)
tk_city_results_treeview.grid(row = 2, column = 0, sticky='nsew', columnspan = 6)

tk_city_results_treeview.config(yscroll = tk_city_results_scrollbar.set)
tk_city_results_scrollbar.grid(row = 2, column = 6, sticky = 'ns')

tk_main_frame.update()

bottom_frame.config(bg=colour_scheme_list[2])
bottom_frame.pack(padx = 5, pady = 5)
bottom_frame.pack_propagate(0)
bottom_frame.configure(width = tk_main_frame.winfo_width() - 10, 
                       height = tk_main_frame.winfo_height() - top_frame.winfo_height() - 10)

tk_main_frame.update()

button.config(bg='grey', text = "+", font=('times', 24, 'bold'))
# button.bind('<Motion>',motion)
button.pack(side = "left")

tk_window.update()

tk_window.config(menu=tk_menubar)
tk_window.attributes("-alpha", 1.0)
tk_window.mainloop()

#new plan ... the plan

# get city by name
# select from list
# use weather data by city lat lon for charts
