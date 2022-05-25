import cv2
import mediapipe as mp
import math
import time

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

#Se realiza la videocaptura
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Variables de conteo
parpadeo = False
conteo = 0
tiempo = 0
inicio = 0
final = 0
conteo_sue = 0
muestra = 0


with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,  #rostros a detectar
    min_detection_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        #Listas para almacenar los resultados
        px = []
        py = []
        lista = []
        r= 5
        t = 3

        if results.multi_face_landmarks is not None: 
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
        
                #Se extraen los puntos del rostro detectado
                for id,puntos in enumerate(face_landmarks.landmark):

                    #print(puntos) Proporción
                    al, an, c = frame.shape
                    x,y = int(puntos.x*an), int(puntos.y*al)
                    px.append(x)
                    py.append(y)
                    lista.append([id,x,y])

                    if len(lista) == 468:

                    #Ojo derecho
                        x1, y1 = lista[145][1:]
                        x2, y2 = lista[159][1:]
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                        #cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), t)
                        #cv2.circle(frame, (x1, y1), r, (0, 0, 0), cv2.FILLED)
                        #cv2.circle(frame, (x2, y2), r, (0, 0, 0), cv2.FILLED)
                        #cv2.circle(frame, (cx, cy), r, (0, 0, 0), cv2.FILLED)

                        longitud1 = math.hypot(x2 - x1, y2 - y1)
                        #print(longitud1)

                    


                        #Ojo izquierdo
                        x3, y3 = lista[374][1:]
                        x4, y4 = lista[386][1:]
                        cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                        longitud2 = math.hypot(x4 - x3, y4 - y3)

                        #Detección de microsueño
                        cv2.putText(frame, f'Parpadeos: {int(conteo)}', (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),3)
                        cv2.putText(frame, f'Microsueños: {int(conteo_sue)}', (780, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),3)
                        cv2.putText(frame, f'Duración: {int(muestra)}', (550, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),3)

                        if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False: # Parpadeo
                            conteo = conteo + 1
                            parpaedo = True 
                            inicio = time.time()

                        elif longitud2 > 10 and longitud2 > 10 and parpadeo == True: #Seguridad parpadeo
                            parpadeo = False
                            final = time.time()

                        #Duración del parpadeo
                        tiempo = round(final - inicio, 0)

                        if tiempo >= 3:
                            conteo_sue = conteo_sue + 1
                            muestra = tiempo
                            inicio = 0
                            final = 0

        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
cap.release()
cv2.destroyAllWindows()