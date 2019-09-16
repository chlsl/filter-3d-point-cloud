% August 27, 2019.
% Create a test image for the clever filtering of 3D point clouds.
%

u = imread('~/thesis/ImBase/matias/matias_DarkSena1_735x551_color.jpg');
u = im2double(u);

u = u(61:460, 203:end, :);

figure(1); imshow(u);

g = sqrt(min(rgb2gray(u) / 0.9,1));
g( u(:,:,1) > .5 & u(:,:,2) > .5 & u(:,:,3) < .5 ) = nan;

figure(2); imshow(g); colormap gray



%% write file as tif

filename = 'test_image.tif';
img = g;

t = Tiff(filename, 'w');
tagstruct.ImageLength = size(img, 1);
tagstruct.ImageWidth = size(img, 2);
tagstruct.Compression = Tiff.Compression.None;
%tagstruct.Compression = Tiff.Compression.LZW;        % compressed
tagstruct.SampleFormat = Tiff.SampleFormat.IEEEFP;
tagstruct.Photometric = Tiff.Photometric.MinIsBlack;
tagstruct.BitsPerSample =  32;                        % float data
tagstruct.SamplesPerPixel = size(img,3);
tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky;
t.setTag(tagstruct);
t.write(single(img));
t.close();

