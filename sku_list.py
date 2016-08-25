file = "wrong_gender_file.txt"
sku_array = []
with open(file,"r") as f:
	for line in f:
		temp = line.split("\t")[0]
		sku_array.append(temp.replace("SKU: ", ""))
	with open("only_sku.txt", "w") as output:
		for sku in sku_array:
			output.write(sku+", ")