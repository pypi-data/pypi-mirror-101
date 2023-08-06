dart-hj3415
==========

dart-hj3415 gather dart data from https://opendart.fss.or.kr and analyse it.


Quick start
------------

1. Usage
   > from dart_hj3415 import dart
   > /# get dart dataframe
   > dart.get_df(<<sdate:str>>, <<edate:str>>, <<code:str>>, <<title:str>>, <<restrict:bool>>, <<echo:bool>>) -> df
   > /# save db by date
   > dart.save_db_by_date(<<edate:str>>, <<dbfullpath:str>>, <<echo:bool>>) -> len(df)
   > /# save db by corp
   > dart.save_db_by_corp(<<edate:str>>, <<dbfullpath:str>>, <<echo:bool>>) -> len(df)
