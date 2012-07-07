#!/usr/bin/env bash

SPECFILE=gtk3-ubuntu.spec
MULTILIB=true
# gtk3-immodule-xim and gtk3-immodules are not multilib in Fedora for some
# reason (gtk2 versions are).
MULTILIB_PACKAGES=('gtk3-ubuntu' 'gtk3-ubuntu-devel')
DO_NOT_INSTALL=('gtk3-ubuntu-debuginfo' 'gtk3-ubuntu-devel-docs')
# Same Fedora maintainer as glib2; doesn't care about non-multilib devel
# packages.
MULTILIB_DO_NOT_INSTALL=('gtk3-ubuntu-devel')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
