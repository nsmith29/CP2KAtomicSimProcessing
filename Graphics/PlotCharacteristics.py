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

        self.colour = self.colordict.get(str("color{}".format(self.num)))

class atom_lookup:
    def __init__(self, atom_name):
        self.atom_color = None
        self.size_normalised = None

    # def identification(self):
        if atom_name == 'H':
            atomic_radius = 37
            atom_color = [225, 225, 225]
        elif atom_name == 'Li':
            atomic_radius = 152
            atom_color = [204, 128, 255]
        elif atom_name == 'Be':
            atomic_radius = 112
            atom_color = [194, 255, 0]
        elif atom_name == 'B':
            atomic_radius = 83
            atom_color = [255, 181, 181]
        elif atom_name == 'C':
            atomic_radius = 77
            atom_color = [0, 225, 191]
        elif atom_name == 'N':
            atomic_radius = 75
            atom_color = [48, 80, 248]
        elif atom_name == 'O':
            atomic_radius = 73
            atom_color = [255, 13, 13]
        elif atom_name == 'F':
            atomic_radius = 72
            atom_color = [144, 224, 80]
        elif atom_name == 'Na':
            atomic_radius = 186
            atom_color = [144, 144, 144]
        elif atom_name == 'Mg':
            atomic_radius = 160
            atom_color = [255, 255, 199]
        elif atom_name == 'Al':
            atomic_radius = 143
            atom_color = [191, 166, 161]
        elif atom_name == 'Si':
            atomic_radius = 117
            atom_color = [225, 225, 0]
        elif atom_name == 'P':
            atomic_radius = 110
            atom_color = [225, 128, 0]
        elif atom_name == 'S':
            atomic_radius = 104
            atom_color = [255, 255, 48]
        elif atom_name == 'Cl':
            atomic_radius = 99
            atom_color = [31, 240, 31]
        elif atom_name == 'K':
            atomic_radius = 227
            atom_color = [179, 227, 245]
        elif atom_name == 'Ca':
            atomic_radius = 197
            atom_color = [161, 54, 212]
        elif atom_name == 'Sc':
            atomic_radius = 162
            atom_color = [230, 230, 230]
        elif atom_name == 'Ti':
            atomic_radius = 147
            atom_color = [191, 194, 199]
        elif atom_name == 'V':
            atomic_radius = 134
            atom_color = [166, 166, 171]
        elif atom_name == 'Cr':
            atomic_radius = 128
            atom_color = [138, 153, 199]
        elif atom_name == 'Mn':
            atomic_radius = 127
            atom_color = [156, 122, 199]
        elif atom_name == 'Fe':
            atomic_radius = 126
            atom_color = [224, 102, 51]
        elif atom_name == 'Co':
            atomic_radius = 125
            atom_color = [240, 144, 173]
        elif atom_name == 'Ni':
            atomic_radius = 124
            atom_color = [80, 208, 80]
        elif atom_name == 'Cu':
            atomic_radius = 128
            atom_color = [200, 128, 51]
        elif atom_name == 'Zn':
            atomic_radius = 134
            atom_color = [125, 128, 176]
        elif atom_name == 'Ga':
            atomic_radius = 135
            atom_color = [240, 200, 160]
        elif atom_name == 'Ge':
            atomic_radius = 122
            atom_color = [102, 143, 143]
        elif atom_name == 'As':
            atomic_radius = 120
            atom_color = [189, 128, 227]
        elif atom_name == 'Se':
            atomic_radius = 116
            atom_color = [255, 161, 0]
        elif atom_name == 'Br':
            atomic_radius = 114
            atom_color = [166, 41, 41]
        elif atom_name == 'Rb':
            atomic_radius = 248
            atom_color = [131, 31, 186]
        elif atom_name == 'Sr':
            atomic_radius = 215
            atom_color = [69, 255, 199]
        elif atom_name == 'Y':
            atomic_radius = 180
            atom_color = [148, 255, 255]
        elif atom_name == 'Zr':
            atomic_radius = 160
            atom_color = [217, 255, 199]
        elif atom_name == 'Nb':
            atomic_radius = 146
            atom_color = [66, 130, 150]
        elif atom_name == 'Mo':
            atomic_radius = 139
            atom_color = [84, 181, 181]
        elif atom_name == 'Tc':
            atomic_radius = 136
            atom_color = [0, 143, 255]
        elif atom_name == 'Ru':
            atomic_radius = 134
            atom_color = [36, 143, 143]
        elif atom_name == 'Rh':
            atomic_radius = 134
            atom_color = [0, 186, 255]
        elif atom_name == 'Pd':
            atomic_radius = 137
            atom_color = [208, 105, 133]
        elif atom_name == 'Ag':
            atomic_radius = 144
            atom_color = [192, 192, 192]
        elif atom_name == 'Cd':
            atomic_radius = 151
            atom_color = [255, 217, 143]
        elif atom_name == 'In':
            atomic_radius = 167
            atom_color = [166, 117, 115]
        elif atom_name == 'Sn':
            atomic_radius = 140
            atom_color = [117, 79, 69]
        elif atom_name == 'Sb':
            atomic_radius = 140
            atom_color = [199, 0, 102]
        elif atom_name == 'Te':
            atomic_radius = 143
            atom_color = [212, 106, 0]
        elif atom_name == 'I':
            atomic_radius = 133
            atom_color = [148, 0, 148]
        elif atom_name == 'Cs':
            atomic_radius = 265
            atom_color = [0, 201, 0]
        elif atom_name == 'Ba':
            atomic_radius = 222
            atom_color = [66, 0, 102]
        elif atom_name == 'Hf':
            atomic_radius = 159
            atom_color = [163, 255, 199]
        elif atom_name == 'Ta':
            atomic_radius = 146
            atom_color = [77, 166, 255]
        elif atom_name == 'W':
            atomic_radius = 139
            atom_color = [235, 0, 38]
        elif atom_name == 'Re':
            atomic_radius = 137
            atom_color = [38, 125, 171]
        elif atom_name == 'Os':
            atomic_radius = 135
            atom_color = [0, 171, 36]
        elif atom_name == 'Ir':
            atomic_radius = 136
            atom_color = [23, 84, 135]
        elif atom_name == 'Pt':
            atomic_radius = 138
            atom_color = [230, 0, 46]
        elif atom_name == 'Au':
            atomic_radius = 144
            atom_color = [255, 209, 35]
        elif atom_name == 'Hg':
            atomic_radius = 151
            atom_color = [0, 230, 17]
        elif atom_name == 'Tl':
            atomic_radius = 170
            atom_color = [166, 84, 77]
        elif atom_name == 'Pb':
            atomic_radius = 175
            atom_color = [87, 89, 97]
        elif atom_name == 'Bi':
            atomic_radius = 150
            atom_color = [158, 79, 181]
        elif atom_name == 'Po':
            atomic_radius = 167
            atom_color = [0, 107, 255]
        color_normalised = [a/255 for a in atom_color]
        self.atom_color = (round(float(color_normalised[0]),1),round(float(color_normalised[1]),1),round(float(color_normalised[2]),1))
        self.size_normalised = (atomic_radius / 265) * 2
