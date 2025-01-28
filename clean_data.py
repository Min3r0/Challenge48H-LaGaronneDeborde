import pandas as pd

file_path = './catastrophes_naturelles_data.csv'
cleaned_data = './catastrophes_naturelles_data_cleaned.csv'


def clean_csv(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.replace('"', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('innondation', 'inondation')
            line = line.replace(',temperature', 'id,temperature')
            line = line.replace('catastrophe', 'catastrophe,catastrophe2')
            outfile.write(line)


clean_csv(file_path, cleaned_data)

data = pd.read_csv(cleaned_data)

data["seisme"] = data["catastrophe"].eq("seisme") | data["catastrophe2"].eq("seisme")
data["inondation"] = data["catastrophe"].eq("inondation") | data["catastrophe2"].eq("inondation")

data = data.drop(columns=["catastrophe", "catastrophe2"])

data.to_csv("clean_formated_data.csv", index=False)
