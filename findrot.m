wib_A = [0.4143; 0.5405; -6.9962]; % Original vector
wib_B = [0.574005322936282; 0.28439903016616;-7.000000000000000];

% Normalize vectors
v1_hat = wib_A / norm(wib_A);
v2_hat = wib_B / norm(wib_B);

% Cross product (rotation axis)
k = cross(v1_hat, v2_hat);
k_norm = norm(k);

if k_norm == 0
    % If vectors are parallel or anti-parallel
    if dot(v1_hat, v2_hat) > 0
        R = eye(3); % No rotation
    else
        R = -eye(3); % 180-degree rotation
    end
else
    k = k / k_norm; % Normalize rotation axis
    theta = acos(dot(v1_hat, v2_hat)); % Angle of rotation

    % Skew-symmetric matrix for k
    K = [0, -k(3), k(2); k(3), 0, -k(1); -k(2), k(1), 0];

    % Rodrigues' rotation formula
    R = eye(3) + sin(theta) * K + (1 - cos(theta)) * (K * K);
end

disp('Rotation matrix R:');
disp(R);
