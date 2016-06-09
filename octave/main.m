% ===== img gradient ======
pic_num = 17;
x = dir ("*.jpg");   # get struct of info on .jpg's in directory
for ii = 1:length (x)   # loop over jpg files
  img = imread (x(ii).name);   # read image file
  ## MANIPULATE IMAGE HERE
end
% img_g = imread('img/learn%d.png', pic_num);
% img_c = imread('img/clearn%d.png', pic_num);

% STEP 1: Take the gradient of the depth image.
% [Gx, Gy] = imgradient(img_g);