#!/usr/bin/env bash

SPECFILE=libqtbamf.spec
MULTILIB=true
MULTILIB_PACKAGES=('bamf-qt' 'bamf-qt-devel')
DO_NOT_INSTALL=('bamf-qt-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
