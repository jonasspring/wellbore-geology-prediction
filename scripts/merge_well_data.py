from pathlib import Path
import os

import pandas as pd 

SOURCE_DIR = 'data/raw/train/'
TARGET_DIR = 'data/merged_raw/train/'

def merge_well_tables(source_dir: str, target_dir: str):
    """
    Merge all csv files with well data into one dataframe and save in target_dir. Seperated into vertical
    typewells and horizontal target wells
    """

    wells_list = list(Path(source_dir).glob('*_horizontal_well.csv'))

    hor_wells_list = []
    vert_wells_list = []
    

    for well in wells_list:
        well_name = well.stem.split('__horizontal_well')[0]

        df_hor = pd.read_csv(well)
        df_hor['well_id'] = well_name

        df_vert = pd.read_csv(well.parent / f"{well_name}__typewell.csv")
        df_vert['well_id'] = well_name

        hor_wells_list.append(df_hor)
        vert_wells_list.append(df_vert)

    # concatenate new data with merged table
    df_merged_hor = pd.concat(hor_wells_list, axis=0)
    df_merged_vert = pd.concat(vert_wells_list, axis=0)

    # Save new dataframes
    os.makedirs(target_dir, exist_ok=True)
    df_merged_hor.to_parquet(os.path.join(target_dir,'horizontal_wells.parquet'))
    df_merged_vert.to_parquet(os.path.join(target_dir,'vertical_wells.parquet'))


if __name__ == "__main__":
    merge_well_tables(SOURCE_DIR, TARGET_DIR)