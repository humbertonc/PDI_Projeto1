from PIL import Image

def get_mask(archive_path):
    with open(archive_path, 'r') as file:
        linhas = file.readlines()

    # Processar as linhas para criar a matriz
    mascara = []
    for linha in linhas:
        # Dividir a linha nos espaços em branco e converter os valores para inteiros
        valores = [float(valor) for valor in linha.split()]
        mascara.append(valores)  

    return mascara 

def gaussian_filter(img, mask):
    w, h = img.size
    image = Image.new("RGB", (w, h))
    linhas_k = len(mask)
    colunas_k = len(mask[0])

    middle = linhas_k//2
    for x in range(middle, w-middle):
        for y in range(middle, h-middle):
            gr = 0
            gg = 0
            gb = 0
            for i in range(colunas_k):
                for j in range(linhas_k):
                    gr+= float(mask[i][j]* img.getpixel((x+i-middle,y+j-middle))[0])
                    gg+= float(mask[i][j]* img.getpixel((x+i-middle,y+j-middle))[1])
                    gb+= float(mask[i][j]* img.getpixel((x+i-middle,y+j-middle))[2])

            image.putpixel((x, y), (int(gr), int(gg), int(gb)))
            
    return image

def box_filter(img, mask):
    w, h = img.size
    image = Image.new("RGB", (w, h))
    print(w)
    print(h)
    linhas_k = len(mask)
    colunas_k = len(mask[0])

    offset_colunas = colunas_k // 2
    if colunas_k % 2:
        paridade_colunas = 0
    else:
        paridade_colunas = 1

    offset_linhas = linhas_k // 2
    if linhas_k % 2:
        paridade_linhas = 0
    else:
        paridade_linhas = 1
    
    print(offset_linhas)
    print(offset_colunas)

    for x in range(offset_linhas-paridade_linhas, h-offset_linhas):
        for y in range(offset_colunas-paridade_colunas, w-offset_colunas):
            
            gr = 0
            gg = 0
            gb = 0
            for i in range(linhas_k):
                for j in range(colunas_k):
                    gr+= float(mask[i][j]* img.getpixel((y+j-offset_colunas-paridade_colunas,x+i-offset_linhas-paridade_linhas))[0])
                    gg+= float(mask[i][j]* img.getpixel((y+j-offset_colunas-paridade_colunas,x+i-offset_linhas-paridade_linhas))[1])
                    gb+= float(mask[i][j]* img.getpixel((y+j-offset_colunas-paridade_colunas,x+i-offset_linhas-paridade_linhas))[2])

            image.putpixel((y, x), (int(gr), int(gg), int(gb)))
            
            
    return image


if __name__ == "__main__":
    # img_original = Image.open("imagens/DancingInWater.jpg")
    img_original = Image.open("imagens/Shapes.png")

    # Processar as linhas para criar a matriz
    gaussiano_caminho = 'mascaras/gaussiano_5x5.txt'
    mascara_gaussiano = []
    mascara_gaussiano = get_mask(gaussiano_caminho)
    imagem_filtrada_gau = gaussian_filter(img_original,mascara_gaussiano)

     # Processar as linhas para criar a matriz
    box_caminho = 'mascaras/media_1x26.txt'
    mascara_box = []
    mascara_box = get_mask(box_caminho)
    imagem_filtrada_box = box_filter(img_original,mascara_box)


    imagem_filtrada_box.show()
    imagem_filtrada_gau.show()