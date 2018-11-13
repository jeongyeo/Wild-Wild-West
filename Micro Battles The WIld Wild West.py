from tkinter import *
from time import *
from math import *
from random import *

root = Tk()
root.title("Micro Battles: The Wild Wild West")

# Check screen resolution
srSetting = open("srSetting.txt", "r")
data = srSetting.readlines()
srSetting.close()
srSetting = open("srSetting.txt", "w")
for line in data:
    words = line.split()
    if words[3] == "True":
        width = words[0]
        height = words[2]
    else:
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
    
    sr_value = str(width) + " x " + str(height) + " False"
    srSetting.write(sr_value)
srSetting.close()

# Set screen resolution
try:
    width = int(width)
    height = int(height)
    
except:
    # If file is currupt, change to defalt resolution
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    with open("srSetting.txt", "w") as srSetting:
        sr_value = str(width) + " x " + str(height) + " False"
        srSetting.write(sr_value)

screen = Canvas(root, width = width, height = height, background = "peru")
screen.pack()

# PhotoImage
# Button Image
volOn = PhotoImage(file = "photos/Volume Up.gif")
volOff = PhotoImage(file = "photos/Volume Mute.gif")
keyboard = PhotoImage(file = "photos/Key.gif")
moniter = PhotoImage(file = "photos/Moniter.gif")
leave = PhotoImage(file = "photos/Leave.gif")

# Player and bullet Image
b_bullet_img = PhotoImage(file = "photos/blue bullet.gif")
b_gun_img = PhotoImage(file = "photos/blue with gun.gif")
b_nogun_img = PhotoImage(file = "photos/blue without gun.gif")
r_bullet_img = PhotoImage(file = "photos/red bullet.gif")
r_gun_img = PhotoImage(file = "photos/red with gun.gif")
r_nogun_img = PhotoImage(file = "photos/red without gun.gif")

# Obstacle Image
barrel_img = PhotoImage(file = "photos/slow down barrel.gif")
cactus_img = PhotoImage(file = "photos/cactus.gif")

# Fullscreen State
fState = False
# transition state
transitionState = False
# play
playState = False

fullscreen_label_y = -5

def fullscreen():
    global fState
    if fsButton["text"] == "Enter Full Screen":
        fsButton["text"] = "Exit Full Screen"
        fState = True
        root.attributes("-fullscreen", fState)
    else:
        fsButton["text"] = "Enter Full Screen"
        fState = False
        root.attributes("-fullscreen", fState)

##def fullscreen_label():
##    global fullscreen_label_y
##    if fState:
##        if mouse_motion_y < height*0.01:
##            if fullscreen_label_y == 50:
##                pass
##            else:
##                fullscreen_label_y += 5
##        else:
##            if fullscreen_label_y == -10:
##                pass
##            else:
##                fullscreen_label_y += -5
##                
##        fullscreen_label_text = screen.create_text(width*0.5, fullscreen_label_y , text = "Press 'F11' to exit fullscreen", font = "Comic 20", anchor = CENTER)

# Binding
def binding():
    global r_player_key, b_player_key, playState
    screen.bind("<Escape>", lambda event: root.destroy())
    screen.bind("<F11>", lambda event: fullscreen())
    screen.bind( "<Motion>", mouse_motion)
    screen.bind("<Button-1>", mouse_click)
    r_player_key = "Return"
    b_player_key = "space"
    screen.bind("<Key>", key_down_handler)
        
def mouse_click(event):
    global mouse_click_x, mouse_click_y, transitionState
    mouse_click_x = event.x
    mouse_click_y = event.y
    if mouse_click_x > width*0.4 and mouse_click_x < width*0.6 and mouse_click_y > height*0.15 and mouse_click_y < height*0.25:
        transitionState = True
        transition()
        
def mouse_motion(event):
    global mouse_motion_x, mouse_motion_y
    mouse_motion_x = event.x
    mouse_motion_y = event.y

def key_down_handler(event):
    if playState:
        if event.keysym == r_player_key:
            r_bulletSpawn()
            
        elif event.keysym == b_player_key:
            b_bulletSpawn()
            
# Button
def mainButtons():
    global fsButton, ruleButton, sButton
    # Fullscreen Button
    fsButton = Button(screen, bg = "khaki", text = "Enter Full Screen", font = "10",  command = fullscreen)
    screen.create_window(width*0.975, height*0.06, window = fsButton, anchor = E)

    # Rule Button
    ruleButton = Button(screen, bg = "khaki", text = "Enter Rules", font = "10", command = rule, state = NORMAL)
    screen.create_window(width*0.975, height*0.125, window = ruleButton, anchor = E)

    # Settings Button
    sButton  = Button(screen, bg = "khaki", text = "Enter Settings", font = "10", command = settings, state = NORMAL)
    screen.create_window(width*0.975, height*0.19, window = sButton, anchor = E)

def rule():
    global rState, rule_object_1, rule_object_2, rule_object_3, rule_object_4
    fontsize = "Comic", int(width/70)
    # Change text, create objects and disable settings button
    if ruleButton["text"] == "Enter Rules":
        ruleButton["text"] = "Exit Rules"
        sButton.configure(state = DISABLED)
        # Objects
        rule_object_1 = screen.create_rectangle(width*0.25, height*0.35, width*0.75, height*0.65, fill = "khaki", outline = "goldenrod", width = 5)
        rule_object_2 = screen.create_text(width*0.5, height*0.38, text = "Rules", font = fontsize)  
        rule_object_3 = screen.create_text(width*0.5, height*0.47, text="Shoot and hit the opponent to \ngain points. Player who reaches \n5 points first wins.", font = fontsize)
        rule_object_4 = screen.create_text(width*0.5, height*0.585, text=("Red Player Shoot: " + r_player_key + "\n Blue Player Shoot: " + b_player_key), font = fontsize)
    else:
        ruleButton["text"] = "Enter Rules"
        sButton.configure(state = NORMAL)
        screen.delete(rule_object_1, rule_object_2, rule_object_3, rule_object_4)

def settings():
    global settings_box
    fontsize = "Comic", int(width/50)
    # Change text and run settings_buttons
    if sButton["text"] == "Enter Settings":
        sButton["text"] = "Exit Settings"
        ruleButton.configure(state = DISABLED)
        settings_buttons()
        settings_box = screen.create_rectangle(width*0.25, height*0.35, width*0.75, height*0.65, fill = "khaki", outline = "goldenrod", width = 5)
    else:
        # Change text and destroy buttons
        sButton["text"] = "Enter Settings"
        ruleButton.configure(state = NORMAL)
        screen.delete(settings_box)
        kButton.destroy()
        srButton.destroy()
        exitButton.destroy()
   
def settings_buttons():
    global kButton, srButton, exitButton
    fontsize = "Comic", int(width/70)

    # Key Binding Button
    kButton = Button(screen, bg = "khaki", text = "Key Binding", command = key1, font = fontsize, image = keyboard, compound=LEFT)
    screen.create_window(width*0.375, height*0.55, window = kButton)

    # Screen Resolution Button
    srButton = Button(screen, bg = "khaki", text = "Screen Resolution", command = sr, font = fontsize, image = moniter, compound=LEFT)
    screen.create_window(width*0.5, height*0.45, window = srButton)

    # Exit Game Button
    exitButton = Button(screen, bg = "khaki", text = "Exit Game", command = lambda: root.destroy(), font = fontsize, image = leave, compound=LEFT)
    screen.create_window(width*0.625, height*0.55, window = exitButton)


def key1():
    global top1, key_label1, key_okButton1
    top1 = Toplevel()
    # Set focus
    top1.focus_force()
    top1.grab_set()
    # Objects
    Label(top1, text = "Press the desired key for Red Player\n then press 'OK'\nNew key binding cannot be 'F11' or 'ESC'").pack()
    key_label1 = Label(top1, text = "Your current key for Red Player is: " + r_player_key).pack()
    key_okButton1 = Button(top1, text = "OK", command = key2)
    key_okButton1.pack()
    top1.bind( "<Key>",  keyDetect1)

def key2():
    global top2, key_label2, key_okButton2
    # Destroys previous box
    top1.destroy()
    # Set focus to new box
    top2 = Toplevel()
    top2.focus_force()
    top2.grab_set()
    # Objects
    Label(top2, text = "Press the desired key for Blue Player\n then press 'OK'\nNew key binding cannot be 'F11' or 'ESC'").pack()
    key_label2 = Label(top2, text = "Your current key for Blue Player is: " + b_player_key).pack()
    key_okButton2 = Button(top2, text = "OK", command = top2.destroy)
    key_okButton2.pack()
    top2.bind( "<Key>",  keyDetect2)

def keyDetect1(event):
    global r_player_key
    # Detects new key binded by user. If already binded to the other player, raises error.
    keyPressed = event.keysym
    if b_player_key == keyPressed:
        errorMsg = Message(top1, text="That key is already assigned to something else! Choose another key", fg="red")
        # Error Sound
        winsound.PlaySound(winsound.SND_ASYNC)
        top1.after(1000, errorMsg.destroy)
        key_okButton1.configure(state = DISABLED)
        errorMsg.pack()
        key_okButton1.pack()
    else:
        key_okButton1.configure(state = NORMAL)
        key_okButton1.pack()
        r_player_key = keyPressed

def keyDetect2(event):
    global b_player_key
    # Detects new key binded by user. If already binded to the other player, raises error.
    keyPressed = event.keysym
    if r_player_key == keyPressed:
        errorMsg = Message(top2, text = "That key is already assigned to something else! Choose another key", fg="red")
        # Error Sound
        winsound.PlaySound(winsound.SND_ASYNC)
        top2.after(1000, errorMsg.destroy)
        key_okButton2.configure(state = DISABLED)
        errorMsg.pack()
        key_okButton2.pack()
    else:
        key_okButton2.configure(state = NORMAL)
        key_okButton2.pack()
        b_player_key = keyPressed

def sr():
    global top3, sr_ok_Button
    srList = ["1366 x 768", "1280 x 1024", "1280 x 800"]
    top3 = Toplevel()
    top3.focus_force()
    top3.grab_set()
    # Objects
    sr_label = Label(top3, text = "Set your screen resolution and press 'OK'").pack()
    # Option Menu
    sr_var = StringVar(top3)
    sr_var.set("Select a resolution")
    OptionMenu(top3, sr_var, *srList, command = srDetect).pack()
    Label(top3, fg = "red", text = "Please restart the program.\n Pressing 'OK' will exit the program").pack()
    sr_ok_Button = Button(top3, text="Ok", command = srChange)
    sr_cancel_button = Button(top3, text = "Cancel", command = srChangeCancel)
    sr_ok_Button.pack()
    sr_cancel_button.pack()
    
def srDetect(event):
    global sr_value
    # grabs selected value from sr()
    sr_value = event + " True"

def srChangeCancel():
    global sr_ok_Button, sr_cancel_button
    with open("srSetting.txt", "w") as srSetting:
        sr_value = str(width) + " x " + str(height) + " False"
        srSetting.write(sr_value)
    top3.destroy()

def srChange():
    with open("srSetting.txt", "w") as srSetting:
        srSetting.write(sr_value)
    root.destroy()

def transition_update():
    global transition_i, transitionState, playState
    transition_door(width*0.25*-cos(0.025*transition_i), width*0.25*cos(0.025*transition_i))
    if transition_i < 252:
        transition_i += 1
    elif transition_i == 252:
        transition_i = 0
        
def transition():
    ruleButton.configure(state = DISABLED)
    sButton.configure(state = DISABLED)
    if ruleButton["text"] == "Exit Rules":
        ruleButton["text"] = "Enter Rules"
        screen.delete(rule_object_1, rule_object_2, rule_object_3, rule_object_4)
    elif sButton["text"] == "Exit Settings":
        sButton["text"] = "Enter Settings"
        screen.delete(settings_box)
        kButton.destroy()
        srButton.destroy()
        exitButton.destroy()

def transition_door(xValue1, xValue2):
    global door1_array_object,door2_array_object
    global door1_2, door1_3, door1_4, door1_5, door1_6, door1_7, door1_8
    global door2_2, door2_3, door2_4, door2_5, door2_6, door2_7, door2_8
    door2_array_object = []
    door1_array_object = []
    half = width*0.25
    for i in range(0, 8):
        door1_array_object.append(screen.create_rectangle(width*0.0625*i+xValue1-half, 0, width*0.0625*(i+1)+xValue1-half, height, fill = "#966F33"))
    door1_2 = screen.create_rectangle(width*0.05+xValue1-half, height*0.45, width*0.45+xValue1-half, height*0.55, fill = "#b69b4c")  
    door1_3 = screen.create_polygon(width*0.05+xValue1-half, height*0.9, width*0.1+xValue1-half, height*0.9, width*0.45+xValue1-half, height*0.55, width*0.4+xValue1-half, height*0.55, fill = "#b69b4c", outline = "black")
    door1_4 = screen.create_polygon(width*0.05+xValue1-half, height*0.1, width*0.1+xValue1-half, height*0.1, width*0.45+xValue1-half, height*0.45, width*0.4+xValue1-half, height*0.45, fill = "#b69b4c", outline = "black")
    door1_5 = screen.create_rectangle(0+xValue1-half, 0, width*0.5+xValue1-half, height*0.1, fill = "#825201")
    door1_6 = screen.create_rectangle(0+xValue1-half, height*0.9, width*0.5+xValue1-half, height, fill = "#825201")
    door1_7 = screen.create_rectangle(0+xValue1-half, 0, width*0.05+xValue1-half, height, fill = "#825201")
    door1_8 = screen.create_rectangle(width*0.45+xValue1-half, 0, width*0.5+xValue1-half, height, fill = "#825201")
    for i in range(0, 8):
        door2_array_object.append(screen.create_rectangle((width*0.5)+width*0.0625*i+xValue2+half, 0, (width*0.5)+width*0.0625*(i+1)+xValue2+half, height, fill = "#966F33"))
    door2_2 = screen.create_rectangle(width*0.95+xValue2+half, height*0.45, width*0.55+xValue2+half, height*0.55, fill = "#b69b4c")  
    door2_3 = screen.create_polygon(width*0.95+xValue2+half, height*0.9, width*0.9+xValue2+half, height*0.9, width*0.55+xValue2+half, height*0.55, width*0.6+xValue2+half, height*0.55, fill = "#b69b4c", outline = "black")
    door2_4 = screen.create_polygon(width*0.95+xValue2+half, height*0.1, width*0.9+xValue2+half, height*0.1, width*0.55+xValue2+half, height*0.45, width*0.6+xValue2+half, height*0.45, fill = "#b69b4c", outline = "black")
    door2_5 = screen.create_rectangle(width+xValue2+half, 0, width*0.5+xValue2+half, height*0.1, fill = "#825201")
    door2_6 = screen.create_rectangle(width+xValue2+half, height*0.9, width*0.5+xValue2+half, height, fill = "#825201")
    door2_7 = screen.create_rectangle(width+xValue2+half, 0, width*0.95+xValue2+half, height, fill = "#825201")
    door2_8 = screen.create_rectangle(width*0.55+xValue2+half, 0, width*0.5+xValue2+half, height, fill = "#825201")

def transition_door_delete():
    for i in range(0, 8):
        screen.delete(door2_array_object[i])
        screen.delete(door1_array_object[i])
    screen.delete(door1_2, door1_3, door1_4, door1_5, door1_6, door1_7, door1_8)
    screen.delete(door2_2, door2_3, door2_4, door2_5, door2_6, door2_7, door2_8)
    
def menu_delete():
    screen.delete(play_button_box, play_button_text, menu_title_box, menu_title)
    screen.delete(r_winCount_text, b_winCount_text)

def drawTitle():
    global play_button_box, play_button_text, menu_blue_with_gun, menu_red_with_gun, menu_title_box, menu_title
    global r_winCount, b_winCount, r_winCount_text, b_winCount_text
    fontsize = "Comic", int(width/37)
    play_button_box = screen.create_rectangle(width*0.4, height*0.15, width*0.6, height*0.25, fill = "khaki", outline = "goldenrod", width = 5)
    play_button_text = screen.create_text(width*0.5, height*0.2, text = "Play", fill = "forest green", font = fontsize)
    menu_blue_with_gun = screen.create_image(width*0.15, height*0.5, image = b_gun_img)
    menu_red_with_gun = screen.create_image(width*0.85, height*0.5, image = r_gun_img)
    menu_title_box = screen.create_rectangle(width*0.25, height*0.45, width*0.75, height*0.55, fill = "khaki", outline = "goldenrod", width = 5)
    menu_title = screen.create_text(width*0.5, height*0.5, text = "Micro Battles: Wild Wild West", font = fontsize, fill = "forest green")

    r_winCount_text = screen.create_text(width*0.75, height*0.9, text = r_winCount, font = "Comic 50", fill = "white")
    b_winCount_text = screen.create_text(width*0.25, height*0.9, text = b_winCount, font = "Comic 50", fill = "white")

def drawBackground():
    # 3 boarders
    screen.create_rectangle(-5, -5, width*0.1, height*0.825, fill="#7f644b", outline = "white", width = 5)
    screen.create_rectangle(width*0.9, -5, width+5, height*0.825, fill="#7f644b", outline = "white", width = 5)
    screen.create_rectangle(-5, height*0.825, width+5, height+5, fill = "gray40", outline = "white", width = 10)

    # Top wall decoration
    screen.create_rectangle(width*0.2, 0, width*0.8, 25, fill = "#e0b181", outline = "#b08652", width = 5)
    screen.create_line(width*0.2, 12.5, width*0.8, 12.5, width = 4, fill = "#b08652") 
    screen.create_rectangle(width*0.1825, 0, width*0.2175, 50, fill = "#e0b181", outline = "#b08652", width = 5)
    screen.create_rectangle(width*0.19, 0, width*0.21, 35, fill = "#e0b181", outline = "#b08652", width = 4)
    screen.create_rectangle(width*0.194575, 0, width*0.20525, 25, fill = "#e0b181", outline = "#b08652", width = 3)
    screen.create_rectangle(width*0.3825, 0, width*0.4175, 50, fill = "#e0b181", outline = "#b08652", width = 5)
    screen.create_rectangle(width*0.39, 0, width*0.41, 35, fill = "#e0b181", outline = "#b08652", width = 4)
    screen.create_rectangle(width*0.394575, 0, width*0.40525, 25, fill = "#e0b181", outline = "#b08652", width = 3)
    screen.create_rectangle(width*0.5825, 0, width*0.6175, 50, fill = "#e0b181", outline = "#b08652", width = 5)
    screen.create_rectangle(width*0.59, 0, width*0.61, 35, fill = "#e0b181", outline = "#b08652", width = 4)
    screen.create_rectangle(width*0.594575, 0, width*0.60525, 25, fill = "#e0b181", outline = "#b08652", width = 3)
    screen.create_rectangle(width*0.7825, 0, width*0.8175, 50, fill = "#e0b181", outline = "#b08652", width = 5)
    screen.create_rectangle(width*0.79, 0, width*0.81, 35, fill = "#e0b181", outline = "#b08652", width = 4)
    screen.create_rectangle(width*0.794575, 0, width*0.80525, 25, fill = "#e0b181", outline = "#b08652", width = 3)

# Players
def player_location_update():
    global ySpeed1, yStart1, t1, ySpeed2, yStart2, t2
    global r_player_y, b_player_y
    t1 += 5
    t2 += 5
    
    b_player_y = ySpeed1 * t1 + yStart1
    r_player_y = ySpeed2 * t2 + yStart2

    # Reverse the ySpeed if player hits top or bottom
    if r_player_y >= height*0.778:
        t2 = 5
        yStart2 = r_player_y
        ySpeed2 = -1*ySpeed2

    elif r_player_y <= height*0.15:
        t2 = 5
        yStart2 = r_player_y
        ySpeed2 = -1*ySpeed2
        
    if b_player_y >= height*0.778:
        t1 = 5
        yStart1 = b_player_y
        ySpeed1 = -1*ySpeed1

    elif b_player_y <= height*0.15:
        t1 = 5
        yStart1 = b_player_y
        ySpeed1 = -1*ySpeed1

    check_if_hit()
    
def check_if_hit():
    global r_score, b_score
    r_i = 0
    b_i = 0
    # dist1 = distance between bullet and enemy
    # dist2 = distance between bullet and yourself, since your own bullet can hit yourself
    # check bullet distance and delete the bullet and array values if hit.
    while r_i < len(r_bullet):
        r_dist1 = sqrt((r_xBullet[r_i] - width*0.15)**2 + (r_yBullet[r_i] - b_player_y)**2)
        r_dist2 = sqrt((r_xBullet[r_i] - width*0.85)**2 + (r_yBullet[r_i] - r_player_y)**2)
        if r_dist1 <= 50:
            r_xBullet.pop(r_i)
            r_yBullet.pop(r_i)
            r_bullet.pop(r_i)
            r_xSpeed.pop(r_i)
            r_ySpeed.pop(r_i)
            r_score += 1
        elif r_dist2 <= 50:
            r_xBullet.pop(r_i)
            r_yBullet.pop(r_i)
            r_bullet.pop(r_i)
            r_xSpeed.pop(r_i)
            r_ySpeed.pop(r_i)
            b_score += 1          
        else:
            r_i += 1
            
    while b_i < len(b_bullet):
        b_dist1 = sqrt((b_xBullet[b_i] - width*0.85)**2 + (b_yBullet[b_i] - r_player_y)**2)
        b_dist2 = sqrt((b_xBullet[b_i] - width*0.15)**2 + (b_yBullet[b_i] - b_player_y)**2)
        if b_dist1 <= 50:
            b_xBullet.pop(b_i)
            b_yBullet.pop(b_i)
            b_bullet.pop(b_i)
            b_xSpeed.pop(b_i)
            b_ySpeed.pop(b_i)
            b_score += 1
        elif b_dist2 <= 50:
            b_xBullet.pop(b_i)
            b_yBullet.pop(b_i)
            b_bullet.pop(b_i)
            b_xSpeed.pop(b_i)
            b_ySpeed.pop(b_i)
            r_score += 1
        else:
            b_i += 1

def draw_player():
    global r_player, b_player
    # Change the player image depending on if he has a bullet reloaded or not
    if r_player_bullet_state:
        r_player = screen.create_image(width*0.85, r_player_y, image = r_gun_img)
    else:
        r_player = screen.create_image(width*0.85, r_player_y, image = r_nogun_img)

    if b_player_bullet_state:
        b_player = screen.create_image(width*0.15, b_player_y, image = b_gun_img)
    else:
        b_player = screen.create_image(width*0.15, b_player_y, image = b_nogun_img)

# Bullets  
def r_bulletSpawn():
    global r_player_bullet_state
    global t2, tStart2, ySpeed2, r_player_y, yStart2
    # If he has a bullet, shoot
    # Append values to array
    if r_player_bullet_state:
        r_bullet.append(0)
        r_xBullet.append(width*0.81)
        r_yBullet.append(r_player_y)
        r_xSpeed.append(-30)
        r_ySpeed.append(0)
        r_player_bullet_state = False
    # If pressed with no bulet, reverse the direction of player
    else:
        yStart2 = ySpeed2 * t2 + yStart2
        ySpeed2 = -1*ySpeed2
        t2 = 0
        
def r_bullet_update():
    for i in range(0, len(r_xBullet)):
        # Calculate bullet location
        r_xBullet[i] = r_xBullet[i] + r_xSpeed[i]
        r_yBullet[i] = r_yBullet[i] + r_ySpeed[i]
        # If it hits top or bottom wall, deflect it
        if r_yBullet[i] > height*0.778:
            r_ySpeed[i] = r_ySpeed[i] * -1
        elif r_yBullet[i] < height*0.1:
            r_ySpeed[i] = r_ySpeed[i] * -1

    # Delete bullets off screen from array
    r_bullet_offscreen()
    r_check_if_bullet_hit_barrel()
    r_check_if_bullet_hit_cactus()
    
def r_bullet_offscreen():
    # If bullet goes offscreen, delete array values and image
    i = 0
    while i < len(r_xBullet):
        if r_xBullet[i] < width*0.1 or r_xBullet[i] > width*0.9:
            r_xBullet.pop(i)
            r_yBullet.pop(i)
            r_bullet.pop(i)
            r_xSpeed.pop(i)
            r_ySpeed.pop(i)
        else:
            i += 1
            
def draw_r_bullet():
    for i in range(0, len(r_xBullet)):
        if r_xSpeed[0] < 0:
            r_bullet[i] = screen.create_image(r_xBullet[i], r_yBullet[i], image = r_bullet_img)
        else:
            r_bullet[i] = screen.create_image(r_xBullet[i], r_yBullet[i], image = b_bullet_img)

def delete_r_bullet():
    for i in range(0, len(r_xBullet)):
        screen.delete(r_bullet[i])
        
def b_bulletSpawn():
    global b_player_bullet_state
    global t1, tStart1, ySpeed1, b_player_y, yStart1
    if b_player_bullet_state:
        b_bullet.append(0)
        b_xBullet.append(width*0.19)
        b_yBullet.append(b_player_y)
        b_xSpeed.append(30)
        b_ySpeed.append(0)
        b_player_bullet_state = False
    else:
        yStart1 = ySpeed1 * t1 + yStart1
        ySpeed1 = -1*ySpeed1
        t1 = 0

def b_bullet_update():
    for i in range(0, len(b_xBullet)):
        b_xBullet[i] = b_xBullet[i] + b_xSpeed[i]
        b_yBullet[i] = b_yBullet[i] + b_ySpeed[i]
        if b_yBullet[i] > height*0.778:
            b_ySpeed[i] = b_ySpeed[i] * -1
        elif b_yBullet[i] < height*0.1:
            b_ySpeed[i] = b_ySpeed[i] * -1

    b_bullet_offscreen()
    b_check_if_bullet_hit_barrel()
    b_check_if_bullet_hit_cactus()
    
def b_bullet_offscreen():
    i = 0
    while i < len(b_xBullet):
        if b_xBullet[i] > width*0.9 or b_xBullet[i] < width*0.1:
            b_xBullet.pop(i)
            b_yBullet.pop(i)
            b_bullet.pop(i)
            b_xSpeed.pop(i)
            b_ySpeed.pop(i)
        else:
            i += 1
            
def draw_b_bullet():
    for i in range(0, len(b_xBullet)):
        if b_xSpeed[0] > 0:
            b_bullet[i] = screen.create_image(b_xBullet[i], b_yBullet[i], image = b_bullet_img)
        else:
            b_bullet[i] = screen.create_image(b_xBullet[i], b_yBullet[i], image = r_bullet_img)

def delete_b_bullet():
    for i in range(0, len(b_xBullet)):
        screen.delete(b_bullet[i])

# Score Boards
def scoreboard():
    global r_score_text, b_score_text
    r_score_text = screen.create_text(width*0.75, height*0.9, text = r_score, font = "Comic 50", fill = "white")
    b_score_text = screen.create_text(width*0.25, height*0.9, text = b_score, font = "Comic 50", fill = "white")

def delete_scoreboard():
    screen.delete(r_score_text, b_score_text)

# Barrel and Cactus
def spawnBarrel():
    maxWidth = int(width*0.25)
    minWidth = int(width*0.75)
    maxHeight = int(height*0.075)
    minHeight = int(height*0.775)
    rand_xBarrel = randint(maxWidth, minWidth)
    rand_yBarrel = randint(maxHeight, minHeight)

# Check if random value lies ontop of existing value, retry
# Check's Barrel to Barrel, then Barrel to Cactus
    if len(barrel) > 0:
        while True:
            i_pass = True
            for i in range(0, len(barrel)):
                dist1 = sqrt((xBarrel[i] - rand_xBarrel)**2 + (yBarrel[i] - rand_yBarrel)**2)
                if dist1 < 100:
                    rand_xBarrel = randint(maxWidth, minWidth)
                    rand_yBarrel = randint(maxHeight, minHeight)
                    i_pass = False
                    break
            
            if i_pass == True:    
                for i in range(0, len(cactus)):
                    dist2 = sqrt((xCactus[i] - rand_xBarrel)**2 + (yCactus[i] - rand_yBarrel)**2)
                    if dist2 < 100:
                        rand_xBarrel = randint(maxWidth, minWidth)
                        rand_yBarrel = randint(maxHeight, minHeight)
                        break
                else:
                    break

    # Appends value that doesn't overlap other objects
    xBarrel.append(rand_xBarrel)
    yBarrel.append(rand_yBarrel)
    barrel.append(screen.create_image(rand_xBarrel, rand_yBarrel, image = barrel_img))

def spawnCactus():
    maxWidth = int(width*0.25)
    minWidth = int(width*0.75)
    maxHeight = int(height*0.075)
    minHeight = int(height*0.775)
    rand_xCactus = randint(maxWidth, minWidth)
    rand_yCactus = randint(maxHeight, minHeight)
    if len(cactus) > 0:
        while True:
            i_pass = True
            for i in range(0, len(cactus)):
                dist1 = sqrt((xCactus[i] - rand_xCactus)**2 + (yCactus[i] - rand_yCactus)**2)
                if dist1 < 100:
                    rand_xCactus = randint(maxWidth, minWidth)
                    rand_yCactus = randint(maxHeight, minHeight)
                    i_pass = False
                    break                 
                
            if i_pass == True:    
                for i in range(0, len(barrel)):
                    dist2 = sqrt((xBarrel[i] - rand_xCactus)**2 + (yBarrel[i] - rand_yCactus)**2)
                    if dist2 < 100:
                        rand_xCactus = randint(maxWidth, minWidth)
                        rand_yCactus = randint(maxHeight, minHeight)
                        break
                else:
                    break

    xCactus.append(rand_xCactus)
    yCactus.append(rand_yCactus)
    cactus.append(screen.create_image(rand_xCactus, rand_yCactus, image = cactus_img))

def r_check_if_bullet_hit_barrel():
    # If distance is less than 50, it means that the bullet hit the barrel.
    # Slow the bullet down
    i = 0
    if r_bullet:
        while i < len(xBarrel):
            if barrel:
                dist = sqrt((r_xBullet[0] - xBarrel[i])**2 + (r_yBullet[0] - yBarrel[i])**2)
            if dist <= 50:
                if r_xSpeed[0] > 0:
                    r_xSpeed[0] = r_xSpeed[0] + int(r_xSpeed[0]/2)
                elif r_xSpeed[0] < 0:
                    r_xSpeed[0] = r_xSpeed[0] - int(r_xSpeed[0]/2)
                screen.delete(barrel[i])
                barrel.pop(i)
                xBarrel.pop(i)
                yBarrel.pop(i)
                
            else:
                i += 1
                
def r_check_if_bullet_hit_cactus():
    # If distance is less than 50, it means that the bullet hit the cactus.
    # Depending on where the bullet hit, deflect.
    i = 0
    if r_bullet:
        while i < len(xCactus):
            if cactus:
                dist = sqrt((r_xBullet[0] - xCactus[i])**2 + (r_yBullet[0] - yCactus[i])**2)
            if dist <= 50:
                if yCactus[i] - r_yBullet[0] > 12:
                    r_ySpeed[0] = r_ySpeed[0] - randint(5, 10)
                elif yCactus[i] - r_yBullet[0] < -12:
                    r_ySpeed[0] = r_ySpeed[0] + randint(5, 10)
                else:
                    r_xSpeed[0] = r_xSpeed[0] * -1

                screen.delete(cactus[i])
                cactus.pop(i)
                xCactus.pop(i)
                yCactus.pop(i)    
            else:
                i += 1

def b_check_if_bullet_hit_barrel():
    i = 0
    if b_bullet:
        while i < len(xBarrel):
            if barrel:
                dist = sqrt((b_xBullet[0] - xBarrel[i])**2 + (b_yBullet[0] - yBarrel[i])**2)
            if dist <= 50:
                if b_xSpeed[0] > 0:
                    b_xSpeed[0] = b_xSpeed[0] - int(b_xSpeed[0]/2)
                elif b_xSpeed[0] < 0:
                    b_xSpeed[0] = b_xSpeed[0] + int(b_xSpeed[0]/2)
                    
                screen.delete(barrel[i])
                barrel.pop(i)
                xBarrel.pop(i)
                yBarrel.pop(i)
            else:
                i += 1

def b_check_if_bullet_hit_cactus():
    i = 0
    if b_bullet:
        while i < len(xCactus):
            if cactus:
                dist = sqrt((b_xBullet[0] - xCactus[i])**2 + (b_yBullet[0] - yCactus[i])**2)
            if dist <= 50:
                if yCactus[i] - b_yBullet[0] > 12:
                    b_ySpeed[0] = b_ySpeed[0] - randint(5, 10)
                elif yCactus[i] - b_yBullet[0] < -12:
                    b_ySpeed[0] = b_ySpeed[0] + randint(5, 10)
                else:
                    b_xSpeed[0] = b_xSpeed[0] * -1
                screen.delete(cactus[i])
                cactus.pop(i)
                xCactus.pop(i)
                yCactus.pop(i)
            else:
                i += 1
                
def resetValues():
    global t1, yStart1, ySpeed1, t2, yStart2, ySpeed2
    global r_player_bullet_state, b_player_bullet_state
    global r_bullet, r_xBullet, r_yBullet, r_xSpeed, r_ySpeed
    global b_bullet, b_xBullet, b_yBullet, b_xSpeed, b_ySpeed
    global r_score, b_score
    
    r_player_bullet_state = True
    yStart1 = height*0.5
    ySpeed1 = 1
    t1 = 0

    b_player_bullet_state = True
    yStart2 = height*0.5
    ySpeed2 = -1
    t2 = 0

    delete_r_bullet()
    delete_b_bullet()

    r_bullet = []
    r_xBullet = []
    r_yBullet = []
    r_xSpeed = []
    r_ySpeed = []
    
        
    b_bullet = []
    b_xBullet = []
    b_yBullet = []
    b_xSpeed = []
    b_ySpeed = []

    r_score = 0
    b_score = 0

def main():
    global transitionState, transition_i, playState, mainRectangle
    global t1, yStart1, ySpeed1, t2, yStart2, ySpeed2
    global r_player_bullet_state, b_player_bullet_state
    global r_bullet, r_xBullet, r_yBullet, r_xSpeed, r_ySpeed
    global b_bullet, b_xBullet, b_yBullet, b_xSpeed, b_ySpeed
    global barrel, xBarrel, yBarrel
    global cactus, xCactus, yCactus
    global r_score, b_score, r_winCount, b_winCount

    binding()
    mainButtons()
    drawBackground()
    r_winCount = 0
    b_winCount = 0
    drawTitle()
    fromMenu = True
    
    countDownList = ["3", "2", "1", "START"]
    transition_i = 0

    r_player_bullet_state = True
    yStart1 = height*0.5
    ySpeed1 = 1
    t1 = 0

    b_player_bullet_state = True
    yStart2 = height*0.5
    ySpeed2 = -1
    t2 = 0
    
    barrel = []
    xBarrel = []
    yBarrel = []

    cactus = []
    xCactus = []
    yCactus = []
    
    r_bullet = []
    r_xBullet = []
    r_yBullet = []
    r_xSpeed = []
    r_ySpeed = []

    b_bullet = []
    b_xBullet = []
    b_yBullet = []
    b_xSpeed = []
    b_ySpeed = []

    r_score = 0
    b_score = 0
    
    while True:
        if playState == False:
            if transitionState == True:
                transition_update()
                screen.update()
                # If from menu, create game when closed
                if fromMenu == True:
                    # If doors are closed
                    if transition_i == 126:
                        sleep(1)
                        menu_delete()
                        # Create starting obstacles
                        while len(cactus) != 10:
                            spawnCactus()
                        while len(barrel) != 5:
                            spawnBarrel()
                    # If doors finished reopening
                    elif transition_i == 252:
                        transitionState = False
                        # Counter
                        for i in range(0, len(countDownList)):
                            countDownText = screen.create_text(width*0.5, height*0.4, text = countDownList[i], font = "Comic 100", fill = "khaki")
                            screen.update()
                            sleep(0.5)
                            screen.delete(countDownText)
                        screen.delete(menu_blue_with_gun, menu_red_with_gun)
                        # Change playState
                        playState = True
                    else:
                        sleep(0.01)
                    transition_door_delete()
                    
                # If from game, create menu when closed
                else:
                    if transition_i == 126:
                        sleep(0.5)
                        drawTitle()
                    elif transition_i == 252:
                        ruleButton.configure(state = NORMAL)
                        sButton.configure(state = NORMAL)
                        # Change state
                        transitionState = False
                        fromMenu = True
                    else:
                        sleep(0.005)
                    transition_door_delete()
            else:
                screen.update()
                
        elif playState == True:
            # Play Game
            scoreboard()
            player_location_update()
            r_bullet_update()
            b_bullet_update()
            # Reload if both players shot and both bullets are off screen
            if b_player_bullet_state == False and r_player_bullet_state == False and not r_bullet and not b_bullet:
                b_player_bullet_state = True
                r_player_bullet_state = True
                if len(barrel) < 5:
                    spawnBarrel()
                while len(cactus) != 10:
                    spawnCactus()
            draw_player()
            draw_r_bullet()
            draw_b_bullet()
            screen.update() 
            sleep(0.025)
            screen.delete(r_player, b_player)
            # End game and return to menu if hit 5 times
            if r_score == 5:
                r_winCount += 1
                transitionState = True
                playState = False
                fromMenu = False
                transition()
                resetValues()
            elif b_score == 5:
                b_winCount += 1
                transitionState = True
                playState = False
                fromMenu = False
                transition()
                resetValues()
            delete_r_bullet()
            delete_b_bullet()
            delete_scoreboard()
            
# run main
root.after(0, main)
screen.pack()
screen.focus_set()
root.mainloop()
