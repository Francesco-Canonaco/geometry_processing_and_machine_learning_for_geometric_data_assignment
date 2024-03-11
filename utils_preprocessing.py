import pandas as pd


def get_level(x, level):
    match level:
        case 1:
            return x.split("|")[0]
        case 2:
            return x.split("|")[1]
        case 3:
            return x.split("|")[2]
        case 4:
            return x.split("|")[3]
        case 5:
            return x.split("|")[4]
        case 6: 
            return x.split("|")[5]
        case 7:
            return x.split("|")[6]
        case _:
            return "Error"



def preprocessing_otu_dataset(path_otu:str, level:int):
    dataset_taxa=pd.read_csv(path_otu)
    dataset_taxa=dataset_taxa.rename(columns={'Unnamed: 0':'Taxa'})
    #removing all the samples with 0 values (removing columns with all zeroes value)
    dataset_taxa=dataset_taxa.loc[:, (dataset_taxa != 0).any(axis=0)]
    dataset_taxa['Taxa']=dataset_taxa['Taxa'].apply(lambda x: get_level(x, level=level))
    dataset_taxa=dataset_taxa.groupby(by="Taxa").sum().reset_index()
    #transposing dataset
    dataset_taxa=dataset_taxa.set_index("Taxa").T
    dataset_taxa=dataset_taxa.rename_axis("", axis=1)
    dataset_taxa=dataset_taxa.reset_index()
    dataset_taxa=dataset_taxa.rename(columns={'index':'sample_id'})
    dataset_taxa.set_index("sample_id", inplace=True)
    #removing all the species with all zeroes vaue (keep in mind that the dataset is transposed)
    dataset_taxa=dataset_taxa.loc[:, (dataset_taxa != 0).any(axis=0)]
    dataset_taxa=dataset_taxa.fillna(0)
    return dataset_taxa

def preprocessing_metadata_dataset(path_metadata:str):
    dataset_metadata=pd.read_csv(path_metadata)
    dataset_metadata.set_index("sample_id",inplace=True)
    return dataset_metadata


def merge_dataset(path_otu:str, path_metadata:str, level:int):
    dataset_taxa=preprocessing_otu_dataset(path_otu, level)
    
    dataset_metadata=preprocessing_metadata_dataset(path_metadata)
    dataset_merged=pd.concat([dataset_metadata, dataset_taxa], ignore_index=False, axis=1)
    dataset_merged=dataset_merged.reset_index()
    
    return dataset_merged

