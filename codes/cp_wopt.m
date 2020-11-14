% num_gene1 = 18719;
% num_gene2 = 14673;
% num_gene_2 = 18719;
num_gene1 = 1001;
num_gene2 = 1001;
num_cancer_type = 1;
P = tenones([num_gene1 num_gene2 num_cancer_type]);
R = 1000;

% read tensor
exp_tensor = tenzeros([num_gene1, num_gene2, num_cancer_type]);
tensor_root = 'C:/Users/xiongxiaoji/Documents/GitHub/DTF-Drug-Synergy/data_sets/tensor/';
for i = 1:(num_cancer_type)
    file_to_read = strcat(tensor_root, 'tensor_',num2str(i),'.csv')
    exp_tensor(:,:,i) = csvread(file_to_read,1,1);
end
% num_predict = 240 * num_cancer_type;

% use P to locate valid & missing values
% 1 means valid, while 0 means missing
P = tenzeros([num_gene1 num_gene2 num_cancer_type]);
% In Matlab index starts from 1
% miss = [0, 5, 6, 8, 10, 12, 14, 17, 18, 19, 26, 27, 29, 33, 34, 35] +1;
count = 0;
for k = 1:num_cancer_type
    valid_path =  strcat('../data_sets/location/valid_',...
        string(k),'.csv');
    valid = csvread(valid_path,1,1);
    for row = 1:num_gene1
        for col = 1:num_gene2
            if valid(row, col) == 1
                P(row, col, k) = 1
                count = count + 1;
            end
        end 
    end 
end 


%get indexes of val set
data = csvread('../data_sets/final_data/fold_0_final.csv');


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

tmp_folder = '/Users/apple/Desktop/tensor_pro/project_sim/final_dtf/';

to_write_name = strcat(tmp_folder,'drug_a.csv');
csvwrite(char(to_write_name), M.u{1} );

to_write_name = strcat(tmp_folder,'drug_b.csv');
csvwrite(char(to_write_name), M.u{2} );

to_write_name = strcat(tmp_folder,'cell_line.csv');
csvwrite(char(to_write_name), M.u{3} );