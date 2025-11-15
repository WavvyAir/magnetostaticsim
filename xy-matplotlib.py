import numpy as np
import matplotlib.pyplot as plt
#import plotly.graph_objects as go


plt.style.use('dark_background')

N = 32

x = np.linspace(-10, 10, N)
y = np.linspace(-10, 10, N)
z = np.linspace(-10, 10, N)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

X_obs, Y_obs = np.meshgrid(x, y, indexing='ij')
Z_obs = np.zeros_like(X_obs)

dx = dy = dz = x[1] - x[0]

dV = dx * dy * dz

#Current flowing in z direction
j0 = 1.0
wire_radius = 2.0

mask1 = ((X)**2+(Y+3)**2 < wire_radius**2)
mask2 = ((X)**2+(Y-3)**2 < wire_radius**2)

JX = np.zeros_like(X)
JY = np.zeros_like(Y)
JZ = np.zeros_like(Z) + j0 * mask1 - j0 * mask2


Bx = np.zeros_like(X_obs)
By = np.zeros_like(Y_obs)
Bz = np.zeros_like(Z_obs)

for i in range(N):
  for j in range(N):
    for k in range(N):

      xp = X[i,j,k]
      yp = Y[i,j,k]
      zp = Z[i,j,k]

      delta_x = X_obs - xp
      delta_y = Y_obs - yp
      delta_z = Z_obs - zp

      r = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
      r[r < 1e-2]=1e-2

      Bx += (JY[i,j,k] * delta_z - JZ[i,j,k] * delta_y) / r**3
      By += (JZ[i,j,k] * delta_x - JX[i,j,k] * delta_z) / r**3
      Bz += (JX[i,j,k] * delta_y - JY[i,j,k] * delta_x) / r**3

Bx *= dV
By *= dV
Bz *= dV

magn = np.sqrt(Bx**2 + By**2 + Bz**2)
magn[magn < 1e-2] = 1e-2

Bx /= np.max(magn)
By /= np.max(magn)
Bz /= np.max(magn)


plt.figure(figsize=(10,10), dpi=150)
plt.quiver(X_obs, Y_obs, Bx, By, magn, cmap='plasma', scale= 35, pivot='middle')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title('Magentic Field xy-plane')
plt.show()
