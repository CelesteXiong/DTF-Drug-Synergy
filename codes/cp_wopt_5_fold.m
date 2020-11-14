num_gene1 = 1001;
num_gene2 = 1001;
num_cancer_type = 1;
P = tenones([num_gene1 num_gene2 num_cancer_type]);
R = 1000;

% read_data
% read tensor
exp_tensor = tenzeros([num_gene1 num_gene2 num_cancer_type]);
tensor_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor/';
for i = 1:(num_cancer_type)
    file_to_read = strcat(tensor_root, 'tensor_',num2str(i),'.csv')
    exp_tensor(:,:,i) = csvread(file_to_read,1,1);
end
% num_predict = 240 * num_cell_line;

% use P to locate valid & missing values
% 1 means valid, while 0 means missing
P = tenzeros([num_gene1 num_gene2 num_cancer_type]);
% In Matlab index starts from 1
count = 0;
for k = 1:num_cancer_type
    valid_path =  strcat('C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/location/valid_',...
        num2str(k),'.csv');
    valid = csvread(valid_path,1,1);
    for row = 1:num_gene1
        for col = 1:num_gene2
            if valid(row, col) == 1
                P(row, col, k) = 1;
                count = count + 1;
            end
        end 
    end 
end 


for test_fold = 0:4
    folder_name = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/fold';

    tmp_data_name = strcat(folder_name ,'/',  num2str(test_fold),'/index.csv')
    data = csvread(tmp_data_name, 1, 0);
    len = length(data)
    
    for k  = 1:len
        z = floor(data(k)/(num_gene1 * num_gene2)) + 1;
        x_y = mod(data(k), num_gene1 * num_gene2);
        x = mod(x_y,num_gene2) + 1;
        y = floor(x_y/num_gene1) + 1;
        P(x,y,z) = 0;
        P(y,x,z) = 0;
    end 
    
    [M,~,output] = cp_wopt(exp_tensor,P,R);
    
    folder_name = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/decomposition';
    tmp_folder = strcat(folder_name ,'exclude_',num2str(test_fold),'/');

    to_write_name = strcat(tmp_folder,'gene1.csv');
    csvwrite(char(to_write_name), M.u{1} );
    
    to_write_name = strcat(tmp_folder,'gene2.csv');
    csvwrite(char(to_write_name), M.u{2} );
    
    to_write_name = strcat(tmp_folder,'cancer_type.csv');
    csvwrite(char(to_write_name), M.u{3} );
    
    % pre_tensor = full(M);
    % %len = length(data);
    % pre_data_test = zeros(len*2,1);
    % true_data_test = zeros(len*2,1);
    % for k = 1:len
    %     z = floor(data(k)/(num_drug_a * num_drug_b)) + 1;
    %     x_y = mod(data(k), num_drug_a * num_drug_b);
    %     x = mod(x_y,num_drug_b) + 1;
    %     y = floor(x_y/num_drug_a) + 1;
    %     pre_data_test(k) = pre_tensor(x,y,z);
    %     true_data_test(k) = exp_tensor(x,y,z);
    %     pre_data_test(len + k) = pre_tensor(y,x,z);
    %     true_data_test(len + k) = exp_tensor(y,x,z);
    % end
    % to_write_name = strcat(folder_name,'fold_',string(test_fold),'_pre_cpwopt.csv');
    % csvwrite(char(to_write_name),pre_data_test);
    
    % to_write_name = strcat(folder_name,'fold_',string(test_fold),'_true_cpwopt.csv');
    % csvwrite(char(to_write_name),true_data_test);
    
end