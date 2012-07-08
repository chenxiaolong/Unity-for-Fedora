#!/usr/bin/env bash

SPECFILE=libunity-misc.spec
MULTILIB=true
MULTILIB_PACKAGES=('libunity-misc' 'libunity-misc-devel')
DO_NOT_INSTALL=('libunity-misc-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
