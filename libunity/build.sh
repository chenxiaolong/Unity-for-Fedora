#!/usr/bin/env bash

SPECFILE=libunity.spec
MULTILIB=true
MULTILIB_PACKAGES=('libunity' 'libunity-devel')
DO_NOT_INSTALL=('libunity-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
