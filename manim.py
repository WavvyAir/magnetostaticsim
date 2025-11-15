class MagneticFieldSim(Scene):
    def construct(self):

        N = 100

        x = np.linspace(-10, 10, N)
        y = np.linspace(-10, 10, N)
        z = np.linspace(-10, 10, N)

        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

        # Observation plane: z = 0
        X_obs, Y_obs = np.meshgrid(x, y, indexing='ij')
        Z_obs = np.zeros_like(X_obs)

        dx = dy = dz = x[1] - x[0]
        dV = dx * dy * dz


        j0 = 1.0
        wire_radius = 2.0

        mask1 = (X**2 + (Y + 3)**2 < wire_radius**2)
        mask2 = (X**2 + (Y - 3)**2 < wire_radius**2)

        JX = np.zeros_like(X)
        JY = np.zeros_like(Y)
        JZ = j0 * mask1 - j0 * mask2

        Bx = np.zeros_like(X_obs)
        By = np.zeros_like(Y_obs)
        Bz = np.zeros_like(X_obs)

        for i in range(N):
            for j in range(N):
                for k in range(N):
                    xp = X[i, j, k]
                    yp = Y[i, j, k]
                    zp = Z[i, j, k]

                    delta_x = X_obs - xp
                    delta_y = Y_obs - yp
                    delta_z = Z_obs - zp

                    r = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
                    r[r < 1e-2] = 1e-2

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


        def interp_B(pos):
            
            xq, yq = pos[0], pos[1]

            i = int((xq - x[0]) / (x[1] - x[0]))
            j = int((yq - y[0]) / (y[1] - y[0]))

            if 0 <= i < N and 0 <= j < N:
                return np.array([Bx[i, j], By[i, j], 0])
            else:
                return np.array([0, 0, 0])

        func = lambda p: interp_B(p)

        stream_lines = StreamLines(
            func,
            stroke_width=2,
            max_anchors_per_line=30,
            virtual_time=6,
            colors=[BLUE, GREEN, YELLOW, ORANGE, RED]
        )

        arrows = ArrowVectorField(
            func,
            x_range=[-10, 10, 0.4],
            y_range=[-10, 10, 0.4]
        )

        self.add(stream_lines)
        self.add(arrows)

        stream_lines.start_animation(warm_up=False, flow_speed=1)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
