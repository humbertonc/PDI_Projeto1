from PIL import Image

def rgb_to_hsb(rgb):
    r,g,b = rgb
    r /= 255.0
    g /= 255.0
    b /= 255.0
    max_val = max(r,g,b)
    min_val = min(r,g,b)

    if max_val == min_val:
        h = 0
    elif g == max_val:
        h = (60*(b-r))/(max_val-min_val) + 120
    elif b == max_val:
        h = (60*(r-g))/(max_val-min_val) + 240
    elif g >= b:
        h = (60*(g-b))/(max_val-min_val)
    else: #Quando R = MAX e G < B
        h = (60*(g-b))/(max_val-min_val) + 360

    if max_val == 0:
        s = 0
    else:
        s = 1-(min_val/max_val)

    return [round(h,2),round(100*s,2),round(100*max_val,2)]

def hsb_to_rgb(hsb):
    h, s, b = hsb
    s /= 100
    b /= 100

    h /= 60.0
    sector_pos = h % 6
    h1 = int(sector_pos)

    f = sector_pos - h1
    p = b *(1-s)
    q = b * (1-f*s)
    t = b * (1 - (1-f)*s)

    if not h1:
        ret = [b,t,p]
    elif h1 == 1:
        ret = [q,b,p]
    elif h1 == 2:
        ret = [p,b,t]
    elif h1 == 3:
        ret = [p,q,b]
    elif h1 == 4:
        ret = [t,p,b]
    elif h1 == 5:
        ret = [b,p,q]
    
    return [round(255*x) for x in ret]

def testa_q1(path):
    img = Image.open(path)

    pixels = img.load()
    w, h = img.size

    certo = 0
    errado = 0
    for x in range(w):
        for y in range(h):
            
            hsb = rgb_to_hsb(pixels[x, y])
            novo_pixel = hsb_to_rgb(hsb)
            
            # Checa se pixel convertido é igual ao original
            if novo_pixel == list(pixels[x,y]):
                certo += 1
            else:
                errado += 1

    print(f'Certo: {certo}')
    print(f'Errado: {errado}')

if __name__ == '__main__':
    testa_q1('imagens/babuino.png')
    testa_q1('imagens/DancingInWater.jpg')
    testa_q1('imagens/Shapes.png')
