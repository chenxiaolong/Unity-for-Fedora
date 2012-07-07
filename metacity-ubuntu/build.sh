#!/usr/bin/env bash

SPECFILE=metacity-ubuntu.spec
MULTILIB=true
MULTILIB_PACKAGES=('metacity-ubuntu' 'metacity-ubuntu-devel')
DO_NOT_INSTALL=('metacity-ubuntu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
