#!/usr/bin/env bash

SPECFILE=libqtgconf.spec
MULTILIB=true
MULTILIB_PACKAGES=('libqtgconf' 'libqtgconf-devel')
DO_NOT_INSTALL=('libqtgconf-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
