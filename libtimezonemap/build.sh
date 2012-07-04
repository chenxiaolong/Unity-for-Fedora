#!/usr/bin/env bash

SPECFILE=libtimezonemap.spec
MULTILIB=true
MULTILIB_PACKAGES=('libtimezonemap' 'libtimezonemap-devel')
DO_NOT_INSTALL=('libtimezonemap-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
