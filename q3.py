from PIL import Image
from q1 import rgb_to_hsb, hsb_to_rgb

def aplica_saturacao(path_1,path_2):
    img_giver = Image.open(path_1)
    img_receiver = Image.open(path_2)

    pixels_giver = img_giver.load()
    pixels_receiver = img_receiver.load()

    # Ambas possuem as mesmas dimensões
    w, h = img_giver.size
    new_image = []
    
    for y in range(w):
        for x in range(h):
            # Pega saturação do pixel da imagem 1 e coloca no HSB da imagem 2
            giv_sat = rgb_to_hsb(pixels_giver[x,y])[1]
            rec_h, rec_s, rec_b = rgb_to_hsb(pixels_receiver[x,y])
            new_image.append(tuple(hsb_to_rgb([rec_h, giv_sat, rec_b])))

    image = Image.new("RGB", (w, h))
    image.putdata(new_image)

    image.show()

if __name__ == '__main__':
    aplica_saturacao('imagens/vermelho_claro.jpg','imagens/azul_cinzado.jpg')
    aplica_saturacao('imagens/azul_cinzado.jpg','imagens/vermelho_claro.jpg')
    aplica_saturacao('imagens/azul_cinzado.jpg','imagens/babuino.png')
    aplica_saturacao('imagens/vermelho_claro.jpg','imagens/babuino.png')
    aplica_saturacao('imagens/cinza.jpg','imagens/babuino.png')
    aplica_saturacao('imagens/cinza.jpg','imagens/vermelho_claro.jpg')
    aplica_saturacao('imagens/cinza.jpg','imagens/azul_cinzado.jpg')