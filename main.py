import requests
import tkinter as tk

response = requests.get("https://networkcalc.com/api/ip/10.5.1.0/28,10.5.1.129/27?binary=false")

print(response.status_code)

print(response.json()["status"])

##print(response.json()["address"][0])
for array_item in response.json()["address"]:
    for subarray_key, subarray_item in array_item.items():
        print(subarray_key, " \t:\t", subarray_item)

##print(response.json()["address"][1])

##  24 |  25 |  26 |  27 |  28 |  29 |  30 |  31 |  32 |
## 256 | 128 |  64 |  32 |  16 |   8 |   4 |   2 |   1 |
##enter starting ip address
##validate using api response code
##enter number of hosts in network
##calculate subnet cidr notation
        
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

tk_window = tk.Tk()
tk_window.attributes("-alpha", 0.0)

starting_width = 1200
starting_height = 1024 

screen_width = tk_window.winfo_screenwidth()
screen_height = tk_window.winfo_screenheight()

starting_x = screen_width/2 - starting_width/2
starting_y = screen_height/2 - starting_height/2

tk_window.minsize(width = 800, height = 600)
tk_window.pack_propagate(0)

#center tk_window on screen
tk_window.geometry("%dx%d+%d+%d" % (starting_width, starting_height, starting_x, starting_y))

tk_main_frame = tk.Frame(tk_window, bg="yellow")
tk_main_frame.pack(fill = "both", expand = True)
# tk_main_frame.pack_propagate(0)

tk_main_frame.bind("<Configure>", resize)
tk_main_frame.update()

top_frame = tk.Frame(tk_main_frame, bg="blue", name = "top_frame")
top_frame.pack(padx = 5, pady = 5)
top_frame.pack_propagate(0)
top_frame.configure(width = tk_main_frame.winfo_width() - 10, height = tk_main_frame.winfo_height()- 210)

tk_main_frame.update()

bottom_frame = tk.Frame(tk_main_frame, bg="red", name = "bottom_frame")
bottom_frame.pack(padx = 5, pady = 5)
bottom_frame.pack_propagate(0)
bottom_frame.configure(width = tk_main_frame.winfo_width() - 10, 
                       height = tk_main_frame.winfo_height() - top_frame.winfo_height() - 10)

tk_main_frame.update()

button = tk.Button(bottom_frame, text = "+")
button.config(bg='grey', font=('times', 24, 'bold'))
# button.bind('<Motion>',motion)
button.pack(side = "left")

tk_window.update()
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
