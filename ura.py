from machine import Pin, ADC
import time

# Definições de pinos
pino_encoder = 0  # Pino D0 para o sinal do encoder
pino_a0 = 33  # Pino A0 para o módulo LM393 (supondo que esteja conectado ao LED emissor e fotodiodo)

# Variáveis globais
pulsos = 0
passos = 0
fracao_de_volta = 0
raio = 0.0325  # Exemplo de raio em metros
pulsos_por_volta = 20  # Substitua pelo número de pulsos por volta do encoder

# Inicialização de variáveis
timeold = time.ticks_ms()

def contador(pin):
    global pulsos
    global passos

    # Incrementa contador
    pulsos += 1
    passos += 1

# Configuração dos pinos
encoder = Pin(pino_encoder, Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(pino_a0))

# Configuração da interrupção
encoder.irq(trigger=Pin.IRQ_FALLING, handler=contador)

try:
    while True:
        # Atualiza o contador a cada segundo
        if time.ticks_diff(time.ticks_ms(), timeold) >= 3000:  # 3000 milissegundos = 3 segundos
            # Atualiza a fração de volta
            fracao_de_volta = passos / pulsos_por_volta
            passos = 0

            # Atualiza o tempo antigo
            timeold = time.ticks_ms()

        # Lê o valor do pino A0 (supondo que esteja conectado ao LED emissor/fotodiodo do LM393)
        valor_a0 = adc.read()

        # Calcula a distância percorrida em centímetros
        distancia_cm = 2 * 3.141592653589793 * raio * fracao_de_volta * 100  # Multiplica por 100 para converter para centímetros

        # Exibe informações no console para depuração
        print("Pulsos: {}, Passos: {}, Fração de Volta: {:.2f}, Distância: {:.2f} centímetros, Valor A0 = {}".format(pulsos, passos, fracao_de_volta, distancia_cm, valor_a0))

        time.sleep(3)

except KeyboardInterrupt:
pass