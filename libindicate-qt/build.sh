#!/usr/bin/env bash

SPECFILE=libindicate-qt.spec
MULTILIB=true
MULTILIB_PACKAGES=('libindicate-qt' 'libindicate-qt-devel')
DO_NOT_INSTALL=('libindicate-qt-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
