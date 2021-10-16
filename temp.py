from gpiozero import CPUTemperature
# pip install gpiozero

def get_temp():
    cpu = CPUTemperature()
    return cpu.temperature

if __name__ == '__main__':
    print(f'Pi temp: {get_temp()}')
