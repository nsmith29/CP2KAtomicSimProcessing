class Colors:
    def __init__(self, num):
        self.num = num
        self. colordict = {
            'color1': "#F0F8FF", # aliceblue
            'color2': "#000000",  # black
            'color3': "#FF7256",  # coral1
            'color4': "#FFB90F", # darkgoldenrod1
            'color5': "#00C957", # emeraldgreen
            'color6': "#B22222", # firebrick
            'color7': "#DCDCDC", # gainsboro
            'color8': "#E0EEE0", # honeydrew2
            'color9': "#CD5C5C", # indianred
            'color10': "#8470FF", # lightslateblue
            'color11': "#E6E6FA", # lavender
            'color12': "#FF34B3",  # maroon1
            'color13': "#BDFCC9", # mint
            'color14': "#FF4500", # orangered1
            'color15': "#98FB98", # palegreen
            'color16': "#FF0000",  # red1
            'color17': "#836FFF",  # slateblue1
            'color18': "#40E0D0", # turquoise
            'color19': "#EE3A8C",  # violetred2
            'color20': "#808069", # warmgrey
            'color21': "#76EEC6", # aquamarine2
            'color22': "#8A2BE2",  # blueviolet
            'color23': "#DC143C", # crimson
            'color24': "#C1FFC1", # darkseagreen1
            'color25': "#FCE6C9", # eggshell
            'color26': "#FF7D40", # flesh
            'color27': "#FFC125", # goldenrod1
            'color28': "#8B3A62", # hotpink4
            'color29': "#4B0082", #indigo
            'color30': "#8B864E", # khaki4
            'color31': "#20B2AA",  # lightseagreen
            'color32': "#AB82FF", # mediumpurple
            'color33': "#FFDEAD", # navajowhite1
            'color34': "#808000", # olive
            'color35': "#8B475D", # palevioletred4
            'color36': "#FFC1C1", # rosybrown1
            'color37': "#54FF9F",  # seagreen1
            'color38': "#FFE1FF", # thistle1
            'color39': "#EEDFCC", # antiquewhite2
            'color40': "#E3CF57", # banana
            'color41': "#6495ED", # cornflowerblue
            'color42': "#BF3EFF", # darkorchid1
            'color43': "#228B22", # forestgreen
            'color44': "#FFFAF0", # foralwhite
            'color45': "#ADFF2F", # greenyellow
            'color46': "#838B83", # honeydew4
            'color47': "#CDCDC1", # ivory3
            'color48': "#FFF0F5", # lavenderblush
            'color49': "#8B5F65", # lightpink4
            'color50': "#03A89E", # manganeseblue
            'color51': "#000080", # navy
            'color52': "#EE9A00", # orange2
            'color53': "#B0E0E6", # powderblue
            'color54': "#4876FF", # royalblue1
            'color55': "#FA8072", # salmon
            'color56': "#EE5C42", # tomato2
            'color57': "#FFFF00" # yellow1
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
