# Source code for Market Basket Analysis to recommend products
from urllib.request import urlopen
products = ["P01","P02","P03","P04","P05","P06","P07","P08","P09","P10"]#available products
training_data = "http://kevincrook.com/utd/market_basket_training.txt"
testing_data = "http://kevincrook.com/utd/market_basket_test.txt"
# Calculating frequencies of 4-item,3-item,2-item lists
def frequency_prod():
    frequency_2products = {}
    frequency_3products = {}
    frequency_4products = {}# dictionaries with key-value pairs 
    prsnt_product = []
    data_load = urlopen(training_data)
    for eachline in data_load:
        split_line = eachline.decode("utf-8").strip().split(',')[1:]#splitting keys and value separated by comma
        # searching products in the training data
        [prsnt_product.append(x) for x in split_line if x not in prsnt_product]
        key_in_the_line = ",".join(split_line)
        if(len(split_line)== 4):# if count is 4 place it in 4 products list
            if(key_in_the_line in frequency_4products.keys()):
                frequency_4products[key_in_the_line] += 1
            else:
                frequency_4products[key_in_the_line] = 1
        elif(len(split_line)==3):# if count is 3 place it in 3 products list
            if(key_in_the_line in frequency_3products.keys()):
                frequency_3products[key_in_the_line] += 1
            else:
                frequency_3products[key_in_the_line] = 1
        elif(len(split_line)==2):# if count is 2 place it in 2 products list
            if(key_in_the_line in frequency_2products.keys()):
                frequency_2products[key_in_the_line] += 1
            else:
                frequency_2products[key_in_the_line] = 1
    return frequency_2products, frequency_3products, frequency_4products ,prsnt_product
# find the best combination of products with highest frequency
def frequent_combination(frequency_map,key_searching):
    final_key = ""
    final_value = 0
    for m , n in frequency_map.items():
        key_setting = set(m.split(","))
        if(key_searching < key_setting):
            if(final_value < n):
                final_value = n
                final_key = key_setting
    return final_key, final_value
#test data 
def testdata_frequency(frequency_2products, frequency_3products, frequency_4products,product_absence):
    final_solution = {}
    data = urlopen(testing_data)
    for eachline in data:
        split_line = eachline.decode("utf-8").strip().split(',')
        line_num = split_line[0]
        keys_in_the_line = split_line[1:]
        # discards products not in training data
        keys_in_the_line = set([x for x in keys_in_the_line if x not in product_absence])
        final_key = {}       
        if(len(keys_in_the_line) ==1):# if length  is 1 then search for 2 products set in training
            final_key, final_val = frequent_combination(frequency_2products, keys_in_the_line)      
        elif(len(keys_in_the_line)==2):# if length  is 2 then search for 3 products in training
            final_key, final_val = frequent_combination(frequency_3products,keys_in_the_line)      
        elif(len(keys_in_the_line)==3):# if length  is 3 then search for 4 products in training
            final_key, final_val = frequent_combination(frequency_4products,keys_in_the_line)        
        final_solution[line_num] = ",".join([x for x in final_key if x not in keys_in_the_line])# creates prodcut for recommendation
    return final_solution
#function to call the methods
if __name__ == '__main__':   
    frequency_2products, frequency_3products, frequency_4products, prsnt_product = frequency_prod()#creating frequency map
    product_absence = [x for x in products if x not in prsnt_product] #products missing in training set
    final_solution = testdata_frequency(frequency_2products, frequency_3products, frequency_4products, product_absence)#function to create recommendations
    fh = open('market_basket_recommendations.txt', 'w', encoding='utf8')#printing the output to text file
    for key in sorted(final_solution.keys()):
        print(key + "," + final_solution[key], file=fh)    
    fh.close()#close file
