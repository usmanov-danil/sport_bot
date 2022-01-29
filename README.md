# Sport bot

TODO: write description


## After git clone
After you cloned this repo, install pre-commit checks globally.
```bash
pip3 install pre-commit==2.13.0
```
Then `cd` into the cloned repository and run
```bash
pre-commit install
```

## Pre-commit checks

`pre-commit` will check your code for code standards after each commit.
Autoformatters run first and if they change anything, they will fail.
You'll need to check that they didn't do anything illegal and `git add` edited files again.

If next stages fail you'll need to fix errors manually.

## Bot commands
### For users
* `/start` – запуск бота, получение клавиатуры и ругистрация пользователя
* `/help` – вывести информацию о коммандах

### For admins
* `/all text` – отправить всем пользователем кроме админов сообщение **text**
