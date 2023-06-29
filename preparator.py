import pandas as pd
import re

df_old = pd.read_csv(r"path...\RASFF_old.csv", sep = ";")

df_old.drop(["Column1", "ACTION_TAKEN", "DISTRIBUTION_STAT",  
             "HAZARDS_CAT", "COUNT_DESTIN", "COUNT_CONCERN", 
             "CLASSIFICATION", "NUMBER", "REFERENCE"], inplace=True, axis=1)

df_new = pd.read_csv(r"path...\RASFF_new.csv", sep = ";")

df_new.drop(["CLASSIFICATION", "REFERENCE"], inplace=True, axis=1)

df_new = df_new[df_new["RISK DECISION"] != "undecided"]
df_new = df_new[df_new["RISK DECISION"] != "no risk"]

hazards = {}
keys = range(56385)
values = df_old["HAZARD"].str.split(",")

for i in keys:
    hazards[i] = values[i]

hazards_set = {i[0] for i in hazards.values()}

products = {}
keys = range(56385)

values = df_old["PRODUCT"].str.split(",")

for i in keys:
    products[i] = values[i]

products_set = {i[0] for i in products.values()}

countries = {}
keys = range(56385)
values = df_old["ORIGIN COUNTRY"].str.split(",")

for i in keys:
    countries[i] = values[i]

countries_set = {i[0] for i in countries.values()}

subjets_list = [i for i in df_new["SUBJET"]]

hazards_list = [[] for x in range(len(subjets_list))]

findmatches = re.compile(r"\b" +
                         r"\b|\b".join(re.escape(hazard) for hazard in hazards_set) +
                         r"\b")

for i in range(len(subjets_list)):
    hazards_list[i] = []
    
    for possible_match in set(findmatches.findall(subjets_list[i])):
        
        if possible_match in hazards_set:
            hazards_list[i].append(possible_match)
            
    if set(findmatches.findall(subjets_list[i])).isdisjoint(hazards_set): 
        hazards_list[i].append("unknown hazards")

countries_list = [[] for x in range(len(subjets_list))]

findmatches = re.compile(r"\b" +
                         r"\b|\b".join(re.escape(country) for country in countries_set) +
                         r"\b")

for i in range(len(subjets_list)):
    countries_list[i] = []
    
    for possible_match in set(findmatches.findall(subjets_list[i])):
        
        if possible_match in countries_set:
            countries_list[i].append(possible_match)
            
    if set(findmatches.findall(subjets_list[i])).isdisjoint(countries_set): 
        countries_list[i].append("unknown origin country")

products_list = [[] for x in range(len(subjets_list))]

findmatches = re.compile(r"\b" +
                         r"\b|\b".join(re.escape(product) for product in products_set) +
                         r"\b")

for i in range(len(subjets_list)):
    products_list[i] = []
    
    for possible_match in set(findmatches.findall(subjets_list[i])):
        
        if possible_match in products_set:
            products_list[i].append(possible_match)
            
    if set(findmatches.findall(subjets_list[i])).isdisjoint(products_set): 
        products_list[i].append("unknown products")

dict_missing_data = {"HAZARD" : hazards_list, "ORIGIN COUNTRY" : countries_list, "PRODUCT" : products_list}

df_new_missing_data = pd.DataFrame.from_dict(dict_missing_data)

df_new_ready = pd.merge(df_new,
                        df_new_missing_data,
                        left_on = "RISK DECISION",
                        right_on = "HAZARDS",
                        how = "left")

df = pd.concat([df_old, df_new_ready])

df = df[df["RISK DECISION"] != "undecided"]
df.drop(["SUBJET"], inplace=True, axis=1)

df.to_csv("RASFF_data")