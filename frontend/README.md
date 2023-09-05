# SEC Insights Frontend

This is SEC Insights, a tool that let's you analyze multiple financial documents, powered by LlamaIndex. [Live URL](https://secinsights.ai/)

## Technical Details

Built with `next.js`, `tailwindcss`, and `typescript react`, based on the [T3 starter kit](https://create.t3.gg/en/usage/next-js).

## Architecture

This app consists of two main routes,

1. `/`, located in `src/pages/index.tsx`. This route is the landing page, and consists of the document selector and a marketing section.
2. `/conversation/{conversation_id}`, located in `src/pages/conversation/[id].tsx` This page consists of the chat window on the left hand side, and the pdf viewer on the right hand side.

- PDFs are rendered using `react-pdf`; a single pdf is rendered by the `VirtualizedPdf.tsx` component
- The Chat component is located in `RenderConversations.tsx`

## How to develop locally

1. `npm i`
2. `npm run dev`

3. And before pushing to the repo, `npm run build` to catch any typescript errors (TODO: pre-commit hook)

Follow our deployment guides for [Vercel](https://create.t3.gg/en/deployment/vercel), [Netlify](https://create.t3.gg/en/deployment/netlify) and [Docker](https://create.t3.gg/en/deployment/docker) for more information.
