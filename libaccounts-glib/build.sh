#!/usr/bin/env bash

SPECFILE=libaccounts-glib.spec
MULTILIB=true
MULTILIB_PACKAGES=('libaccounts-glib' 'libaccounts-glib-devel')
DO_NOT_INSTALL=('libaccounts-glib-debuginfo' 'libaccounts-glib-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
