
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

tasks=[]
done=[]

def add_task():
    text = ask_text_popup("Ajouter une tâche")
    if text is None:
        return
    tasks.append(text)
    refresh_lists()

    
def hover_on_add(text_id):
    canvas.itemconfig(text_id, font=("Helvetica", 23, "bold")) 

def hover_off_add(text_id):
    canvas.itemconfig(text_id, font=("Helvetica", 20, "bold"))
    
    
def refresh_lists():
    canvas.delete("lists")  # efface seulement la zone listes
    # --- TASKS ---
    y = 260
    for i, t in enumerate(tasks):
        item_id = canvas.create_text(
            100, y,
            text="▢ " + t,
            fill="white",
            font=("Helvetica", 16),
            anchor="w", 
            tags=("lists", f"task_{i}")
        )

        # clic sur la tâche => move to done
        canvas.tag_bind(item_id, "<Button-1>", lambda e, idx=i: mark_done(idx))
        # hover
        canvas.tag_bind(item_id, "<Enter>", lambda e, iid=item_id: (canvas.config(cursor="hand2"), canvas.itemconfig(iid, fill="#ffd166")))
        canvas.tag_bind(item_id, "<Leave>", lambda e, iid=item_id: (canvas.config(cursor=""), canvas.itemconfig(iid, fill="white")))

        y += 26

    # --- DONE ---
    y = 675
    for t in done:
        text_id=canvas.create_text(
            100, y,
            text="▦ " + t,
            fill="gray23",
            anchor="w", 
            font=("Helvetica", 18),
            tags=("lists",)
        )
        x1, y1, x2, y2 = canvas.bbox(text_id)
        canvas.create_line(
        x1, (y1 + y2) // 2,
        x2, (y1 + y2) // 2,
        fill="gray23",
        width=2,
        tags=("lists",)
    )
        
        y += 26
    

    
    
def ask_text_popup(title="Ajouter une tâche"):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.resizable(False, False)
    popup.grab_set()

    tk.Label(popup, text="Texte :").pack(padx=12, pady=(12, 4))

    var = tk.StringVar()
    entry_popup = tk.Entry(popup, textvariable=var, width=35)
    entry_popup.pack(padx=12, pady=(0, 10))
    entry_popup.focus_set()

    result = {"text": None}
    
    def ok():
        text = var.get().strip()
        if text:
            result["text"] = text
        popup.destroy()

    def cancel():
        popup.destroy()
    
    btns = tk.Frame(popup)
    btns.pack(pady=(0, 12))
    tk.Button(btns, text="Ajouter", command=ok).pack(side="left", padx=6)

    popup.bind("<Return>", lambda e: ok())
    popup.bind("<Escape>", lambda e: cancel())

    root.wait_window(popup)
    return result["text"]


def mark_done(index):
    # index = position dans tasks
    done.append(tasks.pop(index))
    refresh_lists()




root = tk.Tk()                 
root.title("Ma Todo App")      







# ----BACKGROUND IMG-----
image = Image.open("background-3.jpeg")
bg_image = ImageTk.PhotoImage(image, master=root)
img_width, img_height = image.size
print(image.size)

root.geometry(f"{img_width}x{img_height}")      
#root.resizable(True,False)

canvas = tk.Canvas(root, width=img_width, height=img_height)
canvas.pack()
canvas.create_image(0, 0, image=bg_image, anchor="nw")


# -----Image de Logo------
title_pil = Image.open("Logo.PNG")
title_pil = title_pil.resize((250, 250)) 
title_img = ImageTk.PhotoImage(title_pil, master=root)

# positionne l’image (x, y)
canvas.create_image(img_width // 2, 100, image=title_img)


entry = tk.Entry(root, width=30)







#----BUTTON add task----
add_text_id = canvas.create_text(
    img_width // 4, 230,
    text="+ ADD TASK",
    font=("Helvetica", 20, "bold"),
    fill="light pink",
    tags=("ui",)
)
canvas.tag_bind(add_text_id, "<Button-1>", lambda e: add_task())
canvas.tag_bind(add_text_id, 
                "<Enter>", 
                lambda e: (canvas.config(cursor="hand2"), hover_on_add(add_text_id))
)
canvas.tag_bind(add_text_id, 
                "<Leave>", 
                lambda e: (canvas.config(cursor=""), hover_off_add(add_text_id))
)



#----Done task-----
done_text_id = canvas.create_text(
    img_width // 4, 650,
    text="✔️  DONE",
    font=("Helvetica", 20, "bold"),
    fill="gray23",
    tags=('ui',)
)
canvas.tag_bind(done_text_id, 
                "<Enter>", 
                lambda e: canvas.config(cursor="hand2")
)
canvas.tag_bind(done_text_id, 
                "<Leave>", 
                lambda e: canvas.config(cursor="")
)





root.mainloop()                # boucle: la fenêtre reste ouverte
