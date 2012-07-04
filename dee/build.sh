#!/usr/bin/env bash

SPECFILE=dee.spec
MULTILIB=true
MULTILIB_PACKAGES=('dee' 'dee-devel')
DO_NOT_INSTALL=('dee-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
