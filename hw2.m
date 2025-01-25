% Constants
t = 25; % s
w_ia_A = [1; 2; 3]; % rad/s
alpha_ia_A = [0.1; 0.2; 0.3]; % rad/s
v_ic_A = [4; 5; 6]; % m/s
a_ic_A = [0.4; 0.5; 0.6]; % m/s^2
x0 = 1.5; % m
y0 = -2.5; % m
wH = -10; % rad/s
rh = 0.5; % m
beta0 = -0.1; % rad
beta1 = 0.1; % rad
wb = 20; % rad/s
L = 10; % m

% Blade angle of rotation
tet = wH*t;

% Angle of blade flap
beta = beta0 + beta1 * sin(wb*t); % rad

% Rotation matrices
% R12 sends a vector resolved in frame 2 to the same vector resolved in
% frame 1
RAH = [cos(tet)   -sin(tet)   0; 
      sin(tet)   cos(tet)   0;
       0             0         1];

RHB = [1             0         0; 
      0   cos(beta)   sin(beta);
      0   -sin(beta)      cos(beta)];

% Angular velocity of frame H relative to frame I
wih_A = [0; 0; wH];

% Angular velocity of frame B relative to frame H
whb_B = [wb*beta1*cos(wb*t); 0; 0];

% Angular velocity of frame B relative to frame I
wib_A = wih_A + RAH*RHB * whb_B