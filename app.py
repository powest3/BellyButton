#dependencies
import pandas as pd
import json as json
import csv



#get the sample names to use for the dropdown menu
def get_sample_names():
    samples_df = pd.read_csv("belly_button_biodiversity_samples.csv", encoding = "utf-8")
    sample_names_w_id = list(samples_df.columns.values)
    sample_names = sample_names_w_id[1:]
    return sample_names, samples_df

#get the OTU descriptions to use for the hover text
def get_OTU_desc():
    file_df = pd.read_csv("belly_button_biodiversity_otu_id.csv", encoding = "utf-8")
    otu_data = list(file_df['lowest_taxonomic_unit_found'])
    return otu_data

#get the metadata
def get_sample_metadata():
    file_df = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv", encoding = "utf-8")
    #only get the fields we need because other fields may not have values
    sub_file_df = file_df[["SAMPLEID","ETHNICITY","GENDER","AGE","WFREQ","BBTYPE","LOCATION"]]
    #set the nAn values to either NA or 0
    values = {'ETHNICITY': "NA", 'GENDER': "NA", 'AGE': 0, 'WFREQ': 0,'BBTYPE': "NA", "LOCATION": "NA"}
    new_file_df = sub_file_df.fillna(value=values)
    new_file_df.set_index("SAMPLEID", inplace=True)
    meta_data = new_file_df.to_dict(orient='index')
    return meta_data


#get the data for a particular sample; include the related OTU data
def get_sample_values(sample):
    samples_df = pd.read_csv("belly_button_biodiversity_samples.csv", encoding = "utf-8")
    otu_df = pd.read_csv("belly_button_biodiversity_otu_id.csv", encoding = "utf-8")
    sorted_sample_df = samples_df[['otu_id','BB_'+sample]]
    sorted_lists = sorted_sample_df.sort_values('BB_'+sample,ascending=False)
    sorted_lists.rename(columns={'BB_'+sample:'sample_values'}, inplace=True)

    #merge with OTU data to get the description
    merge_table = pd.merge(sorted_lists, otu_df, on="otu_id")
    merge_table.rename(columns={'lowest_taxonomic_unit_found':'otu_desc'}, inplace=True)

    sorted_dict = merge_table[0:3673].to_dict(orient='list')
    sorted_list = [sorted_dict]

    return sorted_list