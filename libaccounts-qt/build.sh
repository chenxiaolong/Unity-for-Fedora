#!/usr/bin/env bash

SPECFILE=libaccounts-qt.spec
MULTILIB=true
MULTILIB_PACKAGES=('libaccounts-qt' 'libaccounts-qt-devel')
DO_NOT_INSTALL=('libaccounts-qt-debuginfo' 'libaccounts-qt-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
