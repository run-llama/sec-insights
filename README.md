# SEC Insights 🏦
<a href="https://www.producthunt.com/posts/sec-insights-ai?utm_source=badge-top-post-badge&utm_medium=badge&utm_souce=badge-sec&#0045;insights&#0045;ai" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=410213&theme=light&period=daily" alt="SEC&#0032;Insights&#0032;AI - Revolutionizing&#0032;SEC&#0032;document&#0032;analysis | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/run-llama/sec-insights)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SEC Insights uses the Retrieval Augmented Generation (RAG) capabilities of [LlamaIndex](https://github.com/jerryjliu/llama_index) to answer questions about SEC 10-K & 10-Q documents.

You can start using the application now at [secinsights.ai](https://www.secinsights.ai/)

You can also check out our [End-to-End tutorial guide on YouTube](https://youtu.be/2O52Tfj79T4?si=CYUcaBkc9P9g_m0P) for this project! This video covers product features, system architecture, development environment setup, and how to use this application with your own custom documents *(beyond just SEC filings!)*. The video has chapters so you can skip to the section most relevant to you.

## Why did we make this? 🤔
As RAG applications look to move increasingly from prototype to production, we thought our developer community would find value in having a complete example of a working real-world RAG application.

SEC Insights works as well locally as it does in the cloud. It also comes with many product features that will be immediately applicable to most RAG applications.

Use this repository as a reference when building out your own RAG application or fork it entirely to start your project off with a solid foundation.

## Product Features 😎
- Chat-based Document Q&A against a pool of documents
- Citation of source data that LLM response was based on
- PDF Viewer with highlighting of citations
- Use of API-based tools ([polygon.io](https://polygon.io/)) for answering quantitative questions
- Token-level streaming of LLM responses via [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- Streaming of Reasoning Steps (Sub-Questions) within Chat

## Development Features 🤓
- Infrastructure-as-code for deploying directly to [Vercel](https://vercel.com/) & [Render](https://render.com/)
- Continuous deployments provided by Vercel & Render.com. Shipping changes is as easy as merging into your `main` branch.
- Production & Preview environments for both Frontend & Backend deployments! Easily try your changes before release.
- Robust local environment setup making use of [LocalStack](https://localstack.cloud/) & [Docker](https://www.docker.com/) compose
- Monitoring & Profiling provided by [Sentry](https://sentry.io/welcome/)
- Load Testing provided by [Loader.io](https://loader.io/)
- Variety of python scripts for REPL-based chat & data management

## Tech Stack ⚒️
- Frontend
    - [React](https://react.dev/) / [Next.js](https://nextjs.org/)
    - [Tailwind CSS](https://tailwindcss.com/)
- Backend
    - [FastAPI](https://fastapi.tiangolo.com/)
    - [Docker](https://www.docker.com/)
    - [SQLAlchemy](https://www.sqlalchemy.org/)
    - [OpenAI](https://openai.com/) (gpt-3.5-turbo + text-embedding-ada-002)
    - [PGVector](https://github.com/pgvector/pgvector)
    - [LlamaIndex 🦙](https://www.llamaindex.ai/)
- Infrastructure
    - [Render.com](https://render.com/)
        - Backend hosting
        - [Postgres 15](https://www.postgresql.org/)
    - [Vercel](https://vercel.com/)
        - Frontend Hosting
    - [AWS](https://aws.amazon.com/)
        - [Cloudfront](https://aws.amazon.com/cloudfront/)
        - [S3](https://aws.amazon.com/s3/)

### System Architecture
[![System Architecture](https://www.plantuml.com/plantuml/png/jLJ1RjD04BtxAuPmo2bLsgGIaH0YYMqe0XhL4HoggjhOKsVRzMoqEsuR4F_EncxTDEjGX8GFbdRUcpTldZVfGeXNaX2KMEkI8PC6KvQQRF0ggv7FKJo_d9zUdfry-3WFWgR3wiAzUAtS6vabvJQmDv9MmeW2LYAz4Jd2pm3SCt6dtEYIigbMsi3hy70wZ4O0NKYGOT70a5OuQoW4fqlW9O8mHj_LG2scJORcGMXGFLKzriI9_85mE6pEFYjXDAXvlS8jFAuU3s_qsf1gyubMsGuuLZ8dI95S9VWLR6MIAbrc_psHez6R_cJKdi1pFvbWiH1sxqUAmsWIzlq9uU1usE__pOJQQ2t_R4-lUJWS7KTLTRwKwGsXjN3qN8nqji_gt0YoZeN4EtPzx0NB1bCMbAkzgKJZA8p2bjodW-Zu3way2NVEa5pVGQgB3WWBzV5XtdaiB8zd9zLW1rpKrQdH19_qeZusNswcBUS6xMP0VRqwu-y998FEezoiN2YPmYoCOL8wHNuGd1bvAnWXOMr4ZbDDZFVSS9xqedj6Gq91WkPMfcWRwIIQTYr4MIuCECSNyBQNwJlgxRXrixHQvveEf8POag1KEhbGiDXfQryzGMAptZH_qIHP6qdvfadX5UzjEbqXZKyUFRyumwTxcxX47l_KEj_GfAYQ8Bwwv0wkBSIEp4wq8dSXSNpd5KHsNLekaDX2QJULfSmofFhdOGE_7thdDUMYpR5NsQOtDwAnlWstteTsvaitfDLskUgzynstKXsnpOpNN36RhThXFLxz3Vsv7kMV51j_mNjdgYnKy1i0)](https://www.plantuml.com/plantuml/uml/jLJ1RjD04BtxAuPmo2bLsgGIaH0YYMqe0XhL4HoggjhOKsVRzMoqEsuR4F_EncxTDEjGX8GFbdRUcpTldZVfGeXNaX2KMEkI8PC6KvQQRF0ggv7FKJo_d9zUdfry-3WFWgR3wiAzUAtS6vabvJQmDv9MmeW2LYAz4Jd2pm3SCt6dtEYIigbMsi3hy70wZ4O0NKYGOT70a5OuQoW4fqlW9O8mHj_LG2scJORcGMXGFLKzriI9_85mE6pEFYjXDAXvlS8jFAuU3s_qsf1gyubMsGuuLZ8dI95S9VWLR6MIAbrc_psHez6R_cJKdi1pFvbWiH1sxqUAmsWIzlq9uU1usE__pOJQQ2t_R4-lUJWS7KTLTRwKwGsXjN3qN8nqji_gt0YoZeN4EtPzx0NB1bCMbAkzgKJZA8p2bjodW-Zu3way2NVEa5pVGQgB3WWBzV5XtdaiB8zd9zLW1rpKrQdH19_qeZusNswcBUS6xMP0VRqwu-y998FEezoiN2YPmYoCOL8wHNuGd1bvAnWXOMr4ZbDDZFVSS9xqedj6Gq91WkPMfcWRwIIQTYr4MIuCECSNyBQNwJlgxRXrixHQvveEf8POag1KEhbGiDXfQryzGMAptZH_qIHP6qdvfadX5UzjEbqXZKyUFRyumwTxcxX47l_KEj_GfAYQ8Bwwv0wkBSIEp4wq8dSXSNpd5KHsNLekaDX2QJULfSmofFhdOGE_7thdDUMYpR5NsQOtDwAnlWstteTsvaitfDLskUgzynstKXsnpOpNN36RhThXFLxz3Vsv7kMV51j_mNjdgYnKy1i0)

## Usage 💻
See `README.md` files in `frontend/` & `backend/` folders for individual setup instructions for each. As mentioned above, we also have a YouTube tutorial [here](https://youtu.be/2O52Tfj79T4?si=1Tm3zvuqna5ei4Cu&t=677) that covers how to setup this project's development environment.

We've also included a config for a [GitHub Codespace](https://github.com/features/codespaces) in [`.devcontainer/devcontainer.json`](https://github.com/run-llama/sec-insights/blob/main/.devcontainer/devcontainer.json). If you choose to use GitHub Codespaces, your codespace will come pre-configured with a lot of the libraries and system dependencies that are needed to run this project. This is probably the fastest way to get this project up and running! Having said that, developers have successfully set-up this project in Linux, macOS, and Windows environments!

If you have any questions when trying to run this project, you may find your answer quickly by reviewing our [FAQ](./FAQ.md) or by searching through our [GitHub issues](https://github.com/run-llama/sec-insights/issues)! If you don't see a satisfactory answer to your question, feel free to [open a GitHub issue](https://github.com/run-llama/sec-insights/issues/new) so we may assist you!

We also have a dedicated [#sec-insights channel on our Discord](https://discord.com/channels/1059199217496772688/1150942525968879636) where we may be able to assist with smaller issues more instantaneously.

## Caveats 🧐
- The frontend currently doesn't support Mobile
- Our main goal with this project is to provide a solid foundation for full-stack RAG apps. There is still room for improvement in terms of RAG performance!

## Contributing 💡
We remain very open to contributions! We're looking forward to seeing the ideas and improvements the LlamaIndex community is able to provide.

Huge shoutout to [**@Evanc123**](https://github.com/Evanc123) for his fantastic work building the frontend for this project!
