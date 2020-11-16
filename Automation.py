#imports
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

sc = SparkContext()
sqlContext = SQLContext(sc)

spark = SparkSession \
    .builder \
    .config("spark.sql.broadcastTimeout", 36000) \
    .getOrCreate()

#get DBR_df's
DBR_ddf_group_1 = glueContext.create_dynamic_frame.from_catalog()
DBR_df_group_1 = orders_ddf.toDF()

DBR_ddf_group_2 = glueContext.create_dynamic_frame.from_catalog()
DBR_df_group_2 = orders_ddf.toDF()

DBR_ddf_group_3 = glueContext.create_dynamic_frame.from_catalog()
DBR_df_group_3 = orders_ddf.toDF()

#get DBFNEU_df
DBFNEU_ddf = glueContext.create_dynamic_frame.from_catalog()
DBFNEU_df = orders_ddf.toDF()

#set variables
result_rows = []

#define testcases
testcases_group_1 = [
#this list represents 1 testcase
[{"column from DBR df":"filter value",\
"colour":"green", "Age":"44"},\
{"column from DBFNEU df":"filter value", "amount":"320", \
"types":["type_1", "type_2", "type_3"]}], 
#this list represents another test case
[{"":""}, {"":""}] 
]

testcases_group_2 = [
    [{"":""}, {"":""}]
]

testcases_group_3 = [
    [{"":""}, {"":""}]
]

def test_testcases(DBR_df, DBFNEU_df, testcases):
    """filters DBR and DBFNEU dataframes by conditions 
    specified in testcases and then 
    compares number of rows for the filtered dfs"""
    for case in testcases:
        DBR_df2 = DBR_df
        DBFNEU_df2 = DBFNEU_df
        case_parameters = ""
        #filter DBR_df
        for column, value in case[0].items():
            if type(value) == list:
                DBR_df2 = DBR_df2[col(column).isin(value)]
            else:
                DBR_df2 = DBR_df2[col(column) == value]
        #filter DBFNEU_df
        for column, value in case[1].items():
            if type(value) == list:
                DBFNEU_df2 = DBFNEU_df2[col(column).isin(value)]
                case_parameters += f"{column}:{value} "
            else:
                DBFNEU_df2 = DBFNEU_df2[col(column) == value]
                value = str(value)
                case_parameters += f"{column}:{value} "

        #compare dbs and save result
        if DBR_df2.count() == DBFNEU_df2.count():
            result_rows.append([case_parameters, "Success"])
        else:
            result_rows.append([case_parameters,"Failure"])

#execute function
test_testcases(DBR_df_group_1, DBFNEU_df, testcases_group_1)

test_testcases(DBR_df_group_2, DBFNEU_df, testcases_group_2)

test_testcases(DBR_df_group_3, DBFNEU_df, testcases_group_3)

#save result df
df.repartition(1).write.mode("overwrite").format("csv")\
    .option("header", "true").save()
