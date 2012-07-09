#!/usr/bin/env bash

SPECFILE=libgdu.spec
MULTILIB=true
MULTILIB_PACKAGES=('libgdu' 'libgdu-devel')
DO_NOT_INSTALL=('libgdu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
