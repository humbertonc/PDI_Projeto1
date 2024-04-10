from PIL import Image

def rgb_to_hsb(rgb):
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    if max_val == min_val:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / (max_val - min_val)) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / (max_val - min_val)) + 120) % 360
    elif max_val == b:
        h = (60 * ((r - g) / (max_val - min_val)) + 240) % 360
    
    if max_val == 0:
        s = 0
    else:
        s = (max_val - min_val) / max_val
    
    b = max_val
    
    return (round((h / 360) * 255), round(s * 255), round(b * 255))

def hsb_to_rgb(hsb):
    h, s, b = hsb
    s /= 255
    b /= 255

    h = (h / 255) * 360

    c = b * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = b - c

    if h < 60:
        rp, gp, bp = c, x, 0
    elif h < 120:
        rp, gp, bp = x, c, 0
    elif h < 180:
        rp, gp, bp = 0, c, x
    elif h < 240:
        rp, gp, bp = 0, x, c
    elif h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x

    r = (rp + m) * 255
    g = (gp + m) * 255
    b = (bp + m) * 255

    return [round(r), round(g), round(b)]


def mult_ad_filter(ad_m, mult_s, mult_b):
    img = Image.open('DancingInWater.jpg')
    width, height = img.size

    img_hsv = []
    new_img = []

    img_rgb = Image.new("RGB", (width, height))

    # Transformar a imagem de RGB para HSV
    for y in range(height):
        row = []

        for x in range(width):
            pxl = img.getpixel((x, y))
            new_pxl = rgb_to_hsb(pxl)
            row.append(new_pxl)

        img_hsv.append(row)


    # Aplicar o filtro
    for y in range(height):
        row = []

        for x in range(width):
            pxl = img_hsv[y][x]

            if (pxl[0] + ad_m) <= 255:
                h = int(pxl[0] + ad_m)
            else:
                h = 255

            if (pxl[1] * mult_s) <= 255:
                s = int(pxl[1] * mult_s)
            else:
                s = 255

            if (pxl[2] * mult_b) <= 255:
                b = int(pxl[2] * mult_b)
            else:
                b = 255

            new_pxl = [h, s, b]
            row.append(new_pxl)

        new_img.append(row)

    # Transformar a imagem de HSV em RGB
    for y in range(height):
        for x in range(width):
            pxl = new_img[y][x]
            new_pxl = hsb_to_rgb(pxl)
            img_rgb.putpixel((x, y), tuple(new_pxl))

    img_rgb.show()

#Testes   
if __name__ == '__main__':  
    # Imagem normal        
    mult_ad_filter(0, 1, 1)

    # Imagem em preto e branco (saturação 0)
    mult_ad_filter(0, 0, 1)

    # Imagem preta (brilho 0)
    mult_ad_filter(0, 1, 0)

    # Imagens com diferentes valores de matiz
    mult_ad_filter(50, 1, 1)
    mult_ad_filter(100, 1, 1)
    mult_ad_filter(150, 1, 1)
    mult_ad_filter(200, 1, 1)
    mult_ad_filter(250, 1, 1)

    # Imagens aplicando os três filtros simultaneamente
    mult_ad_filter(-255, 1, 1)
    mult_ad_filter(0, 0.5, 1)
    mult_ad_filter(0, 1, 0.2)