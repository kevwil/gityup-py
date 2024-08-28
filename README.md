# gityup-py

Given a folder that contains git projects:

```text
~/code
├── project1
├── project2
├── etc
```

loop through them and run `git smart-pull` [^1] and `git remote update origin --prune`.

## Reason

A great way to start learning programming languages is to develop small programs, especially solving problems for yourself.

I decided to write a tool to sync projects I work on and ones I have cloned down just for reference.

Keeping them up-to-date helps me not branch from an old commit ref as well as keeping reference projects current.

## Development

```bash
poe clean
poe check
poe format
poe build
```

## Other Languages

- Haskell: <https://github.com/kevwil/gityup-haskell>
- Lua: <https://github.com/kevwil/gityup-lua>
- Go: <https://github.com/kevwil/gityup-go>

## Footnotes

[^1]: git-smart Ruby gem <https://github.com/kevwil/git-smart> which is a fork from [here](https://github.com/geelen/git-smart) with some fixes.
