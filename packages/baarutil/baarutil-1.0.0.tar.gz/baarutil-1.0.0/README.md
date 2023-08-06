**This Custom Library is specifically created for the developers/useres who use BAAR. Which is a product of Allied Media Inc. (www.alliedmedia.com)**

Author:
~~~~~~~
Souvik Roy	[sroy-2019]
Zhaoyu (Thomas) Xu	[xuzhaoyu]

Dependencies:
~~~~~~~~~~~~~
pandas==1.0.3 or above
numpy==1.18.4 or above


Additional Info:
~~~~~~~~~~~~~~~~
The string structure that follows is a streamline structure that the developers/users follow throughout an automation workflow designed in BAAR:
"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"


Available functions and the examples are listed below:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1.	read_convert(string), Output Data Type: list of dictionary
Attributes:
	i.	string:	Input String, Data Type = String
Input:	"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
Output:	[{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]

2.	write_convert(input_list), Output Data Type: string
Attributes:
	i.	input_list:	List that contains the Dictionaries of Data, Data Type = List
Input:	[{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
Output:	"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"

3.	string_to_df(string, rename_cols, drop_dupes), Output Data Type: pandas DataFrame
Attributes:
	i.	string:	Input String, Data Type = String
	ii.	rename_cols:	Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}
	iii.drop_dupes:	Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False
Input:	"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
Output:
	|	Column_1	|	Column_2
---------------------------------
  0	|	abc			|	def
  1	|	hello		|	world

4.	df_to_string(input_df, rename_cols, drop_dupes), Output Data Type: string
Attributes:
	i.	input_df:	Input DataFrame, Data Type = pandas DataFrame
	ii.	rename_cols:	Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}
	iii.drop_dupes:	Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False
Input:
	|	Column_1	|	Column_2
---------------------------------
  0	|	abc			|	def
  1	|	hello		|	world
Output:	"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"