import requests
import tkinter as tk

response_networkcalc = requests.get("https://networkcalc.com/api/ip/10.5.1.0/28,10.5.1.129/27?binary=false")
print(response_networkcalc.status_code)
print(response_networkcalc.json()["status"])
# print(response.json()["address"][0])
# for networkcalc_item in response_networkcalc.json()["address"]:
#    for sub_networkcalc_key, sub_networkcalc_item in networkcalc_item.items():
#        print(sub_networkcalc_key, " \t:\t", sub_networkcalc_item)

# print(response.json()["address"][1])

# #  24 |  25 |  26 |  27 |  28 |  29 |  30 |  31 |  32 |
# # 256 | 128 |  64 |  32 |  16 |   8 |   4 |   2 |   1 |
# #enter starting ip address
# #validate using api response code
# #enter number of hosts in network
# #calculate subnet cidr notation

tk_window = tk.Tk()
tk_menubar = tk.Menu(tk_window)
tk_main_frame = tk.Frame(tk_window)
top_frame = tk.Frame(tk_main_frame, name = "top_frame")
bottom_frame = tk.Frame(tk_main_frame, name = "bottom_frame")
button = tk.Button(bottom_frame)
colour_scheme_list=[[49,47,49],[91,83,81],[133,155,143],[226,209,167],[235,198,126]]

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
      # for sub_c_s_2d_item in colour_scheme_2d_item:
        # rgb_colour += "%x" % sub_c_s_2d_item
      
      colour_scheme_list.append("#" + rgb_colour)
    print(colour_scheme_list)
    global tk_window, tk_menubar, tk_main_frame, top_frame, bottom_frame
    tk_main_frame.config(bg=colour_scheme_list[0])
    top_frame.config(bg=colour_scheme_list[1])
    bottom_frame.config(bg=colour_scheme_list[2])
    tk_window.update()
    # tk_main_frame.update()
    # top_frame.update()
    # bottom_frame.update()
    # for scheme_item in colour_scheme_list:
    #   print(scheme_item)
  return response_scheme_colormind.status_code


def get_scheme_colormind():
  response_scheme_colormind = requests.get("http://colormind.io/list/")
  if response_scheme_colormind.status_code == requests.codes.ok:
    return response_scheme_colormind.json()["result"]
  else:
    return response_scheme_colormind.status_code

        
def motion(event):
  print("Mouse position: (%s %s)" % (event.x, event.y))
  return


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
top_frame.configure(width = tk_main_frame.winfo_width() - 10, height = tk_main_frame.winfo_height()- 210)

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

# the plan

# allow buttons to be added to the top frame from the bottom frame
# # add computer / computer group
# # add switch
# # add router
# # add straight through
# # add crossover
# # add coaxial
# # add fibre
# # not sure about how wireless fits in atm

# buttons access a toplevel window
# hidden details must be stored / saved to a file
# toplevel windows are stats windows for network interfaces created from 
# - required hosts and ip address start
# default gateway also will be required to be set if router is to another network
# try to simulate ping
# attempt routing commands
