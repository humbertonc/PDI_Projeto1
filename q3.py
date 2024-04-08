from PIL import Image

def rgb_to_hsb(rgb):
    r,g,b = rgb
    r /= 255
    g /= 255
    b /= 255
    max_val = max(r,g,b)
    min_val = min(r,g,b)

    if max_val == min_val:
        h = 0
    elif g == max_val:
        h = 60*(b-r)/(max_val-min_val) + 120
    elif b == max_val:
        h = 60*(r-g)/(max_val-min_val) + 240
    elif g >= b:
        h = 60*(g-b)/(max_val-min_val)
    else: #Quando R = MAX e G < B
        h = 60*(g-b)/(max_val-min_val) + 360

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

    # get the fractional part of the sector
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

    return [int(255*x) for x in ret]

def testa_q3(path_1,path_2):
    img_giver = Image.open(path_1)
    img_receiver = Image.open(path_2)

    pixels_giver = img_giver.load()
    pixels_receiver = img_receiver.load()

    # Ambas possuem as mesmas dimensões
    w, h = img_giver.size
    new_image = []
    # Iterate over each pixel
    for y in range(w):
        for x in range(h):
            giv_sat = rgb_to_hsb(pixels_giver[x,y])[1]
            rec_h, rec_s, rec_b = rgb_to_hsb(pixels_receiver[x,y])
            new_image.append(tuple(hsb_to_rgb([rec_h, giv_sat, rec_b])))

    image = Image.new("RGB", (w, h))  # Create a new RGB image
    image.putdata(new_image)  # Put the pixel data into the image

    image.show()

#testa_q3('vermelho_claro.jpg','azul_cinzado.jpg')
#testa_q3('azul_cinzado.jpg','vermelho_claro.jpg')
#testa_q3('azul_cinzado.jpg','babuino.png')
#testa_q3('vermelho_claro.jpg','babuino.png')