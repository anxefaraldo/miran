import OSC
import Tkinter
import threading

# OSC
# ===

s1 = 1

c = OSC.OSCClient()
c.connect(('localhost', 7113))
s = OSC.ThreadingOSCServer(('localhost', 7111))
s.addDefaultHandlers() # register a 'default' handler (for unmatched messages)



def receive_OSC(addr, tags, stuff, source):
    print addr, stuff[0]
    if addr=="/tempo":
        v_tempo.set(stuff[0])
    if addr=="/density":
        v_density.set(stuff[0])
    if addr=="/legato":
        v_legato.set(stuff[0])
    if addr=="/saturation":
        v_saturation.set(stuff[0])
    if addr=="/substitution":
        v_substitution.set(stuff[0])
    if addr=="/activity":
        v_activity.set(stuff[0])
    if addr=="/register":
        v_register.set(stuff[0])

s.addMsgHandler("/tempo", receive_OSC)
s.addMsgHandler("/density", receive_OSC)
s.addMsgHandler("/legato", receive_OSC)
s.addMsgHandler("/saturation", receive_OSC)
s.addMsgHandler("/substitution", receive_OSC)
s.addMsgHandler("/activity", receive_OSC)
s.addMsgHandler("/register", receive_OSC)

# GRAPHICAL USER INTERFACE
# ========================

window = Tkinter.Tk()

v_tempo = Tkinter.IntVar()
v_density = Tkinter.IntVar()
v_legato = Tkinter.DoubleVar()
v_saturation = Tkinter.DoubleVar()
v_substitution = Tkinter.DoubleVar()
v_activity = Tkinter.DoubleVar()
v_register = Tkinter.IntVar()

def send_OSC(value):
        msg = OSC.OSCMessage()
        msg.setAddress("/tempo")
        msg.append(value)
        c.send(msg)
        print value

def send_tempo(value):
        msg = OSC.OSCMessage()
        msg.setAddress("/density")
        msg.append(value)
        c.send(msg)
        print value


v_tempo.set(125)
v_density.set(4)
v_legato.set(0)
v_saturation.set(0)
v_substitution.set(0)
v_activity.set(0)
v_register.set(1)

# DECLARE WIDGETS
# ===============

window.title('House Harmonic Filler')
s
s_tempo = Tkinter.Scale(orient='horizontal',
                        length=300,
                        from_=40,
                        to=302,
                        showvalue='true',
                        variable=v_tempo,
                        command=send_tempo)
s_density = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=1,
                        from_=1,
                        to=32,
                        showvalue='true',
                        variable=v_density,
                        command=send_OSC)
s_legato = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0.00,
                        to=1.00,
                        showvalue='true',
                        variable=v_legato,
                        command=send_OSC)
s_saturation = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_saturation,
                        command=send_OSC)
s_substitution = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_substitution,
                        command=send_OSC)
s_activity = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_activity,
                        command=send_OSC)
s_register = Tkinter.Scale(orient='horizontal',
                        resolution=1,
                        length=180,
                        from_=1,
                        to=4,
                        showvalue='true',
                        variable=v_register,
                        command=send_OSC)



b_load = Tkinter.Button(text="Load MIDI File",width=15)
b_play = Tkinter.Button(text="Play",width=5)

l_density = Tkinter.Label(text='Density', font=('Arial', 10))
l_legato = Tkinter.Label(text='Legato', font=('Arial', 10))
l_saturation = Tkinter.Label(text='Chord Saturation', font=('Arial', 10))
l_substitution = Tkinter.Label(text='Substitution Distance', font=('Arial', 10))
l_activity = Tkinter.Label(text='Voicing Activity', font=('Arial', 10))
l_register = Tkinter.Label(text='Register Expansion', font=('Arial', 10))
l_tempo = Tkinter.Label(text='Tempo', font=('Arial', 10))

t_inversion = Tkinter.Checkbutton(text="Allow Inversions")

# VISUAL LAYOUT
# =============

b_load.grid(row=0, column=0, sticky='WS')
b_play.grid(row=0, column=1,sticky='WS')

l_tempo.grid(row=1, column=0, sticky='ES')
s_tempo.grid(row=1, column=1, sticky='W')

l_density.grid(row=2, column=0, sticky='ES')
s_density.grid(row=2, column=1, columnspan=2)

l_legato.grid(row=3, column=0, sticky='ES')
s_legato.grid(row=3, column=1, columnspan=2)

l_saturation.grid(row=4, column=0, sticky='ES')
s_saturation.grid(row=4, column=1, columnspan=2)

l_substitution.grid(row=5, column=0, sticky='ES')
s_substitution.grid(row=5, column=1, columnspan=2)

l_activity.grid(row=6, column=0, sticky='ES')
s_activity.grid(row=6, column=1, columnspan=2)

l_register.grid(row=7, column=0, sticky='ES')
s_register.grid(row=7, column=1, sticky='W')

t_inversion.grid(row=7, column=1, sticky='ES')

# MAIN FUNCTION

def main():
    print "Starting OSCServer"
    st = threading.Thread(target=s.serve_forever)
    st.start()
    window.mainloop()
main()

import OSC
import Tkinter
import threading

# OSC
# ===

s1 = 1

c = OSC.OSCClient()
c.connect(('localhost', 7113))
s = OSC.ThreadingOSCServer(('localhost', 7111))
s.addDefaultHandlers() # register a 'default' handler (for unmatched messages)



def receive_OSC(addr, tags, stuff, source):
    print addr, stuff[0]
    if addr=="/tempo":
        v_tempo.set(stuff[0])
    if addr=="/density":
        v_density.set(stuff[0])
    if addr=="/legato":
        v_legato.set(stuff[0])
    if addr=="/saturation":
        v_saturation.set(stuff[0])
    if addr=="/substitution":
        v_substitution.set(stuff[0])
    if addr=="/activity":
        v_activity.set(stuff[0])
    if addr=="/register":
        v_register.set(stuff[0])

s.addMsgHandler("/tempo", receive_OSC)
s.addMsgHandler("/density", receive_OSC)
s.addMsgHandler("/legato", receive_OSC)
s.addMsgHandler("/saturation", receive_OSC)
s.addMsgHandler("/substitution", receive_OSC)
s.addMsgHandler("/activity", receive_OSC)
s.addMsgHandler("/register", receive_OSC)

# GRAPHICAL USER INTERFACE
# ========================

window = Tkinter.Tk()

v_tempo = Tkinter.IntVar()
v_density = Tkinter.IntVar()
v_legato = Tkinter.DoubleVar()
v_saturation = Tkinter.DoubleVar()
v_substitution = Tkinter.DoubleVar()
v_activity = Tkinter.DoubleVar()
v_register = Tkinter.IntVar()

def send_OSC(value):
        msg = OSC.OSCMessage()
        msg.setAddress("/tempo")
        msg.append(value)
        c.send(msg)
        print value

def send_tempo(value):
        msg = OSC.OSCMessage()
        msg.setAddress("/density")
        msg.append(value)
        c.send(msg)
        print value


v_tempo.set(125)
v_density.set(4)
v_legato.set(0)
v_saturation.set(0)
v_substitution.set(0)
v_activity.set(0)
v_register.set(1)

# DECLARE WIDGETS
# ===============

window.title('House Harmonic Filler')
s
s_tempo = Tkinter.Scale(orient='horizontal',
                        length=300,
                        from_=40,
                        to=302,
                        showvalue='true',
                        variable=v_tempo,
                        command=send_tempo)
s_density = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=1,
                        from_=1,
                        to=32,
                        showvalue='true',
                        variable=v_density,
                        command=send_OSC)
s_legato = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0.00,
                        to=1.00,
                        showvalue='true',
                        variable=v_legato,
                        command=send_OSC)
s_saturation = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_saturation,
                        command=send_OSC)
s_substitution = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_substitution,
                        command=send_OSC)
s_activity = Tkinter.Scale(orient='horizontal',
                        length=300,
                        resolution=0.01,
                        from_=0,
                        to=1,
                        showvalue='true',
                        variable=v_activity,
                        command=send_OSC)
s_register = Tkinter.Scale(orient='horizontal',
                        resolution=1,
                        length=180,
                        from_=1,
                        to=4,
                        showvalue='true',
                        variable=v_register,
                        command=send_OSC)



b_load = Tkinter.Button(text="Load MIDI File",width=15)
b_play = Tkinter.Button(text="Play",width=5)

l_density = Tkinter.Label(text='Density', font=('Arial', 10))
l_legato = Tkinter.Label(text='Legato', font=('Arial', 10))
l_saturation = Tkinter.Label(text='Chord Saturation', font=('Arial', 10))
l_substitution = Tkinter.Label(text='Substitution Distance', font=('Arial', 10))
l_activity = Tkinter.Label(text='Voicing Activity', font=('Arial', 10))
l_register = Tkinter.Label(text='Register Expansion', font=('Arial', 10))
l_tempo = Tkinter.Label(text='Tempo', font=('Arial', 10))

t_inversion = Tkinter.Checkbutton(text="Allow Inversions")

# VISUAL LAYOUT
# =============

b_load.grid(row=0, column=0, sticky='WS')
b_play.grid(row=0, column=1,sticky='WS')

l_tempo.grid(row=1, column=0, sticky='ES')
s_tempo.grid(row=1, column=1, sticky='W')

l_density.grid(row=2, column=0, sticky='ES')
s_density.grid(row=2, column=1, columnspan=2)

l_legato.grid(row=3, column=0, sticky='ES')
s_legato.grid(row=3, column=1, columnspan=2)

l_saturation.grid(row=4, column=0, sticky='ES')
s_saturation.grid(row=4, column=1, columnspan=2)

l_substitution.grid(row=5, column=0, sticky='ES')
s_substitution.grid(row=5, column=1, columnspan=2)

l_activity.grid(row=6, column=0, sticky='ES')
s_activity.grid(row=6, column=1, columnspan=2)

l_register.grid(row=7, column=0, sticky='ES')
s_register.grid(row=7, column=1, sticky='W')

t_inversion.grid(row=7, column=1, sticky='ES')

# MAIN FUNCTION

def main():
    print "Starting OSCServer"
    st = threading.Thread(target=s.serve_forever)
    st.start()
    window.mainloop()
main()

