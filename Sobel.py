from PIL import Image

def grayscale(colored):
    w, h = colored.size
    img = Image.new("RGB", (w, h))

    for x in range(w):
        for y in range(h):
            pxl = colored.getpixel((x,y))
            # media das coordenadas RGB gera a luminância
            lum = (pxl[0] + pxl[1] + pxl[2])//3
            img.putpixel((x,y),(lum,lum,lum))
    return img

def get_mask(archive_path):
    with open(archive_path, 'r') as file:
        linhas = file.readlines()

    # Processar as linhas para criar a matriz
    mascara = []
    for linha in linhas:
        # Dividir a linha nos espaços em branco e converter os valores para inteiros
        valores = [int(valor) for valor in linha.split()]
        mascara.append(valores)  

    return mascara 

def expansao_histograma(img,r_max,r_min):
    w, h = img.size
    image = Image.new("RGB", (w, h))
    print(r_min)
    print(r_max)
    for x in range(w):
        for y in range(h):
            pixel = img.getpixel((x,y))[0]
            resultado = round((pixel - r_min) / (r_max - r_min))
            if resultado:
                resultado = 255

            image.putpixel((x, y), (resultado, resultado, resultado))
            
    return image


def sobel_filter(img, mask):
    w, h = img.size
    image = Image.new("RGB", (w, h))
    
    r_max = 0
    r_min = 255


    for x in range(1, w-1):
        for y in range(1, h-1):
            gx = 0
            for i in range(len(mask[0])):
                for j in range(len(mask)):
                    gx+= mask[i][j]* img.getpixel((x+i-1,y+j-1))[0]

            image.putpixel((x, y), (gx, gx, gx))
            if gx > r_max:
                if gx > 255:
                    r_max = 255
                else:
                    r_max = gx
            elif gx < r_min:
                if gx < 0:
                    r_min = 0
                else:
                    r_min = gx

    image = expansao_histograma(image,r_max,r_min)

    return image

def sobel_sum(sobel_v, sobel_h):
    w, h = sobel_v.size
    image = Image.new("RGB", (w, h))
    for x in range(w):
        for y in range(h):
            pixel_sv = sobel_v.getpixel((x,y))[0]
            pixel_sh = sobel_h.getpixel((x,y))[0]
            if pixel_sv:
                image.putpixel((x, y), (pixel_sv, pixel_sv, pixel_sv))
            elif pixel_sh:
                image.putpixel((x, y), (pixel_sh, pixel_sh, pixel_sh))
            else :
                image.putpixel((x, y), (0, 0, 0))
    return image



if __name__ == "__main__":
    #img_original = Image.open("DancingInWater.jpg")
    img_original = Image.open("Shapes.png")
    img_gray = grayscale(img_original)

    # Processar as linhas para criar a matriz
    sobel_v_caminho = 'sobel_vertical.txt'
    mascara_sobel_v = []
    mascara_sobel_v = get_mask(sobel_v_caminho)
    imagem_filtrada_sv = sobel_filter(img_gray,mascara_sobel_v)

    sobel_h_caminho = 'sobel_horizontal.txt'
    mascara_sobel_h = []
    mascara_sobel_h = get_mask(sobel_h_caminho)
    imagem_filtrada_sh = sobel_filter(img_gray,mascara_sobel_h)

    sobel_total = sobel_sum(imagem_filtrada_sv,imagem_filtrada_sh)
    
    imagem_filtrada_sv.show()
    imagem_filtrada_sh.show()
    sobel_total.show()

    # imagem_filtrada_sv.save("imagem_filtrada_sv.jpg")
    # imagem_filtrada_sh.save("imagem_filtrada_sh.jpg")
    # sobel_total.save("sobel_total.jpg")
    


    
