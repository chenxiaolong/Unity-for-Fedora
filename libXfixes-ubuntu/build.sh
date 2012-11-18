#!/usr/bin/env bash

SPECFILE=libXfixes-ubuntu-Fedora_$(rpm -E '%fedora').spec
MULTILIB=true
MULTILIB_PACKAGES=('libXfixes-ubuntu' 'libXfixes-ubuntu-devel')
DO_NOT_INSTALL=('libXfixes-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
