import cv2 
import mediapipe as mp 
import serial


camera = cv2.VideoCapture(0)
resolucao_x = 1280
resolucao_y = 720

camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucao_y) 

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils 
maos = mp_maos.Hands()
# Habilitar a porta serial para comunicar com arduino
arduino = serial.Serial('COM7', 9600)


def encontra_coordenadas_maos(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resultado = maos.process(img_rgb)
    todas_maos = []

    if resultado.multi_hand_landmarks:
        for lado_mao, marcacao_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_mao = {}
            coordenadas = []
            for marcacao in marcacao_maos.landmark:
                coord_x, coord_y, coord_z = int(marcacao.x * resolucao_x), int(marcacao.y * resolucao_y), int(marcacao.z * resolucao_x)
                coordenadas.append((coord_x, coord_y, coord_z))
            
            info_mao['coordenadas'] = coordenadas
            todas_maos.append(info_mao)
        mp_desenho.draw_landmarks(img, marcacao_maos, mp_maos.HAND_CONNECTIONS)
    
    return img, todas_maos


#Função para indificar a ponta dos dedos estão levantadas 
def dedos_levantados(mao):
    dedos = []
    for ponta_dedo in [8,12,16,20]:
        if mao['coordenadas'][ponta_dedo][1] < mao['coordenadas'][ponta_dedo - 2][1]:
            dedos.append(True)
        else:
            dedos.append(False)
    return dedos


while True:
    sucesso, img = camera.read()

    img = cv2.flip(img,1)
    
    img,todas_maos = encontra_coordenadas_maos(img)

    #Envia a mensagem C(se estiver correta a senha ) e envia a mensagem E(se estiver errada a senha)
    if len(todas_maos) == 1:
        info_dedo_mao1 = dedos_levantados(todas_maos[0])
        if info_dedo_mao1 == [True, False, False, True]:
            arduino.write('C'.encode())
        else:
            arduino.write('E'.encode())
        


        cv2.imshow('Imagem', img)    

    tecla = cv2.waitKey(1)
    if tecla == 27:
        break



