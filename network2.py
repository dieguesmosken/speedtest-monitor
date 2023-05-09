import psutil
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import messagebox
from datetime import datetime, timedelta


# Configuração do gráfico
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['animation.html'] = 'jshtml'

# Configuração dos dados
ys = []
xs = []
speeds_per_min = []
fig, ax = plt.subplots()
ax.set_ylim([0, 100])
ax.set_xlim([0, 60])
line, = ax.plot(xs, ys)

# Velocidades máxima e mínima
max_speed = 0
min_speed = float('inf')
text_max = ax.text(0.95, 0.95, f"Max: {max_speed:.2f} MB/s", transform=ax.transAxes, ha='right', va='top')
text_min = ax.text(0.95, 0.9, f"Min: {min_speed:.2f} MB/s", transform=ax.transAxes, ha='right', va='top')
avg_speed = 0
text_avg = ax.text(0.95, 0.85, f"Média: {avg_speed:.2f} MB/s", transform=ax.transAxes, ha='right', va='top')

# Função para coletar a porcentagem de uso da CPU
def get_network_speed():
    before = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    time.sleep(1)
    after = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    speed = (after - before) / 1024 / 1024 * 8
    print(f"Before: {before}, After: {after}, Speed: {speed}")
    return speed

start_time = datetime.now()

# Função de animação
def animate(i):
    speed = get_network_speed()
    xs.append((datetime.now() - start_time).total_seconds())
    ys.append(speed)
    xs = xs[-60:]
    ys = ys[-60:]
    line.set_xdata(xs)
    line.set_ydata(ys)
    
    # Atualiza as velocidades máxima e mínima
    max_speed = max(max_speed, speed)
    min_speed = min(min_speed, speed)
    text_max.set_text(f"Max: {max_speed:.2f} MB/s")
    text_min.set_text(f"Min: {min_speed:.2f} MB/s")
    
    # Atualiza a velocidade média a cada minuto
    if i > 0 and i % 60 == 0:
        avg_speed = sum(ys[-60:]) / 60
        speeds_per_min.append(avg_speed)
    
    # Atualiza o texto da velocidade média
    text_avg.set_text(f"Média: {avg_speed:.2f} MB/s")
    
    return line, text_max

# Inicia a animação
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
