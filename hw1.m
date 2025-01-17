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

% Initial conditions
x0 = 6500; % km
y0 = 2700; % km

% Constants
mu = 6.6743e-11 * 5.972e24 / 1000^3; % km^3 / s^2 Standard gravitational constant for Earth
r = sqrt(x0^2 + y0^2); % km radius from Earth's center to spacecraft
V = sqrt(mu / r); % km/s orbital tangential speed
xdot0 = -V * y0/r; % km/s
ydot0 = V * x0/r; % km/s

q0 = [x0 xdot0 y0 ydot0];

% Time interval
tspan = [0 3600*17]; % s

% Numerically solve
options = odeset('RelTol',1e-5,'AbsTol',1e-6); % Adjust tolerances 
[t, q] = ode45(@circ_orbit, tspan, q0, options);

% Time in hours
t = t/3600; % hours

% Plot results
figure

% X and Y positions vs. Time
% Extract Coordinates 
x = q(:, 1);
y = q(:, 3);

subplot(2,1,1)
hold on
plot(t, x, 'b', 'LineWidth', 4, 'DisplayName', 'x position') 
plot(t, y, 'r', 'LineWidth', 4, 'DisplayName', 'y position') 
xlabel('Time (hours)')
ylabel('Position (km)')
title('X and Y Positions vs Time')
legend('Location', 'best') 
hold off

% Velocities vs. Time
subplot(2,1,2)
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


% Invariant Values vs Tim
% Distance from Earth's center to spacecraft
rsim = sqrt(x.^2 + y.^2); 
radius_error = (r - rsim)/r * 100; % percent

% Kinetic Energy
kesim = 1/2 * (xdot.^2 + ydot.^2);
ke_error = (1/2*V^2 - kesim) / (1/2*V^2) * 100; % percent

% Magnitude of Angular Momentum
hsim = sqrt(x.^2 + y.^2) .* sqrt(xdot.^2 + ydot.^2);
h_error = (r*V - hsim) / (r*V) * 100; % percent 

figure
subplot(2,1,1)
hold on
plot(t, radius_error, 'k', 'LineWidth', 4, 'DisplayName', "Distance from Earth's Center") 
plot(t, ke_error, 'm', 'LineWidth', 4, 'DisplayName', "Kinetic Energy") 
plot(t, h_error, 'c', 'LineWidth', 4, 'DisplayName', "Magnitude of Angular Momentum") 

xlabel('Time (hours)')
ylabel('Percent Error (%)')
title('Percent Errors of Invariants')
legend('Location', 'best')
hold off
latex_fig(12, 6.5, 3.3)

% Orbit in XY plane
subplot(2,1,2)
plot(x, y, 'm', 'LineWidth', 4)
xlabel('x position (km)')
ylabel('y position (km)')
title('Orbital Trajectory in XY Plane')
axis equal 

latex_fig(12, 6.5, 3.3)