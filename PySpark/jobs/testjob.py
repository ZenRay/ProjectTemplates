#coding:utf8
"""
Test Spark Context Job
"""
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions as F


from utils.context import JobContext

records = [
    Row(id=1, first_name='Dan', second_name='Germain', floor=1),
    Row(id=2, first_name='Dan', second_name='Sommerville', floor=1),
    Row(id=3, first_name='Alex', second_name='Ioannides', floor=2),
    Row(id=4, first_name='Ken', second_name='Lai', floor=2),
    Row(id=5, first_name='Stu', second_name='White', floor=3),
    Row(id=6, first_name='Mark', second_name='Sweeting', floor=3),
    Row(id=7, first_name='Phil', second_name='Bird', floor=4),
    Row(id=8, first_name='Kim', second_name='Suter', floor=4)
]


def createdf(spark, data):
    df = spark.creatDataFrame(data)
    df.coalesce(1).write.parquet("/tmp/test/employees", mode="overwrite")

    report = df.select(F.col('id'),
        F.concat_ws(' ',F.col('first_name'),F.col('second_name')).alias('name'),
            (F.col('floor') * F.lit(2)).alias('steps_to_desk'))
    
    report.coalesce(1).write.parquet("/tmp/test/employee_report", mode="overwrite")




if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .enableHiveSupport() \
        .appName("testApp") \
        .master("yarn") \
        .config("spark.executor.memory", "2G") \
        .getOrCreate()


    createdf(spark, records)
    # job.execute(createdf, spark, records)
