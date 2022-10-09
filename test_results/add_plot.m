function add_plot(metric, version_name)
    % 度量方式为metric，添加version_name曲线
    
    file_name = '.\' + version_name + '\' + metric + '.txt';
    m = load(file_name);
    n = length(m);
    % n = 4;
    x = (1:n)*250;
    plot(x, m(1:n), "Marker", "*", 'LineWidth', 1.5);
end

