Folder = 'Py_single';

numIm = 32;


for i = 0 : numIm
    system(sprintf('cp %s/default.bmp %s/%02d_PAT.bmp', Folder, Folder, i));
end