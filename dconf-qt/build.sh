#!/usr/bin/env bash

SPECFILE=dconf-qt.spec
MULTILIB=true
MULTILIB_PACKAGES=('dconf-qt' 'dconf-qt-devel')
DO_NOT_INSTALL=('dconf-qt-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
