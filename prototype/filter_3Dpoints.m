% August 27, 2019.
% Filter 3D point clouds (use test_image.tif) by counting the number of
% neighbors. When this number is under a threshold (3D point is alone...) then
% its value is considered as erroneous. We give erroneous pixels the value
% "nan".

clear variables
% close all
% clc

u = imread('test_image.tif');
% u = u(251:280, 271:300);

figure(1); imshow(u);

in_nan_vals = isnan(u);

figure(2); imshow(in_nan_vals);


% algo:
% step 1) find values that should be removed.
%         they are far in intensity from the other ones in their neighborhood
% step 2) 


% step 1

nb_of_neighbors = zeros(size(u));

for r = 1:size(u,1)
    for c = 1:size(u,2)
        nb_of_neighbors(r, c) = sum(sum(...
                                abs(u(max(1, r-1) : min(size(u,1), r+1), ...
                                      max(1, c-1) : min(size(u,2), c+1)) ...
                                    - u(r,c)) < 0.2));
    end
end

%%

figure(3); imagesc(nb_of_neighbors);
v = u;
rejected_pix_img = nb_of_neighbors < 6;
rejected_pix_img_saved = rejected_pix_img;
rejected_pix = find(nb_of_neighbors < 6);
v(rejected_pix) = NaN;

figure(4); imshow(v);
figure(5); imshow(rejected_pix_img); colormap winter

flag = true;
while flag
    flag = false;
%     fprintf('beginning of turn\n');
    for p = rejected_pix'
        [rr, cc] = ind2sub(size(u), p);
        
        % If the rejected pixel has (at least) one neighbor that is both not
        % rejected and close to its value, then it becomes not rejected too.

        rejected_local_patch = rejected_pix_img(...
                               max(1, rr-1) : min(size(u,1), rr+1), ...
                               max(1, cc-1) : min(size(u,2), cc+1));
        u_local_patch =      u(max(1, rr-1) : min(size(u,1), rr+1), ...
                               max(1, cc-1) : min(size(u,2), cc+1));
        not_rejected_pix = u_local_patch(~rejected_local_patch);
                           
%         fprintf('value = %5.3f (pix %3d %3d) rejected=%d.\n',...
%                 u(rr, cc), rr, cc, rejected_pix_img(rr, cc));
                           
        if ~isempty(not_rejected_pix)
%             fprintf('Cond1 True...');
            if  sum(abs(not_rejected_pix - u(p)) < 0.2) > 0
                rejected_pix_img(p) = false;
                rejected_pix(rejected_pix == p) = [];
                flag = true;
%                 fprintf(' Cond2 True  (pix %3d %3d).\n', rr, cc);
%             else
%                 fprintf(' Cond2 False (pix %3d %3d).\n', rr, cc);
            end
        end
    end
%     figure(5); imshow(rejected_pix_img); colormap winter
end

%%

figure(5); imshow(rejected_pix_img); colormap winter

v2 = u;
v2(rejected_pix_img) = NaN;

figure(6); imshow(v2);
figure(7); imagesc(rejected_pix_img_saved - rejected_pix_img);

