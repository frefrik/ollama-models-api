# 🦙 Ollama Models API

This API provides a simple interface to explore the complete collection of [Ollama](https://ollama.com/) models.

This project was mainly created due to the lack of filtering and sorting capabilities in Ollama's own [search engine](https://ollama.com/search). With this API, users can easily search for models based on various criteria and sort the results.

## Documentation

The documentation for the API is available at [ollamadb.dev/docs](https://ollamadb.dev/docs).

## Base URL
The base URL for the API is: `https://ollamadb.dev/api/v1`

## Endpoints

### GET /models

Retrieve a list of all available Ollama models.

#### Parameters

- `search`: (optional) Search for models by name or description.
- `model_identifier`: (optional) Filter models by identifier.
- `namespace`: (optional) Filter models by namespace.
- `capability`: (optional) Filter models by capability.
- `model_type`: (optional) Filter models by type.
- `sort_by`: (optional) Sort the results by a specific field. Valid fields: `pulls`, `last_updated`.
- `order`: (optional) Sort order. Valid values: `asc`, `desc`.
- `limit`: (optional) Number of results to return. Default is 20.
- `skip`: (optional) Number of results to skip. Default is 0.

Example request:

```bash
curl https://ollamadb.dev/api/models?limit=3
```

Example response:

```json
{
  "models": [
    {
      "model_identifier": "llama3",
      "namespace": null,
      "model_name": "llama3",
      "model_type": "official",
      "description": "Meta Llama 3: The most capable openly available LLM to date",
      "capability": null,
      "labels": [
        "8B",
        "70B"
      ],
      "pulls": 6300000,
      "tags": 68,
      "last_updated": "2024-05-25",
      "last_updated_str": "4 months ago",
      "url": "https://ollama.com/library/llama3"
    },
    {
      "model_identifier": "llama3.1",
      "namespace": null,
      "model_name": "llama3.1",
      "model_type": "official",
      "description": "Llama 3.1 is a new state-of-the-art model from Meta available in 8B, 70B and 405B parameter sizes.",
      "capability": "Tools",
      "labels": [
        "8B",
        "70B",
        "405B"
      ],
      "pulls": 5500000,
      "tags": 94,
      "last_updated": "2024-09-16",
      "last_updated_str": "9 days ago",
      "url": "https://ollama.com/library/llama3.1"
    },
    {
      "model_identifier": "gemma",
      "namespace": null,
      "model_name": "gemma",
      "model_type": "official",
      "description": "Gemma is a family of lightweight, state-of-the-art open models built by Google DeepMind. Updated to version 1.1",
      "capability": null,
      "labels": [
        "2B",
        "7B"
      ],
      "pulls": 4099999,
      "tags": 102,
      "last_updated": "2024-04-25",
      "last_updated_str": "5 months ago",
      "url": "https://ollama.com/library/gemma"
    }
  ],
  "total_count": 4370,
  "limit": 3,
  "skip": 0,
  "data_updated": "2024-09-25T09:30:04.823125Z"
}
```

## Disclaimer

This project is not affiliated with, endorsed by, or in any way officially connected to Ollama. It is an independent project created to enhance the usability of Ollama's model collection.