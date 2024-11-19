def clearApp(app):
    for frame in app.winfo_children():
        frame.destroy()