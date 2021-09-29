

# Step 1: Extracting equal chunks of data from large JSON data.

from glob import glob
import pandas as pd

data = pd.read_json('Clothing_Shoes_and_Jewelry.json',
                    chunksize=1000000, lines=True)

# for cols in data:
#     cols
#     break

# cols.columns

counter = 1

for chunk in data:
    new_df = pd.DataFrame(chunk[['overall', 'reviewText', 'summary']])
    new_df1 = new_df[new_df['overall'] == 5].sample(4000)
    new_df2 = new_df[new_df['overall'] == 4].sample(4000)
    new_df3 = new_df[new_df['overall'] == 3].sample(10000)
    new_df4 = new_df[new_df['overall'] == 2].sample(4000)
    new_df5 = new_df[new_df['overall'] == 1].sample(4000)

    new_df6 = pd.concat([new_df1, new_df2, new_df3, new_df4,
                         new_df5], axis=0, ignore_index=True)
    new_df6.to_csv(f"filtered_chunks/{counter}.csv", index=False)
    counter += 1


# Step 2 : Combining extracted chunks into a single file

filenames = [file for file in glob('filtered_chunks/*.csv')]

combined_csv = pd.concat([pd.read_csv(file) for file in filenames]).sort_values(
    ['overall'], ascending=False)

combined_csv.to_csv("balanced_reviews.csv", index=False)
