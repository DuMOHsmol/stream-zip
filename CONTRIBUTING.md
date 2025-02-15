# How to contribute

In most cases to contribute you will need a [GitHub account](https://github.com/join).


## Contributing an issue

Suspected issues with stream-zip can be submitted at [the stream-unzip Issues page](https://github.com/uktrade/stream-zip/issues).

An issue that contains a [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example) stands the best chance of being resolved. However, it is understood that this is not possible in all circumstances.


## Contributing a feature request

A feature request can be submitted using the [Ideas category in the stream-zip discussions](https://github.com/uktrade/stream-zip/discussions/categories/ideas).


## Contributing documentation or code

To contribute changes to documentation or code, you will need the source of stream-unzip locally. The instructions for this depend on if you are a member of the [uktrade GitHub organisation](https://github.com/uktrade). In both cases, experience of working with source code, working on the command line, and working with git is helpful.


### If you're a member of uktrade

1. [Setup an SSH key and associate it with your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

2. Clone the repository

    ```bash
    git clone git@github.com:uktrade/stream-zip.git
    cd stream-zup
    ```

You should not fork the repository if you're a member of uktrade.

### If you're not a member of uktrade

1. [Setup an SSH key and associate it with your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

2. Clone the repository.

    ```bash
    git clone git@github.com:/stream-zip.git
    cd stream-zup
    ```

2. [Fork the repository](https://github.com/uktrade/stream-zip/fork). Make a note of the "Owner" that you fork to. This is usually your username.

    There is more documentation on forking in [GitHub's guide on contributing to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects).

3. Clone the forked repository. In the following, replace `my-username` with the owner that you forked to in step 2.

    ```bash
    git clone git@github.com:my-username/stream-zip.git
    cd stream-zup
    ```

## Contributing documentation

The source of the documentation is in the [docs/](https://github.com/uktrade/stream-zip/tree/main/docs) directory of the source code, and is written using [Material for mkdocs](https://squidfunk.github.io/mkdocs-material/).

Changes are then submitted via a Pull Request (PR). To do this:

1. Decide on a short hyphen-separated descriptive name for your change, prefixed with `docs/` for example `docs/add-django-recipe`.

2. Make a branch using this descriptive name.

    ```bash
    git checkout -b docs/add-django-recipe
    cd stream-zip
    ```

3. Make your changes in a text editor.

4. Preview your changes locally.

    ```bash
    pip install -r requirements-docs.txt  # Only needed once
    mkdocs serve
    ```

5. Commit your change and push to your fork. Ideally the commit message will follow the [Conventional Commit specification](https://www.conventionalcommits.org/).

    ```bash
    git add docs/recipies.md  # Repeat for each file changed
    git commit -m "docs: added a Django recipe"
    gir push origin docs/add-django-recipe
    ```

6. Raise a PR at [https://github.com/uktrade/stream-zip/pulls](https://github.com/uktrade/stream-zip/pulls) against the `main` branch in stream-zip.

7. Wait for the PR to be approved and merged, and respond to any questions or suggested changes.

When the PR is merged, the documentation is deployed automatically to [https://stream-zip.docs.trade.gov.uk/](https://stream-zip.docs.trade.gov.uk/).


## Contributing code

To contribute most code changes:

- Knowledge of Python is required. Python iterables, and specifically generators, are used heavily in stream-zip.

- Understanding the low-level properties of the ZIP file format is required. These are covered in detail in the specification of the ZIP file format, known as [APPNOTE](https://support.pkware.com/home/pkzip/developer-tools/appnote).

APPNOTE can be difficult to read, and contains a lot of information that isn't needed for stream-zip. A more concise introduction is in the [Wikipedia page on the ZIP file format](https://en.wikipedia.org/wiki/ZIP_(file_format)). However the Wikipedia page is less authoritative.

In both APPNOTE and the Wikipedia page, the most relevant parts are about the "local file header" and the "data descriptor". These are sections of metadata that go before and after the contents of each file respectively.

---

Changes are then submitted via a Pull Request (PR). To do this:

1. Decide on a short hyphen-separated descriptive name for your change, prefixed with the type of change. For example `fix/the-bug-description`.

2. Make a branch using this descriptive name.

    ```bash
    git checkout -b fix-a-bug-description
    ```

3. Make sure you can run existing tests locally

    ```bash
    ./install-libarachive.sh             # Only needed once
    pip install -r requirements-dev.txt  # Only needed once
    pytest
    ```

4. Make your changes in a text editor. In the cases of changing behaviour, this would usually include changing or adding at least one test in [test_stream_zip.py](https://github.com/uktrade/stream-zip/blob/main/test_stream_zip.py), and running them.

    ```bash
    pytest
    ```

5. Commit your changes and push to your fork. Ideally the commit message will follow the [Conventional Commit specification](https://www.conventionalcommits.org/).

    ```bash
    git add stream_zip.py  # Repeat for each file changed
    git commit -m "feat: the bug description"
    gir push origin fix/the-bug-description
    ```

6. Raise a PR at [https://github.com/uktrade/stream-zip/pulls](https://github.com/uktrade/stream-zip/pulls) against the `main` branch in stream-zip.

7. Wait for the PR to be approved and merged, and respond to any questions or suggested changes.
