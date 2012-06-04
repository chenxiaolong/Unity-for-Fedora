#!/usr/bin/env bash

SPECFILE=gtk3.spec
MULTILIB=true
# gtk3-immodule-xim and gtk3-immodules are not multilib in Fedora for some
# reason (gtk2 versions are).
MULTILIB_PACKAGES=('gtk3' 'gtk3-devel')
DO_NOT_INSTALL=('gtk3-debuginfo' 'gtk3-devel-docs')
# Same Fedora maintainer as glib2; doesn't care about non-multilib devel
# packages.
MULTILIB_DO_NOT_INSTALL=('gtk3-devel')

source "$(dirname ${0})/../internal_builder.sh"
build ${1}
