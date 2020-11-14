num_drug_a = 38;
num_drug_b = 38;
num_cell_line = 39;
P = tenones([num_drug_a num_drug_b num_cell_line]);
R = 1000;

% read_data
num_predict = 240 * num_cell_line;

P = tenones([num_drug_a num_drug_b num_cell_line]);
miss = [0, 5, 6, 8, 10, 12, 14, 17, 18, 19, 26, 27, 29, 33, 34, 35] +1;

for k = 1:16
    for j = i+1:16
        P(miss(k),miss(j),:) = 0;
        P(miss(j),miss(k),:) = 0;
    end
end

%folder_name = '/Users/apple/Desktop/tensor_pro/project_sim/revison_data/';

for test_fold = 0:4
    folder_name = '/Users/apple/Desktop/tensor_pro/project_sim/revison_data/';

    tmp_data_name = strcat(folder_name ,'fold_',string(test_fold),'.csv');
    data = csvread(tmp_data_name);
    len = length(data);
    
    for k  = 1:len
        z = floor(data(k)/(num_drug_a * num_drug_b)) + 1;
        x_y = mod(data(k), num_drug_a * num_drug_b);
        x = mod(x_y,num_drug_b) + 1;
        y = floor(x_y/num_drug_a) + 1;
        P(x,y,z) = 0;
        P(y,x,z) = 0;
    end 
    
    [M,~,output] = cp_wopt(exp_tensor,P,R);
    
    folder_name = '/Users/apple/Desktop/tensor_pro/project_sim/5_fold_cv/';
    tmp_folder = strcat(folder_name ,'exclude_',string(test_fold),'/');

    to_write_name = strcat(tmp_folder,'drug_a.csv');
    csvwrite(char(to_write_name), M.u{1} );
    
    to_write_name = strcat(tmp_folder,'drug_b.csv');
    csvwrite(char(to_write_name), M.u{2} );
    
    to_write_name = strcat(tmp_folder,'cell_line.csv');
    csvwrite(char(to_write_name), M.u{3} );
    
    pre_tensor = full(M);
    %len = length(data);
    pre_data_test = zeros(len*2,1);
    true_data_test = zeros(len*2,1);
    for k = 1:len
        z = floor(data(k)/(num_drug_a * num_drug_b)) + 1;
        x_y = mod(data(k), num_drug_a * num_drug_b);
        x = mod(x_y,num_drug_b) + 1;
        y = floor(x_y/num_drug_a) + 1;
        pre_data_test(k) = pre_tensor(x,y,z);
        true_data_test(k) = exp_tensor(x,y,z);
        pre_data_test(len + k) = pre_tensor(y,x,z);
        true_data_test(len + k) = exp_tensor(y,x,z);
    end
    to_write_name = strcat(folder_name,'fold_',string(test_fold),'_pre_cpwopt.csv');
    csvwrite(char(to_write_name),pre_data_test);
    
    to_write_name = strcat(folder_name,'fold_',string(test_fold),'_true_cpwopt.csv');
    csvwrite(char(to_write_name),true_data_test);
    
end