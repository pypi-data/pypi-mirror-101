# Fluffy Snips

CLI tools that I find useful

## Installation

```bash
pip install fluffysnips
```

## Commands

### mvscreenshot

Move your most recent screenshot to a destination

```bash
Usage: mvscreenshot [OPTIONS] DESTINATION

Arguments:
  DESTINATION  [required]

Options:
  -m      Print markdown to use image  [default: False]
  --help  Show this message and exit.
```

Example
```bash
$ mvscreenshot pictures/example_1
Screenshot from 18 hours ago
Move to: /home/user/current/directory/pictures/example_1.png
Confirm [Y/n]: y
```

### tablefix

Reformat your markdown tables so each column is aligned to the largest cell


#### Usage

```
Usage: tablefix [OPTIONS] TARGET

Arguments:
  TARGET  [required]

Options:
  -i, --inline     Change the file  [default: False]
  -r, --recursive  If targeting a directory, format all markdown files in the
                   directory  [default: False]

  --help           Show this message and exit.
```

#### Example

Before:

```markdown
### Diff

| Flag | Description |
| ---- | ----------- |
| -y   | Side by side |
| -r   | Recursive (directory) |
```

After:
```markdown
### Diff

| Flag | Description           |
| ---- | --------------------- |
| -y   | Side by side          |
| -r   | Recursive (directory) |
```
