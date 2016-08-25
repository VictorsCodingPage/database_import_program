switch_dict_female_to_male = {3: 23, 4: 22, 5: 25, 6: 21, 8: 27, 16: 32, 17: 33, 18: 34, 20: 37, 39: 35, 38: 36}
switch_dict_male_to_female = {23: 3, 22: 4, 25: 5, 21: 6, 27: 8, 32: 16, 33: 17, 34: 18, 37: 20, 35: 39, 36: 38}

print switch_dict_male_to_female.get(25)
print switch_dict_female_to_male.get(5)