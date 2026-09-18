# CampusCare AI Frontend

React + Vite frontend for the CampusCare AI student assistance platform.

## Run locally

```bash
npm install
npm run dev
```

## Production build

```bash
npm run build
```

## Backend integration

The frontend calls:

`POST /api/chat`

The backend base URL defaults to `http://localhost:8000` and can be overridden with:

```
VITE_API_URL=http://localhost:8000
```

The API request body is:

```json
{
  "question": "What should I do if I lose my student ID?"
}
```

The response is expected to include `answer` and optionally `sources`.
