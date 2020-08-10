function genPH()
    %for i=12:15
    %    fname = int2str(i)
    %for i=1:10
    %    mat = randi(256,87,85);
        fname = '04_8184';
        mat = imread([fname '.tif']);
        % mat(mat>128) = 128;
        %fname = [fname '_128'];
        runPerseus(fname,mat,2);
    %persdia([fname '_1.txt']);
    %savefig(figure,[fname 'persdia.png']);
end
