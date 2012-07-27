#!/usr/bin/env bash

SPECFILE=grail.spec
MULTILIB=true
MULTILIB_PACKAGES=('grail' 'grail-devel')
DO_NOT_INSTALL=('grail-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
