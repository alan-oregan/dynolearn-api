# Dynolearn API

Welcome to the Dynolearn API!

## API Reference

| Endpoint | Description |
|----------------|-------------------------------------------------------------------------------------------------|
| [/generateTasks](https://dynolearn-api.azurewebsites.net/generateTasks) | Generate a list of tasks for learning based on given name, age, reading_level and teaching_task |

## Development

1. Install/Open VS Code

2. Install Azure Functions VS Code Extension

3. Edit/Create local.settings.json to include HUGGINGFACEHUB_API_TOKEN and LANGCHAIN_API_KEY

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "HUGGINGFACEHUB_API_TOKEN": "secret key here",
    "LANGCHAIN_API_KEY": "secret key here",
    "LANGCHAIN_TRACING_V2": true,
    "LANGCHAIN_PROJECT": "DynoLearn Dev"
  }
}
```

4. To run locally press f5 or go to the debugging tab and launch the `Attach to Python Functions (dynolearn-api)` configuration.

5. Use the VS Code Thunder Client extension or equivalent software such as Postman to send requests.

## Deployment

The deployed API can be accessed at <https://dynolearn-api.azurewebsites.net>
