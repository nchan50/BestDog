Web VPython 3.2

scene.autoscale = False
sphere(pos=vector(0,0,0),texture="https://raw.githubusercontent.com/nchan50/BestDog/blob/main/the_noble_hot_dog.png",radius=200,shininess=0)

dogs = []

immutable = True

def create_dog():
    global immutable
    if immutable:
        dogs.append(cylinder(pos=vec(0, 0, 0), axis=vec(1, 1, 1), color=color.red))
    immutable = False
    print(len(dogs))
    
def adjust_dog(evt):
    if evt.id is 'r' and not immutable:
        dogs[-1].radius = evt.value
        rt.text = '{:1.2f}'.format(evt.value)
    if evt.id is 'l' and not immutable:
        dogs[-1].length = evt.value
        lt.text = '{:1.2f}'.format(evt.value)

def save_dog():
    global immutable
    dogs[-1].pos()
    immutable = True

scene.caption = 'Create Your Hot Dog: '
button(bind = create_dog, text= 'Create me!')
scene.append_to_caption('\n')
rs = slider(bind = adjust_dog, max = 5, min = 0.5, step = 0.1, value = 1, id = 'r')
scene.append_to_caption('Radius: ')
rt = wtext(text='{:1.2f}'.format(rs.value))
scene.append_to_caption(' m\n')
ls = slider(bind = adjust_dog, max = 5, min = 0.5, step = 0.1, value = 1, id = 'l')
scene.append_to_caption('Length: ')
lt = wtext(text='{:1.2f}'.format(ls.value))
scene.append_to_caption(' m\n')
button(bind = save_dog, text= 'Save me!')
