# +---------------------------------------------------------------------------
# : Funny Ascii specific recipes
# +---------------------------------------------------------------------------
# Display welcome message ;-)
about:
    #!/usr/bin/env bash
    cat .just/banners/about.txt

# Display debian logo
debian:
    #!/usr/bin/env bash
    cat .just/banners/debian.txt

[private]
@help:
    echo "🛟  Ascii Help 🛟"
    just --list --list-heading '' --list-prefix "    ↪ " --justfile {{justfile()}}

[private]
@setup:
    echo "🚧  Ascii Setup 🚧"
    #!/usr/bin/env sh