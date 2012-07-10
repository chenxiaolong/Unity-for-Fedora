#!/usr/bin/env bash

SPECFILE=gcc46.spec
MULTILIB=true
MULTILIB_PACKAGES=('gcc46' 'gcc46-devel' 'gcc46-static')
DO_NOT_INSTALL=('gcc46-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
