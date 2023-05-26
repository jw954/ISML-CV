repvals = [8, 16 ,32]

folder = 'Py_MaskPatterns';

H = 320;
W = 512;

value = 0

for vals = repvals
    
    allFiles = dir(sprintf('%s/.bmp', folder));
    
    allPatterns = zeros(vals * numel(allFiles) * H, W);
    
    counter = 0;
    
    curPatterns = imread( sprintf('%s/dual_%03d.bmp', folder, value));
    for j = 1 : vals
        allPatterns(counter * H + (1 : H), :) = curPatterns;
        
        counter = counter + 1
    end
    
    imwrite(logical(allPatterns), sprintf('/home/demo/mian/test/CamAPI_py/maskfile/direct_pattern=%03d_rep=%02d.bmp', value, vals));
    
end
