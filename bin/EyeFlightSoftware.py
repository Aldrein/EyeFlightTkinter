import datetime
import tkinter as tk
from tkinter import font
from pathlib import Path
import CanvasImage as cvImg
import GPSUtils as GU

# Window size and position variables
appWidth = 1024
appHeight = 600
appOffsetX = 250
appOffsetY = 100

# Color setup
darkGrayColor = '#1c1c1c' # Base button background
grayColor = '#2e2e2e' # Active button background

# Project path
projectPath = Path(__file__).parents[1].resolve()
print(projectPath)

# Plane coordinates
gps = GU.GpsUtils()
gps.init()
# longWS84, latWS84, longPixel, latPixel = gps.access()
latWS84 = 0
longWS84 = 0
longPixel = 3500
latPixel = 3500
bearing = 0
altitude = 0


timeFormat = '%Y-%m-%d-%H:%M:%S'

class MapWindow(tk.Frame):
    """ Main window class """
    def __init__(self, mainframe: tk.Frame, path: Path, planePath: Path):
        """ Initialize the main Frame """
        tk.Frame.__init__(self, master=mainframe)
        self.master.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=1)
        self.canvas = cvImg.CanvasImage(self.master, path, planePath, appWidth, appHeight)  # create widget
        self.canvas.movecenter()
        self.canvas.drawPlane(longPixel, latPixel, bearing)
        self.canvas.grid(row=0, column=0)  # show widget

class EyeFlight(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        filename = Path(projectPath, 'img//OACI_11_L93_E100.png')
        planePath = Path(projectPath, 'img//aircraft.png')
        mapFrameRoot = tk.Frame(master=self.parent)
        self.mapFrame = MapWindow(mapFrameRoot, path=filename, planePath=planePath)
        mapFrameRoot.place(x=0, y=0)
        self.UIFrame = tk.Frame(master=self.parent)
        self.UIFrame.place(x=0, y=0)
        self.dataFrame = tk.Frame(master=self.parent, bg=darkGrayColor, border=0)
        self.dataFrame.place(anchor='sw', relx=0.0, rely=1.0, relheight=.3, relwidth=.25)
        self.__createUI()

    def __createUI(self):
        self.__buttonPlacement()
        self.__dataPlacement()

    def __buttonPlacement(self):
        #Icons setup
        exitIcon = tk.PhotoImage(file = 'img//icons//exitInvert.png')
        weatherIcon = tk.PhotoImage(file = 'img//icons//weatherInvert.png')
        docIcon = tk.PhotoImage(file = 'img//icons//docInvert.png')
        navigationIcon = tk.PhotoImage(file = 'img//icons//navigationInvert.png')
        historyIcon = tk.PhotoImage(file = 'img//icons//historyInvert.png')
        parametersIcon = tk.PhotoImage(file = 'img//icons//parametersInvert.png')
        mapBackgroundIcon = tk.PhotoImage(file = 'img//icons//mapBackgroundInvert.png')
        trafficIcon = tk.PhotoImage(file = 'img//icons//trafficInvert.png')
        centerIcon = tk.PhotoImage(file = 'img//icons//centerInvert.png')
        northUpIcon = tk.PhotoImage(file = 'img//icons//northUpInvert.png')
        displayIcon = tk.PhotoImage(file = 'img//icons//displayInvert.png')


        # Top Menu
        exitButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Exit', image=exitIcon, command=self.parent.destroy)
        exitButton.place(anchor='ne', relx=1.0, rely=0.0, relwidth=.05, relheight=.08)
        exitButton.icon = exitIcon
        weatherButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Météo', image=weatherIcon)
        weatherButton.place(anchor='n', relx=0.2, rely=0.0, relwidth=.08, relheight=.1)
        weatherButton.icon = weatherIcon
        docButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Documents', image=docIcon)
        docButton.place(anchor='n', relx=0.35, rely=0.0, relwidth=.08, relheight=.1)
        docButton.icon = docIcon
        navigationButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Navigation', image=navigationIcon)
        navigationButton.place(anchor='n', relx=0.5, rely=0.0, relwidth=.08, relheight=.1)
        navigationButton.icon = navigationIcon
        historyButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Historique', image=historyIcon)
        historyButton.place(anchor='n', relx=0.65, rely=0.0, relwidth=.08, relheight=.1)
        historyButton.icon = historyIcon
        parametersButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Paramètres', image=parametersIcon)
        parametersButton.place(anchor='n', relx=0.8, rely=0.0, relwidth=.08, relheight=.1)
        parametersButton.icon = parametersIcon

        # Side Menu
        mapBackgroundButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Fond de carte', image=mapBackgroundIcon)
        mapBackgroundButton.place(anchor='e', relx=1.0, rely=.3, relwidth=.08, relheight=.1)
        mapBackgroundButton.icon = mapBackgroundIcon
        trafficButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Traffic', image=trafficIcon)
        trafficButton.place(anchor='e', relx=1.0, rely=.4, relwidth=.08, relheight=.1)
        trafficButton.icon = trafficIcon
        centerButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Centrer', image=centerIcon, command=self.mapFrame.canvas.centerOnPlane)
        centerButton.place(anchor='e', relx=1.0, rely=.5, relwidth=.08, relheight=.1)
        centerButton.icon = centerIcon
        northUpButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Nord en haut', image=northUpIcon)
        northUpButton.place(anchor='e', relx=1.0, rely=.6, relwidth=.08, relheight=.1)
        northUpButton.icon = northUpIcon
        displayButton = tk.Button(self.parent, bg=darkGrayColor, activebackground=grayColor, border=0, text='Affichages', image=displayIcon)
        displayButton.place(anchor='e', relx=1.0, rely=.7, relwidth=.08, relheight=.1)
        displayButton.icon = displayIcon

    def __dataPlacement(self):
        dataFont = font.Font(family='Ubuntu', size=18)
        self.latLabel = tk.Label(master=self.dataFrame, background=darkGrayColor, fg='white', text=latWS84, font=dataFont)
        self.latLabel.place(anchor='center', relx=.5, rely=.2, relwidth=.8, relheight=.2)
        self.longLabel = tk.Label(master=self.dataFrame, background=darkGrayColor, fg='white', text=longWS84, font=dataFont)
        self.longLabel.place(anchor='center', relx=.5, rely=.5, relwidth=.8, relheight=.2)
        self.altLabel = tk.Label(master=self.dataFrame, background=darkGrayColor, fg='white', text=altitude, font=dataFont)
        self.altLabel.place(anchor='center', relx=.5, rely=.8, relwidth=.8, relheight=.2)
        
    def movePlane(self, x, y, b, alt, lat, long):
        dataFont = font.Font(family='Ubuntu', size=18)
        self.mapFrame.canvas.drawPlane(x, y, b)
        self.latLabel.configure(text=lat)
        self.longLabel.configure(text=long)
        self.altLabel.configure(text=alt)


def loop():
  """ Main program loop running alongside Tkinter mainloop """
  currentTime = datetime.datetime.now().strftime(timeFormat)
  delta = datetime.datetime.strptime(currentTime, timeFormat) - datetime.datetime.strptime(startTime, timeFormat)
  win.title(f'EyeFlightSoftware {delta}')
  
  #! CODE BEING LOOPED BELOW
  
  longWS84, latWS84, longPixel, latPixel, bearing, altitude = gps.access()

  if (latPixel != "NA") & (longPixel != "NA"):
    win.children.get('!eyeflight').movePlane(longPixel, latPixel, -bearing, altitude, latWS84, longWS84)

  #? Ici tu peux appeler la fonction pour récupérer les coordonnées GPS puis les transformer en coordonnées image
  #? Après tu peux appeler win.children.get('!eyeflight').movePlane(x,y)
  #? à tester je sais pas si ça récupère l'instance de la classe ou juste la classe elle même
  #? Il faut trouver un moyen d'avoir l'instance pour après appeler movePlane(x, y) qui délègue ensuite au canvas et affiche l'avion
  #? Vu que j'ai pas GPSD je peux pas tester correctement mais tu me diras si tu trouves un moyen
  
  #! CODE BEING LOOPED ABOVE
  
  win.after(500, loop) # loops the function

if __name__=='__main__':
  win = tk.Tk()
  win.geometry(f'{appWidth}x{appHeight}+{appOffsetX}+{appOffsetY}')
  win.title('EyeFlightSoftware')
  win.configure(bg='black')
  #win.overrideredirect(1) #without borders
  #win.wm_attributes('-fullscreen', 'True') #fullscreen
  EyeFlight(win).pack(side='top', fill='both', expand=True)
  startTime = datetime.datetime.now().strftime(timeFormat)
  print(win.children)
  win.after(200, loop)
  win.mainloop()