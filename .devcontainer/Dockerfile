FROM mcr.microsoft.com/vscode/devcontainers/rust:bullseye

# [Optional] Uncomment this section to install additional packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN rustup toolchain install nightly && rustup override set nightly \
    && apt-get update && apt-get -y install --no-install-recommends libfmt-dev librange-v3-dev python3-pip cmake ninja-build lsb-release wget software-properties-common gnupg \
    && pip3 install lit \
    && cd /tmp && wget https://apt.llvm.org/llvm.sh && chmod +x llvm.sh && ./llvm.sh 16 clang opt \
    && for i in clang opt llc FileCheck; do ln -s $(which $i-16) /usr/local/bin/$i; done
