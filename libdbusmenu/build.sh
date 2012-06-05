#!/usr/bin/env bash

SPECFILE=libdbusmenu.spec
NO_BASE_PACKAGE=true
MULTILIB=true
MULTILIB_PACKAGES=('libdbusmenu-glib' 'libdbusmenu-glib-devel'
                   'libdbusmenu-gtk2' 'libdbusmenu-gtk2-devel'
                   'libdbusmenu-gtk3' 'libdbusmenu-gtk3-devel'
                   'libdbusmenu-jsonloader' 'libdbusmenu-jsonloader-devel')
DO_NOT_INSTALL=('libdbusmenu-debuginfo')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
