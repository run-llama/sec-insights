# SEC Insights Dev Container

This dev container configuration sets up a development environment that is specifically configured for this project.

This is useful in getting the project setup faster by having many of the system dependencies already pre-installed.

## How do I use this?

You can either click this button to open the dev container on a Github Codespace:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/run-llama/sec-insights)

Or you can spin up the dev container locally using [VS Code's dev container feature](https://code.visualstudio.com/docs/devcontainers/create-dev-container#_create-a-devcontainerjson-file).

## What are the benefits of using this?
* System level dependencies are pre-installed
  * Project-specific python version
  * Other dependencies like `wkhtmltopdf` & `s3fs` are pre-installed
  * Uses the same base Docker image as what's used for the production service
    * So higher fidelity between your dev environment and prod environment.

## Are there any downsides to using this?
One downside is that when you're using the dev container via Github Codespaces, that service isn't entirely free. There's a free tier limit after which Github Codespace usage is paid.
Also, if you're running the dev container locally via the VS Code dev container feature, you may find that Docker can take up quite a bit of storage space on your machine. Make sure you have the necessary storage space.

