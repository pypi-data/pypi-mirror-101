# Multi-Git

Do you have a lot of git repositories, distributed over your whole system?
Would you like to manage them using a simple command, without the need to constantly
switch directories?

Use multi-git to manage these repos (I typically use the alias `mgit` for this
command, but mgit was unfortunately already taken on PyPi).

First use `multi-git add /path/to/git/repo -t tag1`
to add git repos. Then, use the standard git commands like `status`, `commit`, `pull` and
`push` to execute those commands over all managed git repos. To limit the set of
repos, you can use the `-t` (`--tags`) argument, that selects all repos that have
at least one of these tags set. For example,

```
multi-git pull
```

will pull the latest changes for all git repos that are managed by multi-git.
As another example,

```
multi-git status
```

or

```
multi-git st
```

will display all changes in all managed repos. As already mentioned, `-t` or `--tags`
will limit the set of repos:

```
multi-git st -t work
```
