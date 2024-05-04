# Copyright (c) 2024 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import csv
import datetime as dt
import dateutil.tz  # timezones
import inspect
import io
from KFSconfig import KFSconfig
from KFSfstr   import KFSfstr
from KFSlog    import KFSlog
import logging
import os
import pandas


@KFSlog.timeit
def main(DEBUG: bool) -> None:
    filename_base: str                                      # filename without extension
    filename_DT: dt.datetime                                # filename as DT
    filename_extension: str                                 # filename extension (with dot)
    filenames: list[str]=[filename
                          for filename in os.listdir(".")
                          if os.path.isfile(filename)]      # filenames in directory current
    format_conversion_df: pandas.DataFrame                  # loaded configurations
    FORMAT_CONVERSION_HEADER: list[str]=["input datetime format",
                                         "input timezone offset",
                                         "output datetime format",
                                         "output timezone offset",]
    success: bool=True                                      # if false don't close console windows immediately after execution


    format_conversion_default: str=("# Fill your lines out according to the csv header below.\n"   # default config content
    "# Use the datetime expressions from \"https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior\".\n"
    f"{chr(9).join(FORMAT_CONVERSION_HEADER)}\n\n"                                                 # chr(9)="\t", but backslashes in fstring not allowed
    "# samsung camera\n"
    "%Y%m%d_%H%M%S\t\t%Y-%m-%d %H_%M_%S\t\n"
    "%Y%m%d_%H%M%S(%f)\t\t%Y-%m-%d %H_%M_%S\t\n\n"
    "# dropbox\n"
    "%Y-%m-%d %H.%M.%S\t\t%Y-%m-%d %H_%M_%S\t\n"
    "%Y-%m-%d %H.%M.%S(%f)\t\t%Y-%m-%d %H_%M_%S\t")
    

    class ContextManager():
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_value, exc_traceback):
                if success==False:
                    print("\n\nPress enter to close program.", flush=True)
                    input() # pause
                return
    with ContextManager() as context:   # upon exit, if unsuccessful: don't close console windows immediately after execution
        try:
            format_conversion_df=pandas.read_csv(io.StringIO(KFSconfig.load_config("./config/format conversion.csv", format_conversion_default)),
                                                 comment="#",               # ignore comments
                                                 on_bad_lines="skip",       # will do my own checking
                                                 quoting=csv.QUOTE_NONE,    # don't encapsulate data in quotes
                                                 sep="\t")                  # tab as data separator because it can't be used in filenames
        except FileNotFoundError:
            return
        logging.info(format_conversion_df)
        if format_conversion_df["input datetime format"].isnull().values.any():    # is any input datetime format NaN? # type:ignore
            logging.error(f"An input datetime format is NaN. This is most likely because one of your rows does not contain exactly {len(FORMAT_CONVERSION_HEADER)-1} tabs to make {len(FORMAT_CONVERSION_HEADER)} columns.")
            raise ValueError(f"Error in {main.__name__}{inspect.signature(main)}: An input datetime format is NaN. This is most likely because one of your rows does not contain exactly {len(FORMAT_CONVERSION_HEADER)-1} tabs to make {len(FORMAT_CONVERSION_HEADER)} columns.")
        if format_conversion_df["output datetime format"].isnull().values.any():   # is any output datetime format NaN? # type:ignore
            logging.error(f"An output datetime format is NaN. This is most likely because one of your rows does not contain exactly {len(FORMAT_CONVERSION_HEADER)-1} tabs to make {len(FORMAT_CONVERSION_HEADER)} columns.")
            raise ValueError(f"Error in {main.__name__}{inspect.signature(main)}: An output datetime format is NaN. This is most likely because one of your rows does not contain exactly {len(FORMAT_CONVERSION_HEADER)-1} tabs to make {len(FORMAT_CONVERSION_HEADER)} columns.")

        config_df_TZ_in =format_conversion_df[FORMAT_CONVERSION_HEADER[1]].isnull()
        config_df_TZ_out=format_conversion_df[FORMAT_CONVERSION_HEADER[3]].isnull()
        logging.debug(config_df_TZ_in)
        logging.debug(config_df_TZ_out)

        format_conversion_df=format_conversion_df.fillna("")  # replace NaN with "" so "nan" is not inserted as timezone information

        i: int=0
        while i<len(config_df_TZ_in) and i<len(config_df_TZ_out):
            if config_df_TZ_in.values[i]==False and config_df_TZ_out.values[i]==False:  # if timezones should be changed:
                format_conversion_df.iloc[i, 0]+="%z"                                   # change input format so it takes timezone information #type:ignore
                logging.debug(f"Changed row [{i}] {FORMAT_CONVERSION_HEADER[0]} to {format_conversion_df.iloc[i, 0]}.")
            i+=1

        
        for filename_old in filenames:                                      # go through all filenames and try to rename
            logging.info("--------------------------------------------------")
            logging.info(f"Filename old: \"{filename_old}\"")
            filename_base     =os.path.splitext(filename_old)[0]            # filename without extension
            filename_extension=os.path.splitext(filename_old)[1].lower()    # file extension, convert to lowercase
            logging.debug(f"filename base: \"{filename_base}\"")
            logging.debug(f"filename extension: \"{filename_extension}\"")
            
            for i, config_row in format_conversion_df.iterrows():                                                                                       # try to rename with every input format #type:ignore
                logging.debug(f"Converting \"{filename_base}{config_row.iloc[1]}\" to datetime with format \"{config_row.iloc[0]}\"...")
                try:
                    filename_DT=dt.datetime.strptime(f"{filename_base}{config_row.iloc[1]}", config_row.iloc[0]) 
                    # str -> DT
                except ValueError:                                                                                                                      # if input format does not work: try next one
                    logging.debug(f"\rConverting \"{filename_base}{config_row.iloc[1]}\" to datetime with format \"{config_row.iloc[0]}\" failed.")
                    continue
                logging.debug(f"\rConverted \"{filename_base}{config_row.iloc[1]}\" to datetime with format \"{config_row.iloc[0]}\".")
                if config_df_TZ_in[int(i)]==False and config_df_TZ_out[int(i)]==False:                                                                  # if timezones should be changed: #type:ignore
                    filename_DT=filename_DT.astimezone(dateutil.tz.tzoffset(None, int(config_row.iloc[3][0:3])*3600+int(config_row.iloc[3][4:6])*60))   # change timezone                                                                  
                    logging.debug(f"Changed datetime timezone offset to \"{KFSfstr.notation_tech(int(config_row.iloc[3][0:3])*3600+int(config_row.iloc[3][4:6])*60, 0, round_static=True)}s\".")
                filename_new=f"{filename_DT.strftime(config_row.iloc[2])}{filename_extension}"                                                          # DT -> str, re-add file extension
                logging.info(f"Filename new: \"{filename_new}\"")
                
                logging.info(f"Renaming \"{filename_old}\" to \"{filename_new}\"...")
                try:
                    os.rename(f"{filename_old}", f"{filename_new}") # rename
                except FileExistsError:                             # if file already exists
                    logging.error(f"Renaming \"{filename_old}\" to \"{filename_new}\" failed, because file already exists.")
                    success=False
                except PermissionError:                             # if file still in use:
                    logging.error(f"Renaming \"{filename_old}\" to \"{filename_new}\" failed with \"PermissionError\". File might still be in use.")
                    success=False
                except OSError:                                     # wenn Umbenennung verbotene Zeichen enthält: aufhören
                    logging.error(f"Renaming \"{filename_old}\" to \"{filename_new}\" failed with \"OSError\". Output format might contain characters forbidden for filenames. (\\/:*?\"<>|)")
                    success=False
                else:
                    logging.info(f"\rRenamed \"{filename_old}\" to \"{filename_new}\".")
                break                                               # in any case: filename next
    return