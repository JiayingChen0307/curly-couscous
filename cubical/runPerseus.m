function runPerseus(fname, mat, dim)
    [n m] = size(mat);
    mat = double(mat);
    vec = reshape(mat, [], 1);
    dlmwrite(fname, [dim; n; m; vec],'delimiter','\t');
    cmd = ['/Users/jiaying/Downloads/TDA/TDAWorking/perseusMac cubtop ' fname ' ' fname]
    system(cmd);
end



