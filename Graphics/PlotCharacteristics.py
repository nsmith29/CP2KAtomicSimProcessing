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

class atom_lookup:
    def __init__(self, atom_name):
        self.atom_color = None
        self.size_normalised = None
        self.bonds_formed = None
        self.atomic_radius = None
        self.atom_name = atom_name

    def identification(self):
        if self.atom_name == 'H':
            self.atomic_radius = 37
            self.atom_color = [225, 225, 225]
            self.bonds_formed = 1
        elif self.atom_name == 'Li':
            self.atomic_radius = 152
            self.atom_color = [204, 128, 255]
            self.bonds_formed = 1
        elif self.atom_name == 'Be':
            self.atomic_radius = 112
            self.bonds_formed = 2
            self.atom_color = [194, 255, 0]
        elif self.atom_name == 'B':
            self.atomic_radius = 83
            self.bonds_formed = 3
            self.atom_color = [255, 181, 181]
        elif self.atom_name == 'C':
            self.atomic_radius = 77
            self.bonds_formed = 4
            self.atom_color = [0, 225, 191]
        elif self.atom_name == 'N':
            self.atomic_radius = 75
            self.bonds_formed = 3
            self.atom_color = [48, 80, 248]
        elif self.atom_name == 'O':
            self.atomic_radius = 73
            self.bonds_formed = 2
            self.atom_color = [255, 13, 13]
        elif self.atom_name == 'F':
            self.atomic_radius = 72
            self.bonds_formed = 1
            self.atom_color = [144, 224, 80]
        elif self.atom_name == 'Na':
            self.atomic_radius = 186
            self.bonds_formed = 1
            self.atom_color = [144, 144, 144]
        elif self.atom_name == 'Mg':
            self.atomic_radius = 160
            self.bonds_formed = 2
            self.atom_color = [255, 255, 199]
        elif self.atom_name == 'Al':
            self.atomic_radius = 143
            self.bonds_formed = 3
            self.atom_color = [191, 166, 161]
        elif self.atom_name == 'Si':
            self.atomic_radius = 117
            self.bonds_formed = 4
            self.atom_color = [225, 225, 0]
        elif self.atom_name == 'P':
            self.atomic_radius = 110
            self.bonds_formed = 3
            self.atom_color = [225, 128, 0]
        elif self.atom_name == 'S':
            self.atomic_radius = 104
            self.bonds_formed = 2
            self.atom_color = [255, 255, 48]
        elif self.atom_name == 'Cl':
            self.atomic_radius = 99
            self.bonds_formed = 1
            self.atom_color = [31, 240, 31]
        elif self.atom_name == 'K':
            self.atomic_radius = 227
            self.bonds_formed = 1
            self.atom_color = [179, 227, 245]
        elif self.atom_name == 'Ca':
            self.atomic_radius = 197
            self.bonds_formed = 2
            self.atom_color = [161, 54, 212]
        elif self.atom_name == 'Sc':
            self.atomic_radius = 162
            self.bonds_formed = 3
            self.atom_color = [230, 230, 230]
        elif self.atom_name == 'Ti':
            self.atomic_radius = 147
            self.bonds_formed = 4
            self.atom_color = [191, 194, 199]
        elif self.atom_name == 'V':
            self.atomic_radius = 134
            self.bonds_formed = 5
            self.atom_color = [166, 166, 171]
        elif self.atom_name == 'Cr':
            self.atomic_radius = 128
            self.bonds_formed = 3
            self.atom_color = [138, 153, 199]
        elif self.atom_name == 'Mn':
            self.atomic_radius = 127
            self.bonds_formed = 2
            self.atom_color = [156, 122, 199]
        elif self.atom_name == 'Fe':
            self.atomic_radius = 126
            self.bonds_formed = 2
            self.atom_color = [224, 102, 51]
        elif self.atom_name == 'Co':
            self.atomic_radius = 125
            self.bonds_formed = 2
            self.atom_color = [240, 144, 173]
        elif self.atom_name == 'Ni':
            self.atomic_radius = 124
            self.bonds_formed = 2
            self.atom_color = [80, 208, 80]
        elif self.atom_name == 'Cu':
            self.atomic_radius = 128
            self.bonds_formed = 2
            self.atom_color = [200, 128, 51]
        elif self.atom_name == 'Zn':
            self.atomic_radius = 134
            self.bonds_formed = 2
            self.atom_color = [125, 128, 176]
        elif self.atom_name == 'Ga':
            self.atomic_radius = 135
            self.bonds_formed = 3
            self.atom_color = [240, 200, 160]
        elif self.atom_name == 'Ge':
            self.atomic_radius = 122
            self.bonds_formed = 4
            self.atom_color = [102, 143, 143]
        elif self.atom_name == 'As':
            self.atomic_radius = 120
            self.bonds_formed = 3
            self.atom_color = [189, 128, 227]
        elif self.atom_name == 'Se':
            self.atomic_radius = 116
            self.bonds_formed = 2
            self.atom_color = [255, 161, 0]
        elif self.atom_name == 'Br':
            self.atomic_radius = 114
            self.bonds_formed = 1
            self.atom_color = [166, 41, 41]
        elif self.atom_name == 'Rb':
            self.atomic_radius = 248
            self.bonds_formed = 1
            self.atom_color = [131, 31, 186]
        elif self.atom_name == 'Sr':
            self.atomic_radius = 215
            self.bonds_formed = 2
            self.atom_color = [69, 255, 199]
        elif self.atom_name == 'Y':
            self.atomic_radius = 180
            self.bonds_formed = 3
            self.atom_color = [148, 255, 255]
        elif self.atom_name == 'Zr':
            self.atomic_radius = 160
            self.bonds_formed = 4
            self.atom_color = [217, 255, 199]
        elif self.atom_name == 'Nb':
            self.atomic_radius = 146
            self.bonds_formed = 5
            self.atom_color = [66, 130, 150]
        elif self.atom_name == 'Mo':
            self.atomic_radius = 139
            self.bonds_formed = 6
            self.atom_color = [84, 181, 181]
        elif self.atom_name == 'Tc':
            self.atomic_radius = 136
            self.bonds_formed = 4
            self.atom_color = [0, 143, 255]
        elif self.atom_name == 'Ru':
            self.atomic_radius = 134
            self.bonds_formed = 3
            self.atom_color = [36, 143, 143]
        elif self.atom_name == 'Rh':
            self.atomic_radius = 134
            self.bonds_formed = 3
            self.atom_color = [0, 186, 255]
        elif self.atom_name == 'Pd':
            self.atomic_radius = 137
            self.bonds_formed = 4
            self.atom_color = [208, 105, 133]
        elif self.atom_name == 'Ag':
            self.atomic_radius = 144
            self.bonds_formed = 1
            self.atom_color = [192, 192, 192]
        elif self.atom_name == 'Cd':
            self.atomic_radius = 151
            self.bonds_formed = 2
            self.atom_color = [255, 217, 143]
        elif self.atom_name == 'In':
            self.atomic_radius = 167
            self.bonds_formed = 3
            self.atom_color = [166, 117, 115]
        elif self.atom_name == 'Sn':
            self.atomic_radius = 140
            self.bonds_formed = 4
            self.atom_color = [117, 79, 69]
        elif self.atom_name == 'Sb':
            self.atomic_radius = 140
            self.bonds_formed = 3
            self.atom_color = [199, 0, 102]
        elif self.atom_name == 'Te':
            self.atomic_radius = 143
            self.bonds_formed = 2
            self.atom_color = [212, 106, 0]
        elif self.atom_name == 'I':
            self.atomic_radius = 133
            self.bonds_formed = 1
            self.atom_color = [148, 0, 148]
        elif self.atom_name == 'Cs':
            self.atomic_radius = 265 # largest atom
            self.bonds_formed = 1
            self.atom_color = [0, 201, 0]
        elif self.atom_name == 'Ba':
            self.atomic_radius = 222
            self.bonds_formed = 2
            self.atom_color = [66, 0, 102]
        elif self.atom_name == 'Hf':
            self.atomic_radius = 159
            self.bonds_formed = 4
            self.atom_color = [163, 255, 199]
        elif self.atom_name == 'Ta':
            self.atomic_radius = 146
            self.bonds_formed = 5
            self.atom_color = [77, 166, 255]
        elif self.atom_name == 'W':
            self.atomic_radius = 139
            self.bonds_formed = 4
            self.atom_color = [235, 0, 38]
        elif self.atom_name == 'Re':
            self.atomic_radius = 137
            self.bonds_formed = 4
            self.atom_color = [38, 125, 171]
        elif self.atom_name == 'Os':
            self.atomic_radius = 135
            self.bonds_formed = 4
            self.atom_color = [0, 171, 36]
        elif self.atom_name == 'Ir':
            self.atomic_radius = 136
            self.bonds_formed = 3
            self.atom_color = [23, 84, 135]
        elif self.atom_name == 'Pt':
            self.atomic_radius = 138
            self.bonds_formed = 4
            self.atom_color = [230, 0, 46]
        elif self.atom_name == 'Au':
            self.atomic_radius = 144
            self.bonds_formed = 3
            self.atom_color = [255, 209, 35]
        elif self.atom_name == 'Hg':
            self.atomic_radius = 151
            self.bonds_formed = 2
            self.atom_color = [0, 230, 17]
        elif self.atom_name == 'Tl':
            self.atomic_radius = 170
            self.bonds_formed = 3
            self.atom_color = [166, 84, 77]
        elif self.atom_name == 'Pb':
            self.atomic_radius = 175
            self.bonds_formed = 4
            self.atom_color = [87, 89, 97]
        elif self.atom_name == 'Bi':
            self.atomic_radius = 150
            self.bonds_formed = 3
            self.atom_color = [158, 79, 181]
        elif self.atom_name == 'Po':
            self.atomic_radius = 167
            self.bonds_formed = 2
            self.atom_color = [0, 107, 255]
        color_normalised = [a/255 for a in self.atom_color]
        atom_color = (round(float(color_normalised[0]),1),round(float(color_normalised[1]),1),round(float(color_normalised[2]),1))
        self.size_normalised = (self.atomic_radius / 265) * 2
        return atom_color, self.size_normalised, self.bonds_formed
