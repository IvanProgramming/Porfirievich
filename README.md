# Profirievich Bot
[![Add to your server](https://img.shields.io/badge/Discord-invite-yellow)](https://discord.com/api/oauth2/authorize?client_id=782372065998667829&permissions=0&scope=bot)
## About

* This bot can generate continuation of some sentece with use of reversed [Profirievich](https://porfirevich.ru/)
* Project status: __working__

## Table of contents

> * [Title / Repository Name](#title--repository-name)
>   * [About / Synopsis](#about--synopsis)
>   * [Table of contents](#table-of-contents)
>   * [Installation](#installation)
>   * [Usage](#usage)
>   * [Features](#features)
>   * [Contributing](#contributing)
>   * [License](#license)

## Docker Setup (recommended)

1. Get Bot token from [Discord developer portal](https://discord.com/developers)
2. [Install](https://docs.docker.com/engine/install/) Docker Engine
3. Run bot container
  ```bash
  docker run -e DISCORD_TOKEN=<DISCORD_TOKEN_HERE> --name porfirievich-container ivanisplaying/porfirievich
  ```
  * *Replace `<DISCORD_TOKEN_HERE>` to your Discord token*
  * *Add `-d` for running bot in background*

## Manual setup
1. Clone git repo
```bash
git clone https://github.com/IvanProgramming/Porfirievich
```
2. Get Bot token from [Discord developer portal](https://discord.com/developers)
3. Add discord token to enviroment variables
```bash
export DISCORD_TOKEN=<DISCORD_TOKEN_HERE>
```
* *Replace `<DISCORD_TOKEN_HERE>` to your Discord token*
4. *Optional*. Create new virtual enviroment
```bash
virtualenv venv
```
5. *Optional*. Activate virtual enviroment
```bash
source venv\bin\activate
```
6. Install all requirements
```bash
pip install -r requirements.txt
```
7. Run bot
```bash
python main.py
```
## Usage

* `+gen` command can be used for generating continious of sentence
* `+gen<WORDS_COUNT>`, where `<WORDS_COUNT>` will generate continious less or equal to this count of words

### Features

* Reaction reload
* Reaction words addition
* Picture generate for good continious

## Contributing

Just fork this bot and, after adding new features make Pull Request

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
