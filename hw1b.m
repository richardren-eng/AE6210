clear
close all

function qdot = circ_orbit(t, q)
    mu = 6.6743e-11 * 5.972e24 / 1000^3; % km^3 / s^2 Standard gravitational constant for Earth
    qdot = zeros(4,1);
    qdot(1) = q(2);
    qdot(2) = -mu * q(1) / ( sqrt(q(1)^2 + q(3)^2) ^ 3 );
    qdot(3) = q(4);
    qdot(4) = -mu * q(3) / ( sqrt(q(1)^2 + q(3)^2) ^ 3 );
end

% Constants
mu = 6.6743e-11 * 5.972e24 / 1000^3; % km^3 / s^2 Standard gravitational constant for Earth
R = 6378; % km radius of Earth
h = 677; %km orbital altitude
r = R + h; % km Earth center to spacecraft center
V = sqrt(mu / r); % km/s orbital tangential speed

% Initial conditions
theta0 = 23 * pi / 180; % rad from the horizontal

x0 = r * cos(theta0); % km
y0 = r * sin(theta0); % km
xdot0 = -V * sin(theta0); % km/s
ydot0 = V * cos(theta0); % km/s
q0 = [x0 xdot0 y0 ydot0];

% Time interval
tspan = [0 3600*36]; % s

% Numerically solve
options = odeset('RelTol',1e-10,'AbsTol',1e-10); % Adjust tolerances 
[t, q] = ode45(@circ_orbit, tspan, q0, options);

% Time in hours
t = t/3600; % hours

% Plot results
figure

% X and Y positions vs. Time
% Extract Coordinates 
x = q(:, 1);
y = q(:, 3);

subplot(2,2,1)
hold on
plot(t, x, 'b', 'LineWidth', 4, 'DisplayName', 'x position') 
plot(t, y, 'r', 'LineWidth', 4, 'DisplayName', 'y position') 
xlabel('Time (hours)')
ylabel('Position (km)')
title('X and Y Positions vs Time')
legend('Location', 'best') 
hold off

% Velocities vs. Time
subplot(2,2,2)
hold on

% Extract Components of Velocity
xdot = q(:, 2); % Velocity along x-axis
ydot = q(:, 4); % Velocity along y-axis

plot(t, xdot, 'b', 'LineWidth', 4, 'DisplayName', 'x velocity') 
plot(t, ydot, 'r', 'LineWidth', 4, 'DisplayName', 'y velocity') 
xlabel('Time (hours)')
ylabel('Velocity (km/h)')
title('X and Y Velocities vs Time')
legend('Location', 'best') 
hold off

% Invariant Values vs Time
% Distance from Earth's center to spacecraft
ro2p = sqrt(x.^2 + y.^2); 
normed_ro2p = ro2p / max(ro2p);

% Kinetic Energy
ke = 1/2 * (xdot.^2 + ydot.^2);
normed_ke = ke / max(ke);

% Magnitude of Angular Momentum
ho2p = sqrt(x.^2 + y.^2) .* sqrt(xdot.^2 + ydot.^2);
normed_ho2p = ho2p / max(ho2p);

subplot(2,2,3)
hold on
plot(t, normed_ro2p, 'k', 'LineWidth', 4, 'DisplayName', "Distance from Earth's Center") 
plot(t, normed_ke, 'm', 'LineWidth', 4, 'DisplayName', "Kinetic Energy") 
plot(t, normed_ho2p, 'c', 'LineWidth', 4, 'DisplayName', "Magnitude of Angular Momentum") 

xlabel('Time (hours)')
ylabel('Normalized rel. to Max Values')
title('Normalized Invariant Values')
legend('Location', 'best')
hold off

% Orbit in XY plane
subplot(2,2,4)
plot(x, y, 'm', 'LineWidth', 4)
xlabel('x position (km)')
ylabel('y position (km)')
title('Orbital Trajectory in XY Plane')
axis equal 

sgtitle('Orbital Dynamics')

