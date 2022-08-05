class Colors:
    def __init__(self, num):
        self.num = num
        self. colordict = {
            'color1': "#76EEC6",
            'color2': "#000000",
            'color3': "#8A2BE2",
            'color4': "#20B2AA",
            'color6': "#FF34B3",
            'color5': "#FF0000",
            'color7': "#836FFF",
            'color8': "#54FF9F",
            'color9': "#FFFF00",
            'color10': "#EE3A8C"
        }

    def getcolor(self):
        colour = self.colordict.get(str("color{}".format(self.num)))
        return colour

