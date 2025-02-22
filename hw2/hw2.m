clear
addpath('..')        

% Known Values
t = 25; % s
wia_A = [1; 2; 3]; % rad/s
alpha_ia_A = [0.1; 0.2; 0.3]; % rad/s
v_ic_A = [4; 5; 6]; % m/s
a_ic_A = [0.4; 0.5; 0.6]; % m/s^
x0 = 1.5; % m
z0 = -2.5; % m
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
      0   cos(beta)     -sin(beta);
      0   sin(beta)      cos(beta)];

RAB = RAH*RHB;

% Problem 1
% Angular velocity of frame H relative to frame A
wah_A = [0; 0; wH];

% Angular velocity of frame B relative to frame H
whb_B = [wb*beta1*cos(wb*t); 0; 0];

% Angular velocity of frame B relative to frame I
wib_A = wia_A + wah_A + RAB * whb_B
wib_B = RAB' * wib_A

% Problem 2
% Angular acceleration of frame B relative to frame H
% Derivative in the H frame of w_{hb}
D_whb_H = [-wb^2*beta1*sin(wb*t) ; 0 ; 0]; 

% Angular acceleration of frame B relative to frame I
alpha_ib_A = alpha_ia_A + cross(wia_A , wah_A) + RAH * D_whb_H + cross(wia_A + wah_A, RAB*whb_B)

% Problem 3
% Position of point O relative to point C
rco_A = [x0; 0; z0];

% Position of point P relative to point O
rop_H = [0; rh; 0];

% Position of point T relative to point P
rpt_B = [0; L; 0];

% Velocity of rotor tip relative to frame I
v_it_A = v_ic_A + cross(wia_A , rco_A) + cross(wia_A + wah_A , RAH*rop_H) + cross(wib_A , RAB*rpt_B)

% Problem 4
wih_A = wia_A + wah_A;
D_wah_A = cross(wia_A , wah_A);

% Acceleration of rotor tip relative to frame I
first_term = a_ic_A;
second_term = cross(alpha_ia_A , rco_A) + cross(wia_A , cross(wia_A , rco_A));
third_term = cross(alpha_ia_A , RAH*rop_H) + cross(cross(wia_A , wah_A) , RAH*rop_H) + cross(wih_A , cross(wih_A , RAH*rop_H));
fourth_term = cross(alpha_ib_A , RAB*rpt_B) + cross(wib_A , cross(wib_A , RAB*rpt_B));

a_it_A = first_term + second_term + third_term + fourth_term
