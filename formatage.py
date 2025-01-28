import pandas as pd

file_path = 'catastrophes_naturelles_data.csv'
data = pd.read_csv(file_path)


data["catastrophe"] = data["catastrophe"].str.replace("'", "").str.strip()
data["catastrophe2"] = data["catastrophe2"].str.replace("'", "").str.strip()
data["catastrophe"] = data["catastrophe"].str.replace("innondation", "inondation").str.strip()
data["catastrophe2"] = data["catastrophe2"].str.replace("innondation", "inondation").str.strip()


data["seisme"] = data["catastrophe"].eq("seisme") | data["catastrophe2"].eq("seisme")
data["inondation"] = data["catastrophe"].eq("inondation") | data["catastrophe2"].eq("inondation")


data.to_csv("fichier_modifie.csv", index=False)