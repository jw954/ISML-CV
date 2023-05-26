repvals = 16
doFlip = true;
folder = 'Py_MaskPatterns';
folder = 'privacy_Py_MaskPatterns';

totalNumber = 30;
H = 320;
W = 512;


for vals = repvals 
    
    allFiles = dir(sprintf('%s/*.bmp', folder));
    
    allPatterns = zeros(vals * totalNumber * H, W);
    
    counter = 0;
    for i  = 1 : totalNumber
       curPatterns = imread( sprintf('%s/%s', folder, allFiles(i).name));
       for j = 1 : vals
           
       if doFlip == false
        allPatterns(counter * H + (1 : H), :) = curPatterns;
       else
        allPatterns((totalNumber*vals - counter - 1) * H + (1 : H), :) = circshift(curPatterns,[0,0]);
       end
       
       
       counter = counter + 1
       end
    end
    %imwrite(logical(allPatterns), sprintf('/home/demo/mian/test/CamAPI_py/maskfile/%s_num%02d_rep=%02d.bmp', folder, totalNumber, vals));
    imwrite(logical(allPatterns), sprintf('/home/demo/mian/EpipolarDemo/CamAPI_py/maskfile/%s_num%02d_rep=%02d.bmp', folder, totalNumber, vals));

end