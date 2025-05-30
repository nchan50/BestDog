Web VPython 3.2

## Circuit simulation

##################
# CONSTANTS

SCALE = 5
HOTDOG_RESISTIVITY = 346 * 100 #Ohm/cm

##################
# GLOBAL VARS

dogs = []
change_presets = []
current_preset = []
immutable = True

##################
# CAMERA/SCENE

scene.camera.pos = vec(-30, 0, -30)
scene.camera.axis = vec(30, 0, 30)
scene.fov = pi/8
scene.autoscale = False

background = cone(pos=vec(0, -1.25 * scene.camera.pos.mag *  SCALE, 0), axis=vec(0, 1,0), texture="https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/the_noble_hot_dog%20(1).png",length=2.5 * scene.camera.pos.mag * SCALE, radius=0.75 * scene.camera.pos.mag * SCALE)

battery = box(pos = vec(15, 0, -15), axis = vec(0, 1, 0), length = 10, height = 10, width = 6) 


##################
# GUI


######
# PRESET BUTTONS

scene.title = "Presets: \n"
change_presets.append(button(text="One Hotdog", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Resistor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Resistor in Parallel", pos=scene.title_anchor, bind=presets))
scene.append_to_title('\n') # so the buttons dont clip out
change_presets.append(button(text="Hotdog and Capacitor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Capacitor in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Inductor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Inductor in Parallel", pos=scene.title_anchor, bind=presets))

######
# GRAPHS

temp = graph(title='Hotdog 1', xtitle='Time(s)', ytitle='Energy Dissipated(J)', xmin=0, ymin=0, xmax = 120, ymax = 500)
a = gcurve(graph=temp)
for x in range(0, 120):
    a.plot(x, 150 - 50 ^ x)


##################
# CLASSES

######
# CIRCEL = CIRCUIT ELEMENT

# possible types:
#    battery
#    resistor
#    hotdog (resistor)
#    capacitor (?)
#    inductor (?)
class CIRCEL: 
    def __init__(self, type, val):
        self.type = type
        self.val = val


######
# SERL = SERIES LIST

class SERL:
    def __init__(self, prev, next, el_list):
        self.element_list = element_list
    def set_pn(self,prev,next):
        self.prev = prev
        self.next = next
    def get_pn(self):
        return [self.prev,self.next]
    def add_element(self,elem):
        if (elem.TYPE() == "resistor"):
            self.element_list.append(elem)
    def REQ(self):
        req = 0;
        for i in self.element_list:
            if (i.TYPE() in ["resistor","hotdog"]):
                req += i.val;
        return req
 
 
######
# SERL = PARALLEL LIST

class PARL:
    def __init__(self,element_list): 
        self.element_list = element_list
    def set_pn(self,prev,next):
        self.prev = prev
        self.next = next
    def get_pn(self):
        return [self.prev,self.next]
    def add_element(self,elem):
        if (elem.TYPE() in ["resistor","hotdog"]):
            self.element_list.append(elem)
    def REQ(self):
        req = 0;
        for i in self.element_list:
            if (i.TYPE() in ["resistor","hotdog"]):
                req += 1 / i.val;
        return 1 / req


##################
# COMPUTATIONAL FUNCTIONS

# goes searching for  'start' until you get back to that spot
#def kirchoff_loops(start):

##################
# HELPER FUNCTIONS

def circle_area(radius):
    return pi * (radius ** 2)

def calc_resistance(resistivity,radius,length):
    return resistivity * circleArea(radius) / length

def create_dog(radius, length): #radius and length in METERS
    hotdog = CIRCEL("hotdog",HOTDOG_RESISTIVITY*pi*(radius**2))
    return hotdog


##################
# CIRCUIT PRESETS


######
# One Hotdog
def one_dog(voltage):
    batt = CIRCEL("battery",voltage)
    dog = create_dog(0.01,0.1)
    circ = SERL(None,None,[batt])
    circ.add_element(dog)
    circ.set_pn(circ,circ)
    return circ

######
# Hotdogs in Series
def dogs_ser(voltage,n):
    batt = CIRCEL("battery",voltage)
    circ = SERL(None,None,[batt])
    for i in range(n):
        circ.add_element(create_dog(1, 1))
    circ.set_pn(circ,circ)
    return circ
     
######
# Hotdogs in Parallel
def dogs_par(voltage,n):
    batt = CIRCEL("battery",voltage)
    circ = PARL(None,None,[batt])
    for i in range(n):
        circ.add_element(create_dog(1, 1))
    circ.set_pn(circ,circ)
    return circ
    
######
# Hotdog and Resistor in Series
def dog_res_ser(voltage,resistance):
    batt = CIRCEL("battery",voltage)
    res = CIRCEL("resistor",resistance)
    dog = create_dog(1, 1)
    circ = SERL(None,None,[batt,res,dog])
    circ.set_pn(circ,circ)
    return circ
    

######
# Hotdog and Resistor in Parallel
def dog_res_par(voltage):
    batt = CIRCEL("battery",voltage)

######
# Hotdog and Capacitor in Series
def dog_cap_ser(voltage):
    batt = CIRCEL("battery",voltage)

######
# Hotdog and Capacitor in Parallel
def dog_cap_par(voltage):
    batt = CIRCEL("battery",voltage)

######
# Hotdog and Inductor in Series
def dog_ind_ser(voltage):
    batt = CIRCEL("battery",voltage)

######
# Hotdog and Inductor in Parallel
def dog_ind_par(voltage):
    batt = CIRCEL("battery",voltage)

#def preset_circuits():

def create_visual(sp):
    elements = sp.get_list()
    e_visual = [] 
    for e in elements:
        if isinstance(e, CIRCEL):
            e_visuals.append(element_visual(e))
        else:
            e_visuals.append(create_visual(e))
    return e_visual
    
def element_visual(e):
    if e.type == 'hotdog':
        L, R = e.get_value()
        visual = [cylinder(pos = vec(-L/2, 0, 0), length = L, radius = R, axis = vec(1, 0, 0), color = color.red), 
        sphere(pos = vec(-L/2, 0, 0), radius = R, color = color.red),
        sphere(pos= vec(L/2, 0, 0), radius = R, color = color.red)]
    if e.type == 'battery':
        V = e.get_value()
        visual = [box(pos = vec(0 0, 0), axis = vec(1, 1, 1), length = V/sqrt(3), height = V/sqrt(3), width = V/sqrt(3))]
    if e.type == 'resistor':
        R = e.get_value()
        visual = [cylinder(pos = vec(-4, 0, 0), length = 8, radius = 1, axis = vec(1, 0, 0), color = color.cyan), 
        sphere(pos = vec(-4, 0, 0), radius = 1.5, color = color.cyan),
        sphere(pos= vec(4, 0, 0), radius = 1.5, color = color.cyan)
    if e.type == 'capacitor':
        C = e.get_value()
        visual = [box(pos = vec(0, 2, 0), axis = vec(0, 1, 0), length = 2, height = C/sqrt(2), width = C/sqrt(2), color = color.red),
         box(pos = vec(0, -2, 0), axis = vec(0, -1, 0), length = 2, height = C/sqrt(2), width = C/sqrt(2), color = color.blue)]
    if e.type == 'inductor':
        L = e.get_value()
        visual = [helix(pos = vec(-5, 0, 0), axis = (1, 0, 0), length = 10, coil = sqrt(L), radius = 4, thickness = 0.8, color = color.black)]
    return visual

def presets(evt):
    global change_presets
    global current_preset
    global all_presets
    evt.color = color.white
    evt.background = color.black
    for button in change_presets:
        if button != evt and button.color == color.white:
            button.color = color.black
            button.background = color.white
    for item in current_preset:
        item.visible = False
    current_preset = all_presets[evt.text]
    for item in current_preset:
        item.visible = True

def create_dog():
    global immutable
    if immutable:
        shaft = cylinder(length=15, radius = 1, axis=vec(1, 1, 1), color=color.red)
        shaft.pos = vec(-1, -1, -1) * shaft.length / (2 * sqrt(3)) 
        end1 = sphere(pos=vec(1, 1, 1) * shaft.length / (2 * sqrt(3)), radius=shaft.radius, color=color.red)
        end2 = sphere(pos=vec(-1, -1, -1) * shaft.length / (2 * sqrt(3)), radius=shaft.radius, color=color.red)
        dogs.append([end1, end2, shaft])
    immutable = False
    
def adjust_dog(evt):
    if evt.id is 'r' and not immutable:
        for shape in dogs[-1]:
            shape.radius = evt.value
        rt.text = '{:1.2f}'.format(evt.value)
    if evt.id is 'l' and not immutable:
        for shape in dogs[-1]:
            shape.pos *= evt.value / dogs[-1][2].length
        dogs[-1][2].length = evt.value
        lt.text = '{:1.2f}'.format(evt.value)

def save_dog():
    global immutable
    immutable = True

def temp():
    return

scene.title = "Presets: \n"
change_presets.append(button(text="One Hotdog", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Resistor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Resistor in Parallel", pos=scene.title_anchor, bind=presets))
scene.append_to_title('\n')
change_presets.append(button(text="Hotdog and Capacitor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Capacitor in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Inductor in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Inductor in Parallel", pos=scene.title_anchor, bind=presets))

scene.caption = 'User Options: \n'
scene.append_to_caption('Start Simulation: ')
button(bind = temp, text= 'Turn on Battery')
scene.append_to_caption('\nMake Your Own Hot Dog: ')
button(bind = create_dog, text= 'Create!')
button(bind = save_dog, text= 'Save!')
button(bind = temp, text= 'Attatch to Circuit!')
scene.append_to_caption('\n Adjust Your Hotdogs \n')
rs = slider(bind = adjust_dog, max = 2, min = 0.25, step = 0.1, value = 1, id = 'r')
scene.append_to_caption('Radius: ')
rt = wtext(text='{:1.2f}'.format(rs.value))
scene.append_to_caption(' cm\n')
ls = slider(bind = adjust_dog, max = 30, min = 5, step = 0.1, value = 15, id = 'l')
scene.append_to_caption('Length: ')
lt = wtext(text='{:1.2f}'.format(ls.value))
scene.append_to_caption(' cm\n')
ev = winput(bind=temp, prompt='Adjust Circuit Element Values:', type='numeric')
    
while True:
    rate(10)
    a = background.pos.z / sqrt(background.pos.x ** 2 + background.pos.y ** 2)
    camera_pos = scene.camera.pos
    cone_closest = vec(camera_pos.x/(2 + a), (camera_pos.y - background.pos.x)/ (2 + a), 0)
    cone_closest.z = a * sqrt(cone_closest.x ** 2, cone_closest.y ** 2) + background.pos.x
    if sqrt((cone_closest.x - camera_pos.x) ** 2 + (cone_closest.y - camera_pos.y) ** 2 + (cone_closest.z - camera_pos.z) ** 2) < background.radius / 9:
        background.pos = vec(0, -1.5 * scene.camera.pos.mag *  SCALE, 0)
        background.length = 2.5 * scene.camera.pos.mag * SCALE
        background.radius = 1.75 * scene.camera.pos.mag * SCALE
