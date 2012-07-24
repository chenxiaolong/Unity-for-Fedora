#!/usr/bin/env bash

SPECFILE=evemu.spec
MULTILIB=true
MULTILIB_PACKAGES=('evemu' 'evemu-devel')
DO_NOT_INSTALL=('evemu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
