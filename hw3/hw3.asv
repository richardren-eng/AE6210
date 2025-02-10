% Case 1
clear
L = 0.3; % m
w = 0.1; % m
b = 0.04; % m
m = 0.1; % kg
g = 9.81; % m/s^2

x1 = 1;
y1 = 2;
tet1 = 0.1;
tet2 = 0.2;
x1d = 0.15;
y1d = 0.25;
tet1d = 0.35;
tet2d = 0.45;

Izz_C = m * (w^2+L^2)/12 % kg*m^2
Izz_P = m * (w^2/12 + L^2/3 - b*L + b^2) % kg*m^2

xp = x1 + (L/2 - b) * cos(tet1);
yp = y1 + (L/2 - b) * sin(tet1);

x2 = x1 + (L/2 - b) * (cos(tet1) + cos(tet2))
y2 = y1 + (L/2 - b) * (sin(tet1) + sin(tet2))

J1 = Izz_C + m * (x1^2 + y1^2);
J2 = Izz_C + m * (x2^2 + y2^2);

A = zeros(8,8);
A(1,:) = [m 0 0 0 0 0 -1 0];
A(2,:) = [0 m 0 0 0 0 0 -1];
A(3,:) = [0 0 Izz_C 0 0 0 (L/2-b)*sin(tet1) -(L/2-b)*cos(tet1)];
A(4,:) = [0 0 0 m 0 0 1 0];
A(5,:) = [0 0 0 0 m 0 0 1];
A(6,:) = [0 0 0 0 0 Izz_C (L/2-b)*sin(tet2) -(L/2-b)*cos(tet2)];
A(7,:) = [1 0 0 -1 0 0 0 0];
A(8,:) = [0 1 0 0 -1 0 0 0];

B = zeros(8,1);
B(1) = 0;
B(2) = -m*g;
B(3) = 0;
B(4) = 0;
B(5) = -m*g;
B(6) = 0;
B(7) = (L/2 - b) * (tet1d^2 * cos(tet1) + tet2d^2 * cos(tet2));
B(8) = (L/2 - b) * (tet1d^2 * sin(tet1) + tet2d^2 * sin(tet2));

q1 = A \ B

% Case 2
A = zeros(6,6);
A(1,:) = [m 0 0 0 -1 0];
A(2,:) = [0 m 0 0 0 -1];
A(3,:) = [0 0 Izz_C 0 (L/2-b)*sin(tet1) -(L/2-b)*cos(tet1)];
A(4,:) = [0 0 0 Izz_C (L/2-b)*sin(tet2) -(L/2-b)*cos(tet2)];
A(5,:) = [m 0 0 0 1 0];
A(6,:) = [0 m 0 0 0 1];

B = zeros(6,1);
B(1) = 0;
B(2) = -m*g;
B(3) = 0;
B(4) = 0;
B(5) = m * (L/2 - b) * (tet1d^2 * cos(tet1) + tet2d^2 * cos(tet2));
B(6) = m * (L/2 - b) * (tet1d^2 * sin(tet1) + tet2d^2 * sin(tet2)) - m*g;

q2 = A \ B

% Case 3

A = zeros(4,4);
A(1,:) = [m*(L/2 - b)*sin(tet1) , -m*(L/2-b)*cos(tet1) , Izz_C , 0];
A(2,:) = [m*(L/2 - b)*sin(tet2) , -m*(L/2-b)*cos(tet2) , 0 , Izz_C];
A(3,:) = [2 0 0 0];
A(4,:) = [0 2 0 0];


B = zeros(4,1);
B(1) = m*g*(L/2 - b)*cos(tet1);
B(2) = m*g*(L/2 - b)*cos(tet2);
B(3) = (L/2 - b) * (tet1d^2 * cos(tet1) + tet2d^2 * cos(tet2));
B(4) = (L/2 - b) * (tet1d^2 * sin(tet1) + tet2d^2 * sin(tet2)) - 2*g;

q3 = A \ B