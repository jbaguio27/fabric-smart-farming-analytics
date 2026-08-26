# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "54fb63f8-6e3b-4ddc-9303-34774c9b22c3",
# META       "default_lakehouse_name": "SmartFarming_Lakehouse",
# META       "default_lakehouse_workspace_id": "92bc9c4b-1186-473f-8398-f198e8b16b45",
# META       "known_lakehouses": [
# META         {
# META           "id": "54fb63f8-6e3b-4ddc-9303-34774c9b22c3"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 🚀 Master Medallion Batch Orchestrator (Single-Session Free-Trial Execution)

# CELL ********************

# Configure Delta Lake OCC Concurrency & Isolation
spark.conf.set("spark.databricks.delta.properties.defaults.isolationLevel", "WriteSerializable")
spark.conf.set("spark.databricks.delta.write.concurrentAppendMode.enabled", "true")

%run Notebook_Load_Bronze_History

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook_Silver_ETL

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run Notebook_Gold_ETL

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print("\n✨ ALL 3 MEDALLION STAGES COMPLETED SUCCESSFULLY IN A SINGLE SPARK SESSION!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
