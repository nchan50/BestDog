Web VPython 3.2

## Circuit simulation

##################
# CONSTANTS

SCALE = 20
HOTDOG_RESISTIVITY = 346 * 100 #Ohm/cm

##################
# GLOBAL VARS

dogs = []
dogs_visual = []
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
# OTHER BUTTONS
def temp():
    return

scene.caption = 'User Options: \n'
scene.append_to_caption('Start Simulation: ')
button(bind = temp, text= 'Turn on Battery')
scene.append_to_caption('\nMake Your Own Hot Dog: ')
button(bind = dog_visual, text= 'Create!')
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
    def __init__(self,element_list):
        self.element_list = element_list
        self.type = "SERL"
    def set_pn(self,prev,next):
        self.prev = prev
        self.next = next
    def add_element(self,elem):
#        if (elem.type == "resistor"):
        self.element_list.append(elem)
#    def REQ(self):
#        req = 0;
#        for i in self.element_list:
#            if (i.TYPE() in ["resistor","hotdog"]):
#                req += i.val;
#        return req
 
 
######
# SERL = PARALLEL LIST

class PARL:
    def __init__(self,element_list): 
        self.element_list = element_list
        self.type = "PARL"
    def set_pn(self,prev,next):
        self.prev = prev
        self.next = next
    def add_element(self,elem):
        self.element_list.append(elem)
#    def REQ(self):
#        req = 0;
#        for i in self.element_list:
#            if (i.TYPE() in ["resistor","hotdog"]):
#                req += 1 / i.val;
#        return 1 / req


##################
# COMPUTATIONAL FUNCTIONS

def calculate_paths(current,depth,og):
#    print(0) #number of times func is called
#    print(len(current.element_list))
    if (depth < 0):
        return 0
    elif (current == og):
#        print(current.type)
        if current.type == "PARL":
#            print(len(current.element_list))
            return len(current.element_list)
        elif current.type == "SERL":
            return 1
        else:
            return -1
    else:
#        print(current.type)
        if current.type == "PARL":
#            print(len(current.element_list))
            return len(current.element_list) * calculate_paths(next,depth-1,og)
        elif current.type == "SERL":
            return calculate_paths(next,depth-1,og)
        else:
            return -1
            


# goes searching for  'start' until you get back to that spot

#def kirchoff_loop(start,):
#    path = []
#    if start.type == "SERL":
#        
#    size = len(start.element_list)
    
    

    

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
    hot_dog = create_dog(0.01,0.1)
    batt_circ = SERL([batt])
    circ = SERL([hot_dog])
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

######
# Hotdogs in Series
def dogs_ser(voltage,n):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = SERL([])
    for i in range(n):
        circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ
     
######
# Hotdogs in Parallel
# def dogs_par(voltage,n):
#     batt = CIRCEL("battery",voltage)
#     batt_circ = SERL([batt])
#     circ = PARL([])
#     for i in range(n):
#         circ.add_element(create_dog(1, 1))
#     circ.set_pn(batt_circ,batt_circ)
#     batt_circ.set_pn(circ,circ)
#     return circ
def dogs_par(voltage,n):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    par_circ = PARL([])
    for i in range(n):
        par_circ.add_element(CIRCEL("hotdog", (0.01, 0.1)))
    circ.add_element(par_circ)
    circ.set_pn(circ,circ)
    return circ
    
######
# Hotdog and Resistor in Series
def dog_res_ser(voltage,resistance):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = SERL([])
    circ.add_element(CIRCLEL("resistor",resistance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ
    
######
# Hotdog and Resistor in Parallel
def dog_res_par(voltage,resistance):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = PARL([])
    circ.add_element(CIRCLEL("resistor",resistance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

######
# Hotdog and Capacitor in Series
def dog_cap_ser(voltage):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = SERL([])
    circ.add_element(CIRCLEL("capacitor",capacitance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

######
# Hotdog and Capacitor in Parallel
def dog_cap_par(voltage,capacitance):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = PARL([])
    circ.add_element(CIRCLEL("capacitor",capacitance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

######
# Hotdog and Inductor in Series
def dog_ind_ser(voltage,inductance):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = SERL([])
    circ.add_element(CIRCLEL("inductor",inductance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

######
# Hotdog and Inductor in Parallel
def dog_ind_par(voltage):
    batt = CIRCEL("battery",voltage)
    batt_circ = SERL([batt])
    circ = PARL([])
    circ.add_element(CIRCLEL("inductor",inductance))
    circ.add_element(create_dog(1, 1))
    circ.set_pn(batt_circ,batt_circ)
    batt_circ.set_pn(circ,circ)
    return circ

# Conencts presets to buttons
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


##################
# CIRCUIT VISUALS


# Returns the box of the first element in a nested list
def get_first_box(e_visuals):
    first = e_visuals[0]
    if not isinstance(first, box):
        first = get_first_box(first)
    return first


# Returns the box of the last element in a nested list
def get_last_box(e_visuals):
    last = e_visuals[-1]
    if not isinstance(last[0], box):
        last = get_last_box(last[-1])
    else:
        return last[0]
    return last


# Recursively translates all shapes in a nested list
def reposition(e_visual, translation):
    for item in e_visual:
        if not isinstance(item, (curve, box, cone, sphere, helix, cylinder)):
            reposition(item, translation)
        else:
            if isinstance(item, curve):
                for n in range(item.npoints):
                    item.modify(n, pos = item.point(n)['pos'] + translation)
            else:
                item.pos +=  translation
      
      
# Presets of element visuals based on the type
def element_visual(e, create_mode = False):
    if e.type == 'hotdog':
        R, L = e.val
        R *=  100
        L *=  100
        visual = [
            box(pos = vec(0, 0, 0), length = L, height = max(1.5, 2 * R), width = max(1.5, 2 * R), visible = False), 
            cylinder(pos = vec(-L/2, 0, 0), length = L, radius = R, axis = vec(1, 0, 0), color = color.red),
            sphere(pos = vec(-L/2, 0, 0), radius = R, color = color.red),
            sphere(pos =  vec(L/2, 0, 0), radius = R, color = color.red)]
        if not create_mode:
            visual[0].length += 6
            visual.append(cone(pos = vec(-L/2 - 3, 0, 0), axis = vec(1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
            visual.append(cone(pos = vec(L/2 + 3, 0, 0), axis = vec(-1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
    if e.type == 'battery':
        V = e.val
        visual = [
            box(pos = vec(0, 0, 0), length = V, height = V, width = V, visible = False),
            box(pos = vec(0, 0, 0), axis = vec(1, 0, 0), length = V, height = V, width = V)]
    if e.type == 'resistor':
        R = e.val
        visual = [
            box(pos = vec(0, 0, 0), length = 9, height = 3.2, width = 3.2, visible = False),
            cylinder(pos = vec(-3, 0, 0), length = 6, radius = 1, axis = vec(1, 0, 0), color = color.cyan),
            cylinder(pos = vec(-3.25, 0, 0), length = 0.5, radius = 1.6, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(-1.5, 0, 0), length = 0.5, radius = 1.1, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(0, 0, 0), length = 0.5, radius = 1.1, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(2.75, 0, 0), length = 0.5, radius = 1.6, axis = vec(1, 0, 0), color = color.black),
            sphere(pos = vec(-3, 0, 0), radius = 1.5, color = color.cyan),
            sphere(pos =  vec(3, 0, 0), radius = 1.5, color = color.cyan)]
    if e.type == 'capacitor':
        C = e.val
        visual = [
            box(pos = vec(0, 0, 0), length = 6, height = 6, width = 6, visible = False),
            box(pos = vec(2, 0, 0), axis = vec(1, 0, 0), length = 2, height = 6, width = 6, color = color.red),
            box(pos = vec(-2, 0, 0), axis = vec(-1, 0, 0), length = 2, height = 6, width = 6, color = color.blue)]
    if e.type == 'inductor':
        N = 15 - exp(-sqrt(e.val) / 50 + log(15)) + 5
        a = (N % 1) * 2 * pi
        visual = [
            box(pos = vec(0, 0, 0), length = 10, height = 8, width = 8, visible = False),
            helix(pos = vec(-5, 0, 0), axis = vec(1, 0, 0), length = 10, coils = N, radius = 4, thickness = 0.8, color = color.black),
            cylinder(pos = vec(-5, 0, 4), axis = vec(0, 0, -1), length = 4, radius = 0.4, color = color.black),
            cylinder(pos = vec(5, 0, 4) + 4 * vec(0, sin(a), cos(a) - 1), axis = vec(0, -sin(a), -cos(a)), length = 4, radius = 0.4, color = color.black)]
    return visual
        
        
# Recursively creates the central circuit     
def create_sub_circuit(circ):
    elements = circ.element_list
    e_visuals = []
    for e in elements:
        if isinstance(e, CIRCEL):
            element = element_visual(e)
            if isinstance(circ, SERL):
                try:
                    prev_pos = e_visuals[-1][0].pos + vec(e_visuals[-1][0].length / 2, 0, 0)
                    next_pos = prev_pos + vec(5, 0, 0)
                    wire = [
                        box(pos = (prev_pos + next_pos) / 2, length = 5, height = 0.4, width = 0.4, visible = False), 
                        curve(pos = [prev_pos, next_pos], radius = 0.2, color = color.yellow)]
                    for shape in element:
                        shape.pos += next_pos + vec(element[0].length / 2, 0, 0)
                    e_visuals.append(wire)
                except TypeError:
                    pass
            if isinstance(circ, PARL):
                try:
                    prev_box = e_visuals[-1][0]
                    current_box = element[0]
                    wire = [
                        box(pos = prev_box.pos + (vec(0, (prev_box.height + current_box.height) / 2 + 5, 0)) / 2, length = 0, height = (prev_box.height + current_box.height) / 2 + 5, width = 0.4, visible = False), 
                        curve(pos = [prev_box.pos + vec(prev_box.length / 2, 0, 0), prev_box.pos, prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0),
                        prev_box.pos + vec(current_box.length / 2, (prev_box.height + current_box.height) / 2 + 5, 0)], radius = 0.2, color = color.yellow),
                        curve(pos = [prev_box.pos + vec(-prev_box.length / 2, 0, 0), prev_box.pos, prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0),
                        prev_box.pos + vec(-current_box.length / 2, (prev_box.height + current_box.height) / 2 + 5, 0)], radius = 0.2, color = color.yellow)]
                    for shape in element:
                        shape.pos += prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0)
                    e_visuals.append(wire)
                except TypeError:
                    pass
            e_visuals.append(element)
        else:
            sub_e_visuals = create_sub_circuit(e)
            prev_pos = vec(0, 0, 0)
            try:
                prev_box = get_last_box(e_visuals)
                if isinstance(circ, SERL):
                    prev_pos = prev_box.pos + vec(prev_box.length / 2, 0, 0)
                    next_pos = prev_pos + vec(5, 0, 0)
                    wire = [
                        box(pos = (prev_pos + next_pos) / 2, length = 5, height = 0.4, width = 0.4, visible = False), 
                        curve(pos = [prev_pos, next_pos], radius = 0.2, color = color.yellow)]
                    e_visuals.append(wire)
                    reposition(sub_e_visuals, next_pos + vec(get_first_box(sub_e_visuals).length / 2, 0, 0))
                if isinstance(circ, PARL):
                    current_box = get_first_box(sub_e_visuals)
                    wire = [
                        box(pos = prev_box.pos + (vec(0, (prev_box.height + current_box.height) / 2 + 5, 0)) / 2, length = 0, height = (prev_box.height + current_box.height) / 2 + 5, width = 0.4, visible = False), 
                        curve(pos = [prev_box.pos + vec(prev_box.length / 2, 0, 0), prev_box.pos, prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0),
                        prev_box.pos + vec(current_box.length / 2, (prev_box.height + current_box.height) / 2 + 5, 0)], radius = 0.2, color = color.yellow),
                        curve(pos = [prev_box.pos + vec(-prev_box.length / 2, 0, 0), prev_box.pos, prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0),
                        prev_box.pos + vec(-current_box.length / 2, (prev_box.height + current_box.height) / 2 + 5, 0)], radius = 0.2, color = color.yellow)]
                    e_visuals.append(wire)
                    reposition(sub_e_visuals, prev_box.pos + vec(0, (prev_box.height + current_box.height) / 2 + 5, 0))
            except TypeError:
                pass
            if isinstance(e, PARL):
                sub_e_visuals = [sub_e_visuals[0]] + list(reversed(sub_e_visuals[1:]))
            e_visuals.append(sub_e_visuals)
                
    max_l, max_h, max_w, min_l, min_h, min_w  = 0, 0, 0, 0, 0, 0
    for element in e_visuals:
        max_l = max(max_l, element[0].pos.x + element[0].length / 2)
        max_h = max(max_h, element[0].pos.y + element[0].height / 2)
        max_w = max(max_w, element[0].pos.z + element[0].width / 2)
        min_l = min(min_l, element[0].pos.x - element[0].length / 2)
        min_h = min(min_h, element[0].pos.y - element[0].height / 2)
        min_w = min(min_w, element[0].pos.z - element[0].width / 2)    
    l, w, h = max_l - min_l, max_w - min_w, max_h - min_h
    if isinstance(circ, PARL):
        l += 4
        for element in e_visuals:
            if isinstance(element[1], curve):
                element[0].length = l
                for n in range(element[1].npoints):
                    if n == 1 or n == 2:
                        element[1].modify(n, pos = element[1].point(n)['pos'] + vec(l / 2, 0, 0))
                for n in range(element[2].npoints):
                    if n == 1 or n == 2:
                        element[2].modify(n, pos = element[2].point(n)['pos'] - vec(l / 2, 0, 0))
        l += 0.4
    reposition(e_visuals, -vec(max_l + min_l, max_h + min_h, max_w + min_w) / 2)
    e_visuals.insert(0, box(pos = vec(0, 0, 0), length = l, height = h, width = w, visible = False))
    return e_visuals
    
    
# Connects the beginning and end of the sub circuit
def circuit_loop(e_visuals):
    circ_box = e_visuals[0]
    last_box = get_last_box(e_visuals)
    first_box = get_first_box(e_visuals[1:])
    prev_pos = last_box.pos + vec(last_box.length / 2, 0, 0)
    next_pos = first_box.pos - vec(first_box.length / 2, 0, 0)
    wire = [
        box(pos = (prev_pos + next_pos + vec(0, 0, circ_box.width / 2 + 5)) / 2, length = circ_box.length + 10.4, height = 0.4, width = circ_box.width / 2 + 5.4, visible = False), 
        curve(pos = [prev_pos, prev_pos + vec(5, 0, 0), prev_pos + vec(5, 0, circ_box.width / 2 + 5), next_pos + vec(-5, 0, circ_box.width / 2 + 5), next_pos + vec(-5, 0, 0), next_pos], radius = 0.2, color = color.yellow)]
    e_visuals.append(wire)
 
 
# Creates the circuit
def create_circuit(circ):
    circuit_loop(create_sub_circuit(circ))


# Different circuit models
def test(mode):
    circ = SERL([])
    # All the elements in series
    if mode == 0:
        circ.add_element(CIRCEL('battery', 10))
        circ.add_element(CIRCEL('inductor', 10))
        circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        circ.add_element(CIRCEL('capacitor', 10))
        circ.add_element(CIRCEL('resistor', 5))
        circ.add_element(CIRCEL('battery', 5))
    # Hotdogs in a compelx circuit
    if mode == 1:
        circ.add_element(CIRCEL('battery', 10))
        circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        par_1 = PARL([])
        sub_par_1 = PARL([])
        sub_par_2 = PARL([])
        sub_ser_1 = SERL([])
        sub_ser_2 = SERL([])
        sub_par_1.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_par_1.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_par_2.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_ser_1.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_ser_1.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_ser_2.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_ser_2.add_element(CIRCEL('hotdog', (0.01, 0.1)))
        sub_par_2.add_element(sub_ser_1)
        par_1.add_element(sub_ser_2)
        par_1.add_element(sub_par_1)
        par_1.add_element(sub_par_2)
        circ.add_element(par_1)
        circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    return circ
        
    
#create_circuit(test(0))
#create_circuit(test(1))

def dog_visual():
    global immutable
    if immutable:
        dogs.append(CIRCEL('hotdog', (0.01, 0.1)))
        dogs_visual.append(element_visual(dogs[-1], create_mode = True))
    immutable = False
    
def adjust_dog(evt):
    if evt.id is 'r' and not immutable:
        dogs[-1].val = (evt.value, dogs[-1].val[1])
        for shape in dogs_visual[-1]:
            shape.radius = evt.value
        dogs_visual[-1][0].height = 2 * evt.value
        dogs_visual[-1][0].width = 2 * evt.value
        rt.text = '{:1.2f}'.format(evt.value)
    if evt.id is 'l' and not immutable:
        dogs[-1].val = (dogs[-1].val[0], evt.value)
        for shape in dogs_visual[-1]:
            shape.pos *= evt.value / dogs_visual[-1][1].length
        dogs_visual[-1][0].length = 2 * evt.value
        dogs_visual[-1][1].length = evt.value
        lt.text = '{:1.2f}'.format(evt.value)

def save_dog():
    return
