#!/usr/bin/env bash

SPECFILE=geis.spec
MULTILIB=true
MULTILIB_PACKAGES=('geis' 'geis-devel')
DO_NOT_INSTALL=('geis-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
