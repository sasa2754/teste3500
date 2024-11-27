import RPi.GPIO as GPIO
# from flask import Flask, Response
import cv2
import numpy as np
# from flask_cors import CORS
import time


url = "https://192.168.12.174:8080/video"
# Inicializa a webcam
cap = cv2.VideoCapture(url)

# Função para detectar uma linha amarela
def detec_line_yellow(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            frame_center_x = frame.shape[1] // 2
            error = cx - frame_center_x
            return frame, error
    return frame, None

# Função para seguir a linha amarela
# def process_delivery():
#     while True:  # Loop para seguir a linha amarela
#         success, frame = cap.read()
#         if not success:
#             print("Erro ao capturar frame da câmera.")
#             break

#         # Detecta a linha amarela
#         frame, error = detec_line_yellow(frame)

        # if error is None:
        #     continue

        # cv2.putText(frame, f'Alinhamento: {error}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        # Se encontrar a linha amarela, ajusta a direção
        # print(f"Erro de alinhamento: {error}")

        # Exibe o frame com feedback visual (opcional)
        # cv2.imshow('Robô', frame)

        # Sai se pressionar 'q'
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

# Flask streaming para a webcam
# def generate_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Rota para exibir o vídeo
# app = Flask(__name__)
# CORS(app)

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     process_delivery()  # Inicia a busca pela linha amarela
#     app.run(host="0.0.0.0", port=5000, debug=True)

IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def frente():
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

def tras():
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)

def direita():
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)

def esquerda():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

def parar_motores():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

def kau():
        frente()
        time.sleep(2)
        esquerda()
        time.sleep(0.7)
        frente()
        time.sleep(1.5)
        direita()
        time.sleep(0.6)
        frente()
        time.sleep(4.5)
        esquerda()
        time.sleep(0.7)
        frente()
        time.sleep(6)
        esquerda()
        time.sleep(0.7)
        frente()
        time.sleep(3)


try:
        kau()
    # process_delivery()
#     while True:
        # frente()
        # time.sleep(4)
        # direita()
        # time.sleep(0.6)
        # #     tras()
        # #     time.sleep(3)
        # #     esquerda()
        # frente()
        # time.sleep(2)
        # parar_motores()
        # direita()
        # time.sleep(0.6)
        # # time.sleep(1)
        # frente()
        # time.sleep(3)
        # tras()
        # time.sleep(4)
        #     success, frame = cap.read()
        #     if not success:
        #         print("Erro ao capturar frame da câmera.")
        #         break

        #     frame, error = detec_line_yellow(frame)

        #     print(error)
        #     if error is None:
        #         parar_motores()   

        #     else:
        #         if error > -150 and error < 150:
        #             frente()
        #         elif error < -150:
        #             direita()
        #         elif error > 150:
        #             esquerda()


except KeyboardInterrupt:
        print("programa interrompido")
        parar_motores()
finally:
        GPIO.cleanup()