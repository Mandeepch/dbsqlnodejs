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