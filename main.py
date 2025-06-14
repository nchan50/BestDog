Web VPython 3.2

## Circuit simulation

##################
# CONSTANTS

SCALE = 20
HOTDOG_RESISTIVITY = 0.027 #Ohm/m
HOTDOG_DENSITY = 1000 #kg/m^3
HOTDOG_SPECIFIC_HEAT = 3350 #J/kg*K
count = 0
burnt, charred, perfect, undercooked, uncooked = 100, 75, 50, 25, 0
max_battery, max_capacitor, max_inductor = 2, 1, 1
frame_rate = 500
time = 0
speeder = 1

##################
# GLOBAL VARS

change_presets = []
data_graphs = []
data_curves = []
circuit = None
circuit_visual = None
blanks = []
blanks_visual = []
externals = []
externals_visual = []
element_vector = []
junction_matrix = []
junction_augmented_vector = []
kirchoff_matrix = []
kirchoff_augmented_vector = []
start = False
attatching = False
stepper = 0
breaker = False
drag = False
dragged_object = None
select = False
selected_circels = []
selected_objects = []
selected_labels = []
selected_highest_level = None
selected_secondary_level = []
dt = 0.000005# time step



##################
# CAMERA/SCENE

scene.camera.pos = vec(-30, 0, -30)
scene.camera.axis = vec(30, 0, 30)
scene.fov = pi/8
scene.autoscale = False

background = cone(pos=vec(0, -1.25 * scene.camera.pos.mag *  SCALE, 0), axis=vec(0, 1,0), texture="https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/the_noble_hot_dog%20(1).png",length=2.5 * scene.camera.pos.mag * SCALE, radius=0.75 * scene.camera.pos.mag * SCALE)

##################
# MOUSE AND KEY INPUTS
scene.bind('mousedown', def():
    scene.bind('mousemove', def():
        global drag
        drag = True
    )
    scene.bind('mouseup', def():
        global drag
        drag = False
    )
)

scene.bind('click', def():
    global select
    select = True
)

scene.bind('keydown', key_pressed)
def key_pressed(evt):
    global attatching
    global breaker
    keyname = evt.key
    if keyname == 'a':
        breaker = True and attatching
        
        
##################
# GUI


######
# PRESET BUTTONS

scene.title = "Presets: \n"
change_presets.append(button(text="One Hotdog", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Series", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdogs in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Resistor in Series", pos=scene.title_anchor, bind=presets))
scene.append_to_title('\n') # so the buttons dont clip out
change_presets.append(button(text="Hotdog and Resistor in Parallel", pos=scene.title_anchor, bind=presets))
change_presets.append(button(text="Hotdog and Capacitor in Series", pos=scene.title_anchor, bind=presets))
#change_presets.append(button(text="Hotdog and Capacitor in Parallel", pos=scene.title_anchor, bind=presets))
#change_presets.append(button(text="Hotdog and Inductor in Series", pos=scene.title_anchor, bind=presets))
#change_presets.append(button(text="Hotdog and Inductor in Parallel", pos=scene.title_anchor, bind=presets))


######
# OTHER BUTTONS

scene.caption = 'User Options: \n'
scene.append_to_caption('Start Simulation: ')
button(bind = start_battery, text= 'Turn on Battery')
button(bind = stop_battery, text= 'Turn off Battery')
scene.append_to_caption('\nMake Your Own Hot Dog: ')
button(bind = dog_visual, text= 'Create!')
scene.append_to_caption('\n Adjust Your Hotdogs \n')
rs = slider(bind = adjust_dog, max = 2, min = 0.25, step = 0.1, value = 1, id = 'r')
scene.append_to_caption('Radius: ')
rt = wtext(text = '{:1.2f}'.format(rs.value))
scene.append_to_caption(' cm\n')
ls = slider(bind = adjust_dog, max = 30, min = 5, step = 0.1, value = 10, id = 'l')
scene.append_to_caption('Length: ')
lt = wtext(text = '{:1.2f}'.format(ls.value))
scene.append_to_caption(' cm\n')     
ev = winput(bind = adjust_circel, prompt = 'Adjust Circuit Element Values:', type = 'numeric')
scene.append_to_caption('\n')
attatch_check = checkbox(bind = attatch_object, text= 'Attatch to Circuit!')


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
        self.current = 0
        if type == 'hotdog':
            self.temperature = 293 #Room Temperature
        if type == 'capacitor':
            self.charge = 0
        if type == 'inductor':
            self.di = 0
            

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
        self.element_list.append(elem)
 
 
######
# PARL = PARALLEL LIST

class PARL:
    def __init__(self,element_list): 
        self.element_list = element_list
        self.type = "PARL"
    def set_pn(self,prev,next):
        self.prev = prev
        self.next = next
    def add_element(self,elem):
        self.element_list.append(elem)


##################
# COMPUTATIONAL FUNCTIONS

def RREF(M, a):
    back_count = 0
    for i in range(len(M)):
        for j in range(1, len(M) + 1):
            if all(x == 0 for x in M[-j]) and j > back_count:
                zero_M = M.pop(-j)
                zero_a = a.pop(-j)
                M.append(zero_M)
                a.append(zero_a)
                back_count += 1
        if i >= len(M) - back_count:
            break
        leftmost_i = i
        leftmost_j = len(M[0]) - 1
        for k in range(i, len(M) - back_count):
            for n in range(len(M[0])):
                if M[k][n] != 0 and n < leftmost_j:
                    leftmost_j = n
                    leftmost_i = k
        M_temp = M[i][:]
        M[i] = M[leftmost_i]
        M[leftmost_i] = M_temp
        a_temp = a[i]
        a[i] = a[leftmost_i]
        a[leftmost_i] = a_temp
        factor = M[i][leftmost_j]
        a[i] = a[i] / factor
        M[i] = [e / factor for e in M[i]]
        for k in range(i + 1, len(M) - back_count):
            factor = M[k][leftmost_j] / M[i][leftmost_j]
            a[k] -= a[i] * factor
            for j in range(len(M[0])):
                M[k][j] -= M[i][j] * factor
    a = a[:len(M) - back_count]
    M = M[:len(M) - back_count]
    for i in range(1, len(M) + 1):
        leftmost_j = len(M[0]) - 1
        for j in range(len(M[0])):
            if M[-i][j] != 0 and j < leftmost_j:
                leftmost_j = j
        for k in range(len(M) - i):
            factor = M[k][leftmost_j] / M[-i][leftmost_j]
            a[k] -= a[-i] * factor
            M[k][leftmost_j] -= factor
    return a
            
            
def create_element_vector(circ):
    global element_vector
    for item in circ.element_list:
        element_vector.append(item)
        if isinstance(item, (SERL, PARL)):
            create_element_vector(item)
            
            
def create_junction_matrix(circ):
    global element_vector, junction_matrix, junction_augmented_vector
    if isinstance(circ, SERL):
        for i in range(len(circ.element_list)):
            v = []
            for object in element_vector:
                v.append(0)
            if i == 0 and circ.element_list[0].type != 'blank':
                for j in range(len(element_vector)):
                    if circ == element_vector[j]: 
                        v[j] = 1
                    if circ.element_list[0] == element_vector[j]:
                        v[j] = -1
            else:
                if circ.element_list[i - 1].type != 'blank' and circ.element_list[i - 1].type != 'blank':
                    for j in range(len(element_vector)):
                        if circ.element_list[i - 1] == element_vector[j]:
                            v[j] = 1
                        if circ.element_list[i] == element_vector[j]:
                            v[j] = -1
            junction_matrix.append(v)
            junction_augmented_vector.append(0)
    if isinstance(circ, PARL):
        v = []
        for object in element_vector:
            v.append(0)
        for i in range(len(element_vector)):
            if circ == element_vector[i]: 
                v[i] = 1
            for j in range(len(element_vector)):
                if element_vector[i] in circ.element_list and element_vector[i].type != 'blank': 
                    v[i] = -1
        junction_matrix.append(v)
        junction_augmented_vector.append(0)
    for item in circ.element_list:
        if isinstance(item, (SERL, PARL)):
            create_junction_matrix(item)
            
            
def create_kirchoff_loops(circ):
    if isinstance(circ, SERL):
        KCLs = [[]]
        for item in circ.element_list:
            if isinstance(item, CIRCEL):
                for KCL in KCLs:
                    KCL.append(item)
            if isinstance(item, (SERL, PARL)):
                new_KCLs =  []
                for KCL in KCLs:
                    for sub_KCL in create_kirchoff_loops(item):
                        branched_KCL = KCL[:]
                        branched_KCL.extend(sub_KCL)
                        new_KCLs.append(branched_KCL)
                KCLs.extend(new_KCLs)
                KCLs.remove(KCL)
    if isinstance(circ, PARL):
        KCLs = []
        for item in circ.element_list:
            if isinstance(item, CIRCEL):
                KCLs.append([item])
            if isinstance(item, (SERL, PARL)):
                for sub_KCL in create_kirchoff_loops(item):
                    KCLs.append(sub_KCL)
    return KCLs


def create_kirchoff_matrix(circ):
    global HOTDOG_RESISTIVITY, element_vector, kirchoff_matrix, kirchoff_augmented_vector
    KCLs = create_kirchoff_loops(circ)
    for KCL in KCLs:
        v = []
        for _ in element_vector:
            v.append(0)
        value = 0
        has_blank = False
        for element in KCL:
            for i in range(len(element_vector)):
                if element == element_vector[i]:
                    if element.type == 'hotdog':
                        v[i] = HOTDOG_RESISTIVITY * element.val[1] / (element.val[0] ** 2 * pi)
                    if element.type == 'resistor':
                        v[i] = element.val
                    if element.type == 'battery':
                        value += element.val
                    if element.type == 'capacitor':
                        value -= element.charge / element.val
                    if element.type == 'inductor':
                        value -= element.val * -element.di / 1
                    if element.type == 'blank':
                        has_blank = True
        if not has_blank:
            kirchoff_matrix.append(v)
            kirchoff_augmented_vector.append(value)
    

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
def one_dog(voltage):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    return circ

######
# Hotdogs in Series
def dogs_ser(voltage,n):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    for i in range(n):
        circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    return circ

######
# Hotdogs in Parallel
def dogs_par(voltage,n):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    sub_circ = PARL([])
    for i in range(n):
        sub_circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    circ.add_element(sub_circ)
    return circ

######
# Hotdog and Resistor in Series
def dog_res_ser(voltage,resistance):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    circ.add_element(CIRCEL('resistor', resistance))
    return circ
    
######
# Hotdog and Resistor in Parallel
def dog_res_par(voltage,resistance):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    sub_circ = PARL([])
    sub_circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_circ.add_element(CIRCEL('resistor', resistance))
    circ.add_element(sub_circ)
    return circ

######
# Hotdog and Capacitor in Series
def dog_cap_ser(voltage, capacitance):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    circ.add_element(CIRCEL('capacitor', capacitance))
    return circ

######
# Hotdog and Capacitor in Parallel
def dog_cap_par(voltage,capacitance):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    sub_circ = PARL([])
    sub_circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_circ.add_element(CIRCEL('capacitor', capacitance))
    circ.add_element(sub_circ)
    return circ

######
# Hotdog and Inductor in Series
def dog_ind_ser(voltage,inductance):
    batt = CIRCEL("battery",voltage)
    circ = SERL([batt])
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    circ.add_element(CIRCEL('inductor', inductance))
    return circ


    
######
#Complex
def c_1():
    batt = CIRCEL("battery",120)
    circ = SERL([batt])
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_circ = PARL([])
    sub_circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_ser = SERL([])
    sub_par_2 = PARL([])
    sub_par_2.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_par_2.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_ser.add_element(sub_par_2)
    sub_ser.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    sub_circ.add_element(sub_ser)
    circ.add_element(sub_circ)
    circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
    return circ
    
circuit = c_1()
create_circuit(circuit)

######
# Hotdog and Inductor in Parallel
#def dog_ind_par(voltage, inductance):
##    batt = CIRCEL("battery",voltage)
##    circ = SERL([batt])
##    sub_circ = PARL([])
##    sub_circ.add_element(CIRCEL('hotdog', (0.01, 0.1)))
##    sub_circ.add_element(CIRCEL('inductor', inductance))
##    circ.add_element(sub_circ)
##    return circ
#    return c_1()

# Conencts presets to buttons
def presets(evt):
    global blanks, blanks_visual, circuit, circuit_visual, selected_circels, selected_objects, selected_labels, change_presets
    if not start:
        evt.color = color.white
        evt.background = color.black
        for button in change_presets:
            if button != evt and button.color == color.white:
                button.color = color.black
                button.background = color.white
        for i in range(len(selected_objects)):
            if find_index(selected_objects[i], circuit_visual) != 0:
                selected_circels.remove(selected_circels[i])
                selected_objects.remove(selected_objects[i])
                selected_labels[i].visible = False
                selected_labels.remove(selected_labels[i])
        blanks = []
        blanks_visual = []
        try:
            remove_circuit(circuit_visual)
        except TypeError:
            pass
        if evt.text == 'One Hotdog':
            circuit = one_dog(120, 1)
#            circuit = c_1()
        if evt.text == 'Hotdogs in Series':
            circuit = dogs_ser(120, 2)
        if evt.text == 'Hotdogs in Parallel':
            circuit = dogs_par(120, 2)
        if evt.text == 'Hotdog and Resistor in Series':
            circuit = dog_res_ser(120, 100)
        if evt.text == 'Hotdog and Resistor in Parallel':
            circuit = dog_res_par(120, 100)
        if evt.text == 'Hotdog and Capacitor in Series':
            circuit = dog_cap_ser(120, 10e-6)
        if evt.text == 'Hotdog and Capacitor in Parallel':
            circuit = dog_cap_par(120, 10e-6)
        if evt.text == 'Hotdog and Inductor in Series':
            circuit = dog_ind_ser(120, 10e-5)
        if evt.text == 'Hotdog and Inductor in Parallel':
            circuit = dog_ind_par(120, 10e-5)
        create_circuit(circuit)

##################
# CIRCUIT VISUALS
      

# Start simulation
def start_battery():
    global attatching, start, circuit, stepper, circuit_visuals
    if not attatching:
        try:
            if circel_count('battery', circuit) > 0:
                change_battery(circuit_visual, vec(255, 255, 179) / 255)
                start = True
                stepper = 0
        except TypeError:
            pass
    
    
def change_battery(e_visuals, new_color):
    if len(e_visuals) == 2 and isinstance(e_visuals[1], box):
        e_visuals[1].color = new_color
    for item in e_visuals:
        if isinstance(item, list):
            change_battery(item, new_color)
            

# Start simulation
def stop_battery():
    global attatching, start, circuit_visual
    if not attatching:
        start = False
        stepper = 0
        change_battery(circuit_visual, color.white)


# Creates a hotdog
def dog_visual():
    global attatching
    if not attatching:
        externals.append(CIRCEL('hotdog', (0.01, 0.1)))
        externals_visual.append(element_visual(externals[-1], create_mode = True))
        if circuit != None:
            reposition(externals_visual[-1] , vec(0, 0, circuit_visual[0].width / 2 + 10))
    
    
# Adjust the radius and length of a hotdog
def adjust_dog(evt):
    global attatching, externals, externals_visual, selected_circels, selected_objects, selected_labels
    if not attatching:
        for i in range(len(externals)):
            if externals[i].type == 'hotdog':
                last_dog_index = i
                select_circel = externals[i]
                select_dog = externals_visual[i]
        for i in range(len(selected_circels)):
            if selected_circels[i].type == 'hotdog':
                last_dog_index = i
                select_circel = selected_circels[i]
                select_dog = selected_objects[i]
        indices = [[last_dog_index, find_index(select_dog, circuit_visual, without_wires = False)]]
        if indices[0][1] == 0 or (indices[0][1] != 0 and not start):
            if evt.id is 'r':
                select_circel.val = (evt.value / 100, select_circel.val[1])
                for shape in select_dog:
                    shape.radius = evt.value
                select_dog[0].height = 2 * evt.value
                select_dog[0].width = 2 * evt.value
                rt.text = '{:1.2f}'.format(evt.value)
            if evt.id is 'l':
                select_circel.val = (select_circel.val[0], evt.value / 100)
                select_dog[0].length = evt.value
                select_dog[1].length = evt.value
                select_dog[1].pos = select_dog[0].pos - vec(evt.value / 2, 0, 0)
                select_dog[2].pos = select_dog[0].pos - vec(evt.value / 2, 0, 0)
                select_dog[3].pos = select_dog[0].pos + vec(evt.value / 2, 0, 0)
                lt.text = '{:1.2f}'.format(evt.value)
            for i in range(len(selected_circels)):
                if select_circel == selected_circels[i]:
                    selected_labels[i].visible = False
                    selected_labels[i] = label(pos = select_dog[0].pos, xoffset = max(select_dog[0].length, select_dog[0].width) / 2, yoffset = select_dog[0].height / 2, text = element_label(select_circel))
            if indices[0][1] != 0:
                selected_labels[last_dog_index].visible = False
                for i in range(len(selected_objects)):
                    if select_dog != selected_objects[i]:
                        index = find_index(selected_objects[i], circuit_visual, without_wires = False)
                        comb_index = [i, index]
                        if index != 0:
                            selected_labels[i].visible = False
                            indices.append(comb_index)
                remove_circuit(circuit_visual)
                create_circuit(circuit)
                for index in indices:
                    new_element = circuit_visual
                    for i in index[1]:
                        new_element = new_element[i]
                    for shape in new_element:
                        shape.emissive = True
                    selected_objects[index[0]] = new_element
                    selected_labels[index[0]] = label(pos = new_element[0].pos, xoffset = max(new_element[0].length, new_element[0].width) / 2, yoffset = new_element[0].height / 2, text = element_label(selected_circels[index[0]]))
        
        
# Adjust the values for an element using winput
def adjust_circel(evt):
    global attatching, circuit_visual, selected_circels, selected_objects, selected_labels
    if not (attatching or start):
        for i in range(len(selected_circels)):
            if selected_circels[i].type != 'hotdog':
                last_index = i
                circel = selected_circels[i]
                element = selected_objects[i]
        indices = [find_index(element, externals_visual)]
        if indices[0] != 0:
            circel.val = evt.number
            if circel.type == 'battery':
                for shape in element:
                    shape.length = circel.val
                    shape.height = circel.val
                    shape.width = circel.val
            if circel.type == 'capacitor':
                for shape in element:
                    shape.height = sqrt(circel.val)
                    shape.width = sqrt(circel.val)
            if circel.type == 'inductor':
                N = 15 - exp(-sqrt(circel.val) / 50 + log(15)) + 5
                a = (N % 1) * 2 * pi
                element[1].coils = N
                element[3].pos = element[2].pos + vec(10, 0, 0)  + 4 * vec(0, sin(a), cos(a) - 1)
            selected_labels[last_index].visible = False
            selected_labels[last_index] = label(pos = element[0].pos, xoffset = max(element[0].length, element[0].width) / 2, yoffset = element[0].height / 2, text = element_label(circel))
        indices = [[last_index, find_index(element, circuit_visual, without_wires = False)]]
        if indices[0][1] != 0:
            selected_labels[last_index].visible = False
            circel.val = evt.number
            for i in range(len(selected_objects)):
                if element != selected_objects[i]:
                    index = find_index(selected_objects[i], circuit_visual, without_wires = False)
                    comb_index = [i, index]
                    if index != 0:
                        selected_labels[i].visible = False
                        indices.append(comb_index)
            remove_circuit(circuit_visual)
            create_circuit(circuit)
            for index in indices:
                new_element = circuit_visual
                for i in index[1]:
                    new_element = new_element[i]
                for shape in new_element:
                    shape.emissive = True
                selected_objects[index[0]] = new_element
                selected_labels[index[0]] = label(pos = new_element[0].pos, xoffset = max(new_element[0].length, new_element[0].width) / 2, yoffset = new_element[0].height / 2, text = element_label(selected_circels[index[0]]))
    
    
# Starts element attatchment method
def attatch_object(evt):
    global attatching, stepper, selected_circels, selected_objects, selected_labels
    evt.checked = not start
    if attatching and not evt.checked:
        for object in selected_objects:
            for shape in object[1:]:
                shape.emissive = False
                shape.opacity = 1
        selected_objects = []
        for l in selected_labels:
            l.visible = False
        selected_labels = []
        selected_circels = []
        attatching = False
        attatch_check.checked = False
    attatching = evt.checked
    stepper = 0
    
    
# Presets of element visuals based on the type
def element_visual(e, create_mode):
    if e.type == 'blank':
        L, H, W = e.val
        visual = [box(pos = vec(0, 0, 0), length = L, height = H, width = W, visible = False)]
        visual.append(cone(pos = vec(-L/2, 0, 0), axis = vec(1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
        visual.append(cone(pos = vec(L/2, 0, 0), axis = vec(-1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
    if e.type == 'hotdog':
        R, L = e.val
        R *=  100
        L *=  100
        visual = [
            box(pos = vec(0, 0, 0), length = L, height = max(1.5, 2 * R), width = max(1.5, 2 * R), opacity = 0), 
            cylinder(pos = vec(-L/2, 0, 0), length = L, radius = R, axis = vec(1, 0, 0), color = color.red, color = vec(245, 214, 235) / 255),
            sphere(pos = vec(-L/2, 0, 0), radius = R, color = color.red, color = vec(245, 214, 235) / 255),
            sphere(pos =  vec(L/2, 0, 0), radius = R, color = color.red, color = vec(245, 214, 235) / 255)]
        if not create_mode:
            visual[0].length += 6
            visual.append(cone(pos = vec(-L/2 - 3, 0, 0), axis = vec(1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
            visual.append(cone(pos = vec(L/2 + 3, 0, 0), axis = vec(-1, 0, 0), radius = 0.75, length = 5, color = vec(112, 128, 144) / 255))
    if e.type == 'battery':
        V = e.val
        V = min(V, 20)
        V = max(V, 2)
        visual = [
            box(pos = vec(0, 0, 0), length = V, height = V, width = V, opacity = 0),
            box(pos = vec(0, 0, 0), axis = vec(1, 0, 0), length = V, height = V, width = V)]
    if e.type == 'resistor':
        R = e.val
        visual = [
            box(pos = vec(0, 0, 0), length = 9, height = 3.2, width = 3.2, opacity = 0),
            cylinder(pos = vec(-3, 0, 0), length = 6, radius = 1, axis = vec(1, 0, 0), color = color.cyan),
            cylinder(pos = vec(-3.25, 0, 0), length = 0.5, radius = 1.6, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(-1.5, 0, 0), length = 0.5, radius = 1.1, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(0, 0, 0), length = 0.5, radius = 1.1, axis = vec(1, 0, 0), color = color.black),
            cylinder(pos = vec(2.75, 0, 0), length = 0.5, radius = 1.6, axis = vec(1, 0, 0), color = color.black),
            sphere(pos = vec(-3, 0, 0), radius = 1.5, color = color.cyan),
            sphere(pos =  vec(3, 0, 0), radius = 1.5, color = color.cyan)]
    if e.type == 'capacitor':
        C = e.val
        C *= 10e6
        C = min(C, 20)
        C = max(C, 1)
        visual = [
            box(pos = vec(0, 0, 0), length = 6, height = sqrt(C), width = sqrt(C), opacity = 0),
            box(pos = vec(2, 0, 0), axis = vec(1, 0, 0), length = 2, height = sqrt(C), width = sqrt(C), color = color.red),
            box(pos = vec(-2, 0, 0), axis = vec(-1, 0, 0), length = 2, height = sqrt(C), width = sqrt(C), color = color.blue)]
    if e.type == 'inductor':
        L = e.val
        L *= 10e5
        N = 15 - exp(-sqrt(L) / 50 + log(15)) + 5
        a = (N % 1) * 2 * pi
        visual = [
            box(pos = vec(0, 0, 0), length = 10, height = 8.8, width = 8.8, opacity = 0),
            helix(pos = vec(-5, 0, 0), axis = vec(1, 0, 0), length = 10, coils = N, radius = 4, thickness = 0.8, color = color.black),
            cylinder(pos = vec(-5, 0, 4), axis = vec(0, 0, -1), length = 4, radius = 0.4, color = color.black),
            cylinder(pos = vec(5, 0, 4) + 4 * vec(0, sin(a), cos(a) - 1), axis = vec(0, -sin(a), -cos(a)), length = 4, radius = 0.4, color = color.black)]
    return visual
    
    
# Presets of element visuals based on the type
def element_label(e):
    c = e.current 
    if e.type == 'hotdog':
        R, L = e.val
        T = e.temperature
        return 'Radius: ' + R + ' m\nLength: ' + L + ' m\nCurrent: ' + c + ' A\nTemperature: ' + T + ' K' 
    if e.type == 'battery':
        V = e.val
        return 'Voltage: ' + V + ' V\nCurrent: ' + c + ' A'
    if e.type == 'resistor':
        R = e.val
        return 'Resistance: ' + R + ' Ω\nCurrent: ' + c + ' A'
    if e.type == 'capacitor':
        C = e.val
        Q = e.charge
        return 'Capacitance: ' + C + ' F\nCurrent: ' + c + ' A\nCharge: ' + Q + ' C'
    if e.type == 'inductor':
        L = e.val
        return 'Inductance: ' + L + ' H\nCurrent: ' + c + ' A'
        
        
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
    

# Checks if the circuit contains only one element
def get_single_element(circel_list):
    if isinstance(circel_list[0], CIRCEL):
        return circel_list[0]
    else:
        return get_single_element(circel_list[0])
  
  
# Counts elements in circuit     
def item_count(circel_list):
    items = 0
    for item in circel_list:
        if isinstance(item, (SERL, PARL)):
            items += item_count(item.element_list)
        else:
            items += 1
    return items


# Recursively translates all shapes in a nested list
def reposition(e_visuals, translation):
    for item in e_visuals:
        if not isinstance(item, (curve, box, cone, sphere, helix, cylinder)):
            reposition(item, translation)
        else:
            if isinstance(item, curve):
                for n in range(item.npoints):
                    item.modify(n, pos = item.point(n)['pos'] + translation)
            else:
                item.pos +=  translation
                
                
# Recursively creates the central circuit     
def create_sub_circuit(circ):
    global blanks_visual
    elements = circ.element_list
    e_visuals = []
    for e in elements:
        if isinstance(e, CIRCEL):
            element = element_visual(e)
            if e.type == 'blank':
                blanks_visual.append(element)
            if isinstance(circ, PARL) and len(elements) > 1:
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
            else:
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
            e_visuals.append(element)
        else:
            if item_count(e.element_list) > 0:
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
        single = 0
        for item in elements:
            if isinstance(item, CIRCEL):
                single += 1
            elif item_count(item.element_list) > 0:
                single += 1
        if single > 1:
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
    return e_visuals
 
 
# Creates the circuit
def create_circuit(circ):
    global circuit_visual
    if len(circ.element_list) > 0:
        circuit_visual = create_sub_circuit(circ)
    if circ.type == 'SERL' and circ != None:
        if len(circ.element_list) > 0:
            circuit_visual = circuit_loop(circuit_visual)
        
        
# Finds the element with the shape in it
def find_visual(shape, e_visual):
    if e_visual != None:
        if isinstance(shape, (box, cone, sphere, helix, cylinder)):
            for element in e_visual:
                if shape in element:
                    return element
                if isinstance(element, list):
                    found = find_visual(shape, element)
                    if found != 0:
                        return found
    return 0
    
        
# Finds the index of the elements within the nested circuit structure
def find_index(element, e_visual, without_wires = True):
    wire_offset = 0
    if e_visual != None:
        for i in range(len(e_visual)):
            if isinstance(e_visual[i][1], curve) and without_wires:
                wire_offset += 1
            current = [i - wire_offset]
            if e_visual[i] == element:
                return current
            if isinstance(e_visual[i], list):
                found = find_index(element, e_visual[i], without_wires)
                if found != 0:
                    current.extend(found)
                    return current
    return 0
    
    
# Finds all the hotdogs in a circuit    
def find_dogs(circ):
    dogs = []
    if circ != None:
        for item in circ.element_list:
            if item.type == 'hotdog':
                dogs.append(item)
            if isinstance(item, (SERL, PARL)):
                dogs.extend(find_dogs(item))
    return dogs
    
    
# Finds all the hotdogs in a circuit    
def find_dogs_visual(e_visual):
    dogs_visual = []
    if e_visual != None:
        for element in e_visual:
            if isinstance(element[2], sphere):
                dogs_visual.append(element)
            elif isinstance(element, list):
                dogs_visual.extend(find_dogs_visual(element))
    return dogs_visual
    

# Finds the nearest upper level that contains a sub circuit
def find_contains(circel, circ):
    if circ != None:
        for item in circ.element_list:
            if circel == item:
                return circ
            elif isinstance(item, (SERL, PARL)):
                result = find_contains(circel, item)
                if result != 0:
                    return result
    return 0
 
 
# Returns count of an element type in the circuit
def circel_count(circel_type, circ):
    count = 0
    if circ != None:
        for item in circ.element_list:
            if item.type == circel_type:
                count += 1
            if isinstance(item, (SERL, PARL)):
                count += circel_count(circel_type, item)
    return count
    
# Returns a copy of an element
def clone_element(element):
    element_clone = []
    for shape in element:
        element_clone.append(shape.clone())
    return element_clone
 

# Removes an element from the circuit
def remove_circel(circel, circ):
    if circ != None:
        for item in circ.element_list:
            if item == circel:
                circ.element_list.remove(item)
                return
            elif isinstance(item, (SERL, PARL)):
                remove_circel(circel, item)
                if len(item.element_list) == 0:
                    circ.element_list.remove(item)
                
                
# Replaces an element with another                
def replace_circel(replacing_circel, replaced_circel, circ):
    if circ != None:
        for i in range(len(circ.element_list)):
            if circ.element_list[i] == replaced_circel:
                circ.element_list[i] = replacing_circel
                return
            elif isinstance(circ.element_list[i] , (SERL, PARL)):
                replace_circel(replacing_circel, replaced_circel, circ.element_list[i])
                

# Destroys the current circuit visual                
def remove_circuit(e_visual):
    if e_visual != None:
        for item in e_visual:
            if isinstance(item, (curve, box, cone, sphere, helix, cylinder)):
                item.visible = False
            if isinstance(item, list):
                remove_circuit(item)
    
                
def check_full(circel_list, circ):
    global selected_highest_level, selected_secondary_level
    selected_secondary_level = []
    sub_full = 0
    if circ != None:
        element_full = len(circ.element_list)
        for item in circ.element_list:
            if isinstance(item, (SERL, PARL)):
                s = check_full(circel_list, item)
                if s[1] > 0:
                    selected_secondary_level.append(item)
                element_full += s[0]
                sub_full += s[1]
            if isinstance(item, CIRCEL):
                if item in circel_list:
                    selected_secondary_level.append(item)
                    sub_full += 1
                else:
                    element_full -= 1
        if sub_full == len(circel_list):
            selected_highest_level = circ
            raise TypeError()
        else:
            selected_secondary_level = []
        if len(circ.element_list) == element_full:
            return (0, sub_full)
        else:
            return (-1, 0)
        return (-1, 0)
        
        
while (True):
    rate(frame_rate)
#    dt = 1 / frame_rate
#    dt = 0.2
    shape = scene.mouse.pick
    if start:
        change_battery(circuit_visual, vec(255, 255, 179) / 255)
        time += 1
        dogs = find_dogs(circuit)
        dogs_visual = find_dogs_visual(circuit_visual)
        # Euler's 
        if speeder * time % frame_rate == 0:
            element_vector = []
            element_vector.append(circuit)
            create_element_vector(circuit)
            junction_matrix = []
            junction_augmented_vector = []
            create_junction_matrix(circuit)
            kirchoff_matrix = []
            kirchoff_augmented_vector = []
            create_kirchoff_matrix(circuit)
            current_matrix = []
            current_matrix.extend(junction_matrix)
            current_matrix.extend(kirchoff_matrix)
            augmented_vector = []
            augmented_vector.extend(junction_augmented_vector)
            augmented_vector.extend(kirchoff_augmented_vector)
            augmented_vector = RREF(current_matrix, augmented_vector)
            for i in range(len(element_vector)):
                if element_vector[i].type == 'inductor':
                    element_vector[i].di = abs(element_vector[i].current - element_vector[i].current) / dt
                if i < len(augmented_vector):
                    element_vector[i].current = augmented_vector[i]
                else:
                    element_vector[i].current = 0
                if element_vector[i].type == 'capacitor':
                    element_vector[i].charge += element_vector[i].current * dt
            for i in range(len(dogs)):
                dE = dogs[i].current ** 2 * HOTDOG_RESISTIVITY * dogs[i].val[1] / (dogs[i].val[0] ** 2 * pi)
                dK = dE / (dogs[i].val[1] * (dogs[i].val[0] ** 2 * pi) * HOTDOG_DENSITY * HOTDOG_SPECIFIC_HEAT) 
                dogs[i].temperature += dK
                if dogs[i].temperature > 373:
                    for shape in dogs_visual[i][1:4]:
                        shape.texture = None
                        shape.color = color.black
                elif dogs[i].temperature > 353:
                    dogs_visual[i][1].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_charred_texture.png"
                    dogs_visual[i][2].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_charred_cap.png"
                    dogs_visual[i][3].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_charred_cap.png"
                elif dogs[i].temperature > 333:
                    dogs_visual[i][1].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_perfect_texture.png"
                    dogs_visual[i][2].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_perfect_cap.png"
                    dogs_visual[i][3].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_perfect_cap.png"
                elif dogs[i].temperature > 313:
                    dogs_visual[i][1].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_undercooked_texture.png"
                    dogs_visual[i][2].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_undercooked_texture.png"
                    dogs_visual[i][3].texture = "https://raw.githubusercontent.com/nchan50/BestDog/refs/heads/main/hotdog_undercooked_texture.png"
            for i in range(len(selected_circels)):
                selected_labels[i].visible = False
                selected_labels[i] = label(pos = selected_objects[i][0].pos, xoffset = max(selected_objects[i][0].length, selected_objects[i][0].width) / 2, yoffset = selected_objects[i][0].height / 2, text = element_label(selected_circels[i]))
            if len(selected_circels) > 0:
                try:
                    graphed_circel = selected_circels[-1]
                    data_curves[0].plot(time / frame_rate, graphed_circel.current)
                    if graphed_circel.type == 'hotdog':
                        data_curves[1].plot(time / frame_rate, graphed_circel.temperature)
                except TypeError:
                    pass
            
    # Attatching an element to the circuit
    if attatching and not start:
        if len(externals) == 0:
            alert('No elements to attatch with')
            attatching = False
            attatch_check.checked = False
            continue
        if stepper == 0:
            for object in selected_objects:
                for shape in object[1:]:
                    shape.emissive = False
                    shape.opacity = 1
            selected_objects = []
            for l in selected_labels:
                l.visible = False
            selected_labels = []
            selected_circels = []
            alert('Select one element from outside the circuit')
            stepper += 1
        if stepper == 1:
            if select:
                element = find_visual(shape, externals_visual)
                if element != 0:
                    index = find_index(element, externals_visual)
                    circel = externals[index[0]]
                    if circel.type == 'blank':
                        select = False
                        continue
                    if circel.type == 'battery':
                        if circel_count('battery', circuit) >= max_battery:
                            alert('Cannot add another battery. Limit of ' + max_battery + '.')
                            select = False
                            continue
                    if circel.type == 'capacitor':
                         if circel_count('capacitor', circuit) >= max_capacitor:
                            alert('Cannot add another capacitor. Limit of ' + max_capacitor + '.')
                            select = False
                            continue
                    if circel.type == 'inductor':
                        if circel_count('battery', circuit) >= max_inductor:
                            alert('Cannot add another inductor. Limit of '+  max_inductorr + '.')
                            select = False
                            continue
                    for shape in element[1:]:
                        shape.emissive = True
                        shape.opacity = 0.3
                    selected_objects.append(element)
                    selected_circels.append(circel)
                    selected_labels.append(label(pos = element[0].pos, xoffset = max(element[0].length, element[0].width) / 2, yoffset = element[0].height / 2, text = element_label(circel)))
                    stepper += 1
                    select = False
        if stepper == 2:
            alert('Select elements from inside the circuit')
            stepper += 1
        if stepper == 3:
            if select:
                element = find_visual(shape, circuit_visual)
                if element != 0 :
                    for shape in element[1:]:
                        shape.emissive = True
                        shape.opacity = 0.3
                    index = find_index(element, circuit_visual)
                    circel = circuit
                    for i in index:
                        circel = circel.element_list[i - 1]
                    if circel.type != 'blank':
                        if circel not in selected_circels:
                            selected_objects.append(element)
                            selected_circels.append(circel)
                            selected_labels.append(label(pos = element[0].pos, xoffset = max(element[0].length, element[0].width) / 2, yoffset = element[0].height / 2, text = element_label(circel)))
                        else:
                            for i in range(len(selected_circels)):
                                if selected_circels[i] == circel:
                                    selected_circels.remove(selected_circels[i])
                                    selected_labels[i].visible = False
                                    selected_labels.remove(selected_labels[i])
                                    for shape in selected_objects[i][1:]:
                                        shape.emissive = False
                                        shape.opacity = 1
                                    selected_objects.remove(selected_objects[i])
                select = False
            if breaker:
                try:
                    check_full(selected_circels[1:], circuit)[1] > 0
                    alert('Not a viable set to connect to')
                except TypeError: 
                    stepper += 1
                breaker = False
        if stepper == 4:
            SERL_PARL = input('Connect in series(SERL) or parallel(PARL) or EXIT: ')
            if SERL_PARL == 'SERL' or SERL_PARL == 'PARL':
                stepper += 1
            elif SERL_PARL == 'EXIT':
                stepper -= 1
            else:
                alert('Invalid input')
        if stepper == 5:
            if SERL_PARL == selected_highest_level.type:
                selected_highest_level.add_element(selected_circels[0])
            else:
                if SERL_PARL == 'SERL':
                    new_sub_circ = SERL([])
                if SERL_PARL == 'PARL':
                    new_sub_circ = PARL([])
                if len(selected_secondary_level) == len(selected_highest_level.element_list):
                    new_sub_circ.add_element(selected_highest_level)
                    if selected_highest_level != circuit:
                        circuit_level = find_contains(selected_highest_level, circuit)
                        circuit_level.element_list.remove(selected_highest_level)
                        circuit_level.add_element(new_sub_circ)
                    else:
                        circuit = new_sub_circ
                else:
                    if SERL_PARL == 'SERL':
                        sub_circ = PARL([])
                    if SERL_PARL == 'PARL':
                        sub_circ = SERL([])
                    for secondary in selected_secondary_level:
                        sub_circ.add_element(secondary)
                        selected_highest_level.element_list.remove(secondary)
                    new_sub_circ.add_element(sub_circ)
                    selected_highest_level.add_element(new_sub_circ)
                new_sub_circ.add_element(selected_circels[0])
            remove_circuit(circuit_visual)
            create_circuit(circuit)
            for shape in selected_objects[0]:
                shape.visible = False
            selected_objects.remove(selected_objects[0])
            for object in selected_objects:
                for shape in object[1:]:
                    shape.emissive = False
                    shape.opacity = 1
            selected_objects = []
            for l in selected_labels:
                l.visible = False
            selected_labels = []
            selected_circels = []
            attatching = False
            stepper = 0
            attatch_check.checked = False
        continue

    # Dragging elements and removing them from the circuit
    if drag:
        position = scene.mouse.pos
        for i in range(len(selected_labels)):
            selected_labels[i].pos = selected_objects[i][0].pos
        if dragged_object == None:
            element = find_visual(shape, externals_visual)
            if element != 0:
                index = find_index(element, externals_visual)
                circel = externals[index[0]]
                if not start or circel.type == 'hotdog' and circel.type != 'blank':
                    dragged_object = element
                    reposition(dragged_object, position - dragged_object[0].pos)
                    for blank_visual in blanks_visual:
                        if mag(blank_visual[0].pos - position) < 5:
                            blank_index = find_index(blank_visual, circuit_visual)
                            blank_visual_index = find_index(blank_visual, circuit_visual, without_wires = False)
                            blank = circuit
                            for i in blank_index:
                                blank = blank.element_list[i - 1]
                            externals.remove(circel)
                            for shape in element:
                                shape.visible = False
                            externals_visual.remove(element)
                            replace_circel(circel, blank, circuit)
                            blanks_visual.remove(blank_visual)
                            remove_circuit(circuit_visual)
                            create_circuit(circuit)
                            object = circuit_visual
                            for i in blank_visual_index:
                                object = object[i]
                            for i in range(len(selected_objects)):
                                if selected_objects[i] == element:
                                    selected_circels.remove(selected_circels[i])
                                    selected_objects.remove(element)
                                    selected_labels[i].visible = False
                                    selected_labels.remove(selected_labels[i])
            element = find_visual(shape, circuit_visual)
            if element != 0:
                index = find_index(element, circuit_visual)
                circel = circuit
                circel.current = 0
                for i in index:
                    circel = circel.element_list[i - 1]
                if not start or circel.type == 'hotdog' and circel.type != 'blank':
                    object = clone_element(element)
                    if not start:
                        remove_circel(circel, circuit)
                    else:
                        blank = CIRCEL('blank', (element[0].length, element[0].height, element[0].width))
                        blanks.append(blank)
                        replace_circel(blank, circel, circuit)
                    remove_circuit(circuit_visual)
                    externals.append(circel)
                    if circel.type == 'hotdog':
                        object[4].visible = False
                        object[5].visible = False
                        object = object[:4]
                        object[0].length -= 6
                    externals_visual.append(object)
                    create_circuit(circuit)
                    dragged_object = object
                    reposition(dragged_object, position - dragged_object[0].pos)
                    for i in range(len(selected_objects)):
                        if selected_objects[i] == element:
                            selected_objects[i] = object
                continue
        else:
            reposition(dragged_object, position - dragged_object[0].pos)
            continue
    dragged_object = None

    # Selecting Elements and displaying their data
    if select:
        element = find_visual(shape, externals_visual)
        if element != 0:
            index = find_index(element, externals_visual)
            circel = externals[index[0]]
            if circel.type != 'blank':
                for shape in element:
                    shape.emissive = True
                index = find_index(element, externals_visual)
                if circel not in selected_circels:
                    selected_objects.append(element)
                    selected_circels.append(circel)
                    selected_labels.append(label(pos = element[0].pos, xoffset = max(element[0].length, element[0].width) / 2, yoffset = element[0].height / 2, text = element_label(circel)))
                else:
                    for shape in element:
                        shape.emissive = False
                    selected_objects.remove(element)
                    for i in range(len(selected_circels)):
                        if selected_circels[i] == circel:
                            selected_labels[i].visible = False
                            selected_labels.remove(selected_labels[i])
                    selected_circels.remove(circel)
        element = find_visual(shape, circuit_visual)
        if element != 0:
            index = find_index(element, circuit_visual)
            circel = circuit
            for i in index:
                circel = circel.element_list[i - 1]
            if circel.type != 'blank':
                for shape in element:
                    shape.emissive = True
                if circel not in selected_circels:
                    selected_objects.append(element)
                    selected_circels.append(circel)
                    selected_labels.append(label(pos = element[0].pos, xoffset = max(element[0].length, element[0].width) / 2, yoffset = element[0].height / 2, text = element_label(circel)))
                    if start:
                        for data_graph in data_graphs:
                            data_graph.delete()
                        data_graphs = []
                        data_curves = []
                        current_graph = graph(title = 'Current v.s. Time', xtitle = 'Time(s)', ytitle = 'Current(A)')
                        current_curve = gcurve(graph = current_graph)
                        data_graphs.append(current_graph)
                        data_curves.append(current_curve)
                        if circel.type == 'hotdog':
                            temperature_graph = graph(title = 'Temperature v.s. Time', xtitle = 'Time(s)', ytitle = 'Temperature(K)')
                            temperature_curve = gcurve(label = 'Temperature v.s. Time', graph = temperature_graph)
                            data_graphs.append(temperature_graph)
                            data_curves.append(temperature_curve)
                else:
                    for shape in element:
                        shape.emissive = False
                    selected_objects.remove(element)
                    for i in range(len(selected_circels)):
                        if selected_circels[i] == circel:
                            selected_labels[i].visible = False
                            selected_labels.remove(selected_labels[i])
                    selected_circels.remove(circel)
        select = False
        select = False
