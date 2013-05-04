#!/usr/bin/env bash

SPECFILE=libcolumbus.spec
MULTILIB=true
MULTILIB_PACKAGES=('libcolumbus' 'libcolumbus-devel')
DO_NOT_INSTALL=('libcolumbus-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
