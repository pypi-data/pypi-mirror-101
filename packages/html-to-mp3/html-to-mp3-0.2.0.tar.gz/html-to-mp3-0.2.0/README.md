# `html2mp3`

> Generate `mp3`s from html text.

A tiny cli I made on a fling.

## CLI

Basic use:

```bash
# CLI docs
html2mp3

# Generate from a file
html2mp3 file examples/test1.html test1.mp3

# Download from URL
html2mp3 url https://text.npr.org/985359064

# Download from URL, only generate voice from the text in the selector .paragraphs-container
html2mp3 url https://text.npr.org/985359064 --select ".paragraphs-container"
```

Multiple files at once can be done (though the CLI could be improved to make this less verbose):


```bash
html2mp3 url https://text.npr.org/985359064 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985347984 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985524494 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985032748 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985498425 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985336036 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/976385244 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985470204 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985365621 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985296354 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985594759 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985125653 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985290016 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985400141 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984387402 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984614649 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985143101 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/982223967 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985421813 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984870694 --select ".paragraphs-container"
```

Running the above example (20 examples in total) took about 48s on my personal computer (`47.72s user 0.74s system 480% cpu 10.094 total`)

You can do your own tests via:

```bash
time sh -c 'html2mp3 url https://text.npr.org/985359064 & html2mp3 url https://text.npr.org/985347984'
```

## TODO

- [ ] Testing
- [ ] Multiple files/urls at once
- [ ] Voice generation settings
