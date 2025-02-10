clear
syms x1dd y1dd tet1dd x2dd y2dd tet2dd Fx Fy

L = 0.3; % m
w = 0.1; % m
b = 0.04; % m
m = 0.1; % kg
g = 9.81; % m/s^2


x1 = 1; % m
y1 = 2; % m
tet1 = 0.1; % rad
tet2 = 0.2; % rad
x1d = 0.15; % m/s
y1d = 0.25; % m/s
tet1d = 0.35; % rad/s
tet2d = 0.45; % rad/s

xp = x1 + (L/2 - b) * cos(tet1);
yp = y1 + (L/2 - b) * sin(tet1);

x2 = x1 + (L/2 - b) * (cos(tet1) + cos(tet2));
y2 = y1 + (L/2 - b) * (sin(tet1) + sin(tet2));

Izz_C = m * (w^2+L^2)/12; % kg*m^2
J1 = Izz_C + m * (x1^2 + y1^2);
J2 = Izz_C + m * (x2^2 + y2^2);

eqn1 = Fx == m*x1dd;
eqn2 = Fy - m*g == m*y1dd;
eqn3 = -x1*m*g - yp * Fx + xp * Fy == J1 * tet1dd;
eqn4 = -Fx == m*x2dd;
eqn5 = -Fy - m*g == m*y2dd;
eqn6 = yp * Fx - xp * Fy - m*g*x2 == J2 * tet2dd;
eqn7 = x2dd == x1dd - (L/2 - b) * (tet1d^2 * cos(tet1) + tet2d^2 * cos(tet2));
eqn8 = y2dd == y1dd - (L/2 - b) * (tet1d^2 * sin(tet1) + tet2d^2 * sin(tet2));

sol = vpasolve([eqn1, eqn2, eqn3, eqn4, eqn5, eqn6, eqn7, eqn8] , ...
    [x1dd, y1dd, tet1dd, x2dd, y2dd, tet2dd, Fx, Fy])