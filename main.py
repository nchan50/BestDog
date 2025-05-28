Web VPython 3.2

scene.camera.pos = vec(100, 0, 0)
scene.camera.axis = vec(-100, 0, 0)
scene.fov = pi/3.5
scene.autoscale = False
SCALE = 5

dogs = []
background = cone(pos=vec(0, -1.5 * scene.camera.pos.mag *  SCALE, 0), axis=vec(0, 1,0), texture="https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/the_noble_hot_dog%20(1).png",length=2.5 * scene.camera.pos.mag * SCALE, radius=1.75 * scene.camera.pos.mag * SCALE)

immutable = True

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
    
scene.caption = 'Create Your Hot Dog: '
button(bind = create_dog, text= 'Create me!')
scene.append_to_caption('\n')
rs = slider(bind = adjust_dog, max = 2, min = 0.25, step = 0.1, value = 1, id = 'r')
scene.append_to_caption('Radius: ')
rt = wtext(text='{:1.2f}'.format(rs.value))
scene.append_to_caption(' cm\n')
ls = slider(bind = adjust_dog, max = 30, min = 5, step = 0.1, value = 15, id = 'l')
scene.append_to_caption('Length: ')
lt = wtext(text='{:1.2f}'.format(ls.value))
scene.append_to_caption(' cm\n')
button(bind = save_dog, text= 'Save me!')
    
while True:
    rate(10)
    a = background.pos.z / sqrt(background.pos.x ** 2 + background.pos.y ** 2)
    camera_pos = scene.camera.pos
    cone_closest = vec(camera_pos.x/(2 + a), (camera_pos.y - background.pos.x)/ (2 + a), 0)
    cone_closest.z = a * sqrt(cone_closest.x ** 2, cone_closest.y ** 2) + background.pos.x
    if sqrt((cone_closest.x - camera_pos.x) ** 2 + (cone_closest.y - camera_pos.y) ** 2 + (cone_closest.z - camera_pos.z) ** 2) < background.radius / 3:
        background.pos = vec(0, -1.5 * scene.camera.pos.mag *  SCALE, 0)
        background.length = 2.5 * scene.camera.pos.mag * SCALE
        background.radius = 1.75 * scene.camera.pos.mag * SCALE






## Circuit simulation

#ordered list for both parallel and series
#my_dog = Dog("Buddy", "Golden Retriever")

##################
# CONSTANTS

HOTDOG_RESISTIVITY = 346 * 100 #Ohm/cm

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
        
    def TYPE(self):
        return self.type


######
# SERL = SERIES LIST

class SERL:
    def __init__(self, prev, next, element_list):
        self.prev = prev
    def add_element(elem):
        if (elem.TYPE() == "resistor"):
            self.element_list.append(elem)
    def REQ(self):
        req = 0;
        for i in self.element_list:
            if (i.TYPE() == "resistor"):
                req += i.val;
        return req
 
 
######
# SERL = PARALLEL LIST

class PARL:
    def __init__(self, prev, next, element_list):
        self.prev = prev
    def add_element(elem):
        if (elem.TYPE() == "resistor"):
            self.element_list.append(elem)
    def REQ(self):
        req = 0;
        for i in self.element_list:
            if (i.TYPE() == "resistor"):
                req += 1 / i.val;
        return 1 / req

##################
# OTHER FUNCTIONS

def circleArea(radius):
    return pi * (radius ** 2)

def calc_resistance(resistivity,radius,length):
    return resistivity * circleArea(radius) / length

def create_dog(radius, length): #radius and length in METERS
    hotdog = CIRCEL("resistor",HOTDOG_RESISTIVITY*pi*(radius**2)
    return hotdog


##################
# CIRCUIT PRESETS


# just battery and hotdog
def batt_dog(voltage):
    batt = CIRCEL("battery",voltage)
    
    hot_dog = CIRCEL("resistor",)
    circ = SERL(batt,batt,[hotdog])


#def preset_circuits()









