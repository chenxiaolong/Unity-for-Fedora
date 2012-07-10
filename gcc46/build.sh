#!/usr/bin/env bash

SPECFILE=gcc46.spec
MULTILIB=false
DO_NOT_INSTALL=('gcc46-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
