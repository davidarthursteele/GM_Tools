from Tkinter import *
import Matrix

def sel():
    selection = (["Blue","Green","Orange","Red"][var.get()]) + " Host"
    selection += "\n" + (["Easy","Average","Hard"][diff.get()]) + " Difficulty"
    label.config(text = selection)

root = Tk()
RTitle=root.title("3E Matrix Host Generator")
frame = Frame(root)
root.resizable(False, False)
frame.pack(side = LEFT)
frame2 = Frame(root)
frame2.pack(side = RIGHT)
var = IntVar()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

R1 = Radiobutton(frame, text="Blue Host", variable=var, value=0,
                  command=sel)
R1.pack(anchor = W)

R2 = Radiobutton(frame, text="Green Host", variable=var, value=1,
                  command=sel)
R2.pack(anchor = W)

R3 = Radiobutton(frame, text="Orange Host", variable=var, value=2,
                  command=sel)
R3.pack( anchor = W)

R4 = Radiobutton(frame, text="Red Host", variable=var, value=3,
                  command=sel)
R4.pack( anchor = W)
diff = IntVar()
D1 = Radiobutton(frame2, text="Easy Difficulty", variable=diff, value=0,
                  command=sel)
D1.pack( anchor = W )

D2 = Radiobutton(frame2, text="Average Difficulty", variable=diff, value=1,
                  command=sel)
D2.pack( anchor = W  )

D3 = Radiobutton(frame2, text="Hard Difficulty", variable=diff, value=2,
                  command=sel)
D3.pack( anchor = W )


def callback():
    output_file = open("host.txt", "w")
    color = ["Blue","Green","Orange","Red"][var.get()]
    difficulty = ["easy", "average", "hard"][diff.get()]
    new_host = Matrix.host(color, difficulty)
    output_file.write(str(new_host.color) +" " + str(new_host.security_value) + " - ")
    output_file.write(str(new_host.subsystems["Access"]) + "/" + str(new_host.subsystems["Control"]) + "/")
    output_file.write(str(new_host.subsystems["Index"]) + "/" + str(new_host.subsystems["Files"]) + "/")
    output_file.write(str(new_host.subsystems["Slave"]) + "\n\n\n")
    for line in new_host.sheaf:
        output_file.write(line + "\n")
    output_file.write('\n\nPaydata Points\n')
    for point in new_host.paydata:
        output_file.write("> " + str(point[0]) + " Mp -- " + str(point[1]) + "\n")


label = Label(root)
label.pack()
blackbutton = Button(bottomframe, text="Generate Host", bg="white", fg="black", command = callback)
blackbutton.pack( side = BOTTOM)
root.mainloop()