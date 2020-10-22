
data = read.csv('C:/Users/xiongxiaoji/Desktop/41467_2018_4647_MOESM4_ESM.csv', header = TRUE, nrows = 100)
# data = data[1:100, ]
# summary(data)
# class(data)
cancer_type = data$cancer_type
# encode a vector as a factor (the terms 'category' and 'enumerated type' are also used for factors).
cancer_type = factor(cancer_type) 
length(cancer_type) 
cancer_type = sort(cancer_type) 
all_cancer_type = levels(cancer_type) 
# print(all_cancer_type)
all_cancer_type_length = length(all_cancer_type) # 8
# print(data$gene1[1:3])
all_gene1 = levels(data$gene1) 
length(all_gene1) # 18719
# print(all_gene1[1:3])

all_gene2 = levels(data$gene2) 
length(all_gene2) # 14673
all_gene = union(all_gene1,all_gene2)
all_info = data
# print(all_info)
all_gene_length = length(all_gene)
length(all_gene) # 18719
# encode as number
for(i in 1:all_gene_length)
{
  all_info$gene1 = gsub(pattern = all_gene[i], i,all_info$gene1)
  all_info$gene2 = gsub(pattern = all_gene[i], i,all_info$gene2)
}
all_info$gene1 = as.numeric(all_info$gene1)
all_info$gene2 = as.numeric(all_info$gene2)


# ans = 0
# for(i in 1:23052)
# {
#         if(is.na(as.numeric(all_info$drug_b_name[i])))
#         {
#                 ans = ans +1
#         }
# }
# print(all_cancer_type)
ans = 0
for(p in 1: all_cancer_type_length){
  cancer_type_tmp = subset(all_info,cancer_type == all_cancer_type[p])
  # print(cancer_type_tmp)
  # for(i in 1:604)
  # {
  #         if(is.na(as.numeric(cell_line_1$drug_b_name[i])))
  #         {
  #                 ans = ans +1
  #         }
  # }
  print(length(cancer_type_tmp))
  set_del=(0)
  tmp_r = nrow(cancer_type_tmp)
  if(tmp_r %% 2 )
    tmp_r = tmp_r - 1 
  for( i in seq(1,tmp_r,2))
  {
    if(cancer_type_tmp$gene1[i] == cancer_type_tmp$gene1[i+1 ] &&
       cancer_type_tmp$gene2[i] == cancer_type_tmp$gene2[i+1 ] )
    {
      # cancer_type_tmp$synergy[i+1] = 0.5*(cell_line_tmp$synergy[i] +
      #                                    cell_line_tmp$synergy[i+1])
      
      set_del = union(set_del,i)
      
    }
  }
  if(tmp_r %% 2 )
    tmp_r = tmp_r + 1 else
    tmp_r = tmp_r - 1 
  for( i in seq(2,tmp_r,2))
  {
    if(cancer_type_tmp$gene1[i] == cancer_type_tmp$gene1[i+1 ] &&
       cancer_type_tmp$gene2[i] == cancer_type_tmp$gene2[i+1 ] )
    {
      # cancer_type_tmp$synergy[i+1] = 0.5*(cell_line_tmp$synergy[i] +
      #                                     cell_line_tmp$synergy[i+1])
      set_del = union(set_del,i)
    }
  }
  
  set_del = setdiff(set_del,0)
  if(length(set_del) > 0 )
    cancer_type_tmp = cancer_type_tmp[-set_del,]
  
  #tmp_o = matrix(nrow = 38, ncol = 38,0)
  tmp_o = matrix(nrow = length(all_gene_length) + 1, ncol = length(all_gene_length) + 1)
  test_num = 37
  ans = 0
  for( i in 1:nrow(cancer_type_tmp))
  {
    tmp_o[cancer_type_tmp$gene1[i],
          cancer_type_tmp$gene2[i]] = 
      cancer_type_tmp$SL[i]
    #sink('ans.txt')
    #print(tmp_o[as.numeric(cell_line_1$drug_a_name[i]),
    #as.numeric(cell_line_1$drug_b_name[i])])
    #ans =ans + 1
    #print(ans)
    
    # if( is.na(tmp_o[as.numeric(cell_line_1$drug_a_name[i]),
    #                 as.numeric(cell_line_1$drug_b_name[i])]))
    #         print(i)
  }
  #print(sum(!is.na(tmp_o)))
  
  
  
  
  for( i in 1:all_gene_length+1)
  {
    #if(all_drug_a[i] == all_drug_b[i])
    tmp_o[i,i] = 0 # 和自己的合成效果为0
    
    for( j in (i+1):all_gene_length+1)
      {
        if(!is.na(tmp_o[i,j]))
          tmp_o[j,i] = tmp_o[i,j]
        else if(!is.na(tmp_o[j,i]))
          tmp_o[i,j] = tmp_o[j,i]
    }
  }
  print(all_gene_length)
  tmp_o[all_gene_length+1,all_gene_length+1] = 0
  
  tmp_o[is.na(tmp_o)] = 0 # missing value置0
  name = paste('tensor_',p,'.csv',sep='')
  write.csv(tmp_o,name)
  
}

