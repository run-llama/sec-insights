# SEC Insights
SEC Insights uses the Retrieval Augment Generation (RAG) capabilities of LlamaIndex to answer questions about SEC 10-K & 10-Q documents.

You can start using the application now at [secinsights.ai](https://www.secinsights.ai/)

## Why did we make this?
As RAG applications look to move increasingly from prototype to production, we thought our developer community would find it valuable to have a complete example of a working real world RAG application. SEC Insights works as well locally as it does in the cloud. It also comes with many product features that will be immediately applicable to most RAG applications.

## Product Features
- Chat-based Document Q&A against a pool of documents
- Citation of source data that LLM response was based on
- PDF Viewer with highlighting of citations
- Token-level streaming of LLM responses via [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- Streaming of Reasoning Steps (Sub-Questions) within Chat

## Dev Features
- Infrastructure-as-code for deploying directly to [Vercel](https://vercel.com/) & [Render](https://render.com/)
- Robust local environment setup making use of [LocalStack](https://localstack.cloud/) & [Docker](https://www.docker.com/) compose
- Monitoring & Profiling provided by [Sentry](https://sentry.io/welcome/)
- Load Testing provided by [Loader.io](https://loader.io/)
- Variety of python scripts for REPL-based interaction & managing data

## Tech Stack
- Frontend
    - React/Next.js
    - Tailwind CSS
- Backend
    - FastAPI
    - Docker
    - SQLAlchemy
    - OpenAI
    - PGVector
    - LlamaIndex 🦙
- Infrastructure
    - Render.com
        - Backend hosting
        - Postgres 15
    - Vercel
        - Frontend Hosting
    - AWS
        - Cloudfront
        - S3

## Usage
See `README.md` files in `frontend/` & `backend/` folders for individual setup instructions for each.

## 💡 Contributing
We remain very open to contributions! We're looking forward to seeing the ideas and improvements the LlamaIndex community is able to provide.
