#!/usr/bin/env bash

SPECFILE=libqtdee.spec
MULTILIB=true
MULTILIB_PACKAGES=('libqtdee' 'libqtdee-devel')
DO_NOT_INSTALL=('libqtdee-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
