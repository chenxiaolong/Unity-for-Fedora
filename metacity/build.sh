#!/usr/bin/env bash

SPECFILE=metacity.spec
MULTILIB=true
MULTILIB_PACKAGES=('metacity' 'metacity-devel')
DO_NOT_INSTALL=('metacity-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
