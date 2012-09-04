#!/usr/bin/env bash

SPECFILE=signon.spec
NO_BASE_PACKAGE=true
MULTILIB=true
MULTILIB_PACKAGES=('libsignon-qt' 'libsignon-qt-devel'
                   'signond-libs' 'signond-libs-devel')
DO_NOT_INSTALL=('signon-debuginfo' 'libsignon-qt-docs' 'signond-docs'
                'signon-plugins-docs')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
