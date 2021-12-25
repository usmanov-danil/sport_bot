# Sport bot

TODO: write description

# TODO

- [ ] get data from google docs
- [ ] add fsm
- [ ] add posability to write messages from admin to all users except admins - /message всем привет!
- [ ] add posability to users get wheir weights - weights
- [ ] add posability to users plot their weigth and BMI - weights
- [ ] add posability to users add and change their peofile info (BMI, height and etc) - profile
- [ ] add docker
- [ ] add envs


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
