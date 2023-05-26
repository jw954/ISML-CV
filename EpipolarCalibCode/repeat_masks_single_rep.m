repvals = 480 %16

folder = 'Py_MaskPatterns';
folder = 'Py_MaskProj_600';

mkdir('EpipolarMasks')
H = 320;
W = 512;

for value = 90


for vals = repvals
    
    allFiles = dir(sprintf('%s/.bmp', folder));
    
    allPatterns = zeros(vals * numel(allFiles) * H, W);
    
    counter = 0;
    
    curPatterns = imread( sprintf('%s/dual_%03d.bmp', folder, value));
    for j = 1 : vals
        allPatterns(counter * H + (1 : H), :) = curPatterns;
        
        counter = counter + 1
    end
    
    imwrite(logical(allPatterns), sprintf('/home/demo/mian/EpipolarDemo/CamAPI_py/maskfile/single_epi.bmp'));
        imwrite(logical(allPatterns), sprintf('/home/demo/mian/EpipolarDemo/CamAPI_py/maskfile/white.bmp'));

    %sprintf('EpipolarMasks/single_direct_pattern=%03d_rep=%02d.bmp', value, vals)
    
end
end