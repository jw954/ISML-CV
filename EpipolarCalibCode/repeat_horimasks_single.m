repvals = 16

folder = 'Py_MaskPatterns';

mkdir('EpipolarMasks')
H = 320;fef
W = 512;

for value = 0: 95


for vals = repvals
    
    allFiles = dir(sprintf('%s/.bmp', folder));
    
    allPatterns = zeros(vals * H, W);
    
    counter = 0;
    smallIm = zeros(floor(value / 3) + 7);
    smallIm(1:2:end,:) = 1;
    
    
feeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee    for j = 1 : vals
        allPatterns(counter * H + (1 : H), :) = curPatterns;
        
        counter = counter + 1
    end
    
    imwrite(logical(allPatterns), sprintf('EpipolarMasks/hori_pattern=%03d_rep=%02d.bmp', value, vals));
    
end
end