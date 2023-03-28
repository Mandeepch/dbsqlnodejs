# Databricks notebook source
# DBTITLE 1,Run Node js with DBSQL
#Below are the list of steps which can be done to test and run a sample SQL query using Node js and DBSQL

# COMMAND ----------

# DBTITLE 1,Install Homebrew
# If you don't have homebrew installed on Mac please follow https://docs.brew.sh/Installation for the installation
# Once the installation is done use the below commands
##  > brew upgrade or brew update
##  > export PATH="/usr/local/bin:$PATH"
##  > brew install node
##  > npm install -g grunt-cli


# COMMAND ----------

# DBTITLE 1,Install Databricks Dependencies
## > npm i @databricks/sql
## > npm i -D typescript
## > npm i -D @types/node

# COMMAND ----------

# DBTITLE 1,Create a sample.js file with below code
const { DBSQLClient } = require('@databricks/sql');

var token           = "<<Personal Access Token from Databricks>>";
var serverHostname = "dbc-a1b2345c-d6e7.cloud.databricks.com" #this is an example;
var httpPath      = "/sql/1.0/warehouses/9074fb582825985c" #this is an example;

if (!token || !serverHostname || !httpPath) {
  throw new Error("Cannot find Server Hostname, HTTP Path, or personal access token. " +
                  "Check the environment variables DATABRICKS_TOKEN, " +
                  "DATABRICKS_SERVER_HOSTNAME, and DATABRICKS_HTTP_PATH.");
}

const client = new DBSQLClient();

client.connect(
  options = {
    token: token,
    host:  serverHostname,
    path:  httpPath
  }).then(
    async client => {
      const session = await client.openSession();

      const queryOperation = await session.executeStatement(
        statement = 'SELECT * FROM default.diamonds LIMIT 2',
        options   = {
          runAsync: true,
          maxRows: 10000 // This option enables the direct results feature.
        }
      );

      const result = await queryOperation.fetchAll({
        progress: false,
        callback: () => {},
      });

      await queryOperation.close();

      console.table(result);

      await session.close();
      await client.close();
}).catch((error) => {
  console.log(error);
});


# COMMAND ----------

# DBTITLE 1,Run the code
#run the script with below code in your terminal
## > node sample.js

#you should get something as the below output

# COMMAND ----------

# MAGIC %md
# MAGIC ![my_test_image](files/mandeep/nodejs)
