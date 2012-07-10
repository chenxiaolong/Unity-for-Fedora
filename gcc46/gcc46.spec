# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This package will not contain subpackages (except for devel and static). It
# makes the spec file far too complicated for no good reason. (The official
# Fedora GCC spec file is 2641 lines without changelog!)

# This is only a temporary package until nux and Unity are fixed, so it should
# be easy to install and remove.

# Install to another prefix
%global _prefix /opt/gcc46-x86_%{__isa_bits}
%global _infodir %{_datadir}/info
%global _mandir %{_datadir}/man

Name:		gcc46
Version:	4.6.3
Release:	1%{?dist}
Summary:	GNU Compiler Collection (version 4.6.3)

Group:		Development/Languages
# License found from f16 spec file
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:		http://gcc.gnu.org
Source0:	ftp://ftp.gnu.org/gnu/gcc/gcc-4.6.3/gcc-4.6.3.tar.bz2
Source1:	filter_provides_opensuse.sh

# Do not provide any libraries. It'll cause a huge mess when the package is put
# in a repository.
%if %{defined fedora}
%filter_provides_in %{_libdir}/.*\.so\..*$
%filter_provides_in %{_libdir}/gcc/%{_target_platform}/%{version}/liblto_plugin\.so\..*$
%filter_setup
%endif

%if %{defined suse_version}
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%endif

BuildRequires:	binutils

%if %{defined suse_version}
BuildRequires:	gettext-tools

BuildRequires:	cloog-devel
BuildRequires:	mpc-devel
%endif

%if %{defined fedora}
BuildRequires:	gettext

BuildRequires:	cloog-ppl-devel
BuildRequires:	libmpc-devel
%endif

BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel
BuildRequires:	ppl-devel
BuildRequires:	zlib-devel

%description
This package contains the C and C++ compilers from the GNU Compiler Collection
version 4.6. This package is required for compiling nux and Unity.


%package devel
Summary:	Development files from the GNU Compiler Collection version 4.6
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files needed to create C and C++ programs.


%package static
Summary:	Static libraries from the GNU Compiler Collection version 4.6
Group:		Development/Libraries

Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains the static libraries needed to compile C and C++ programs
statically.


%prep
%setup -q -n gcc-%{version}

# Check md5sums of source code
if ! cat MD5SUMS | grep '^[0-9a-f]' | md5sum -c --status; then
  exit 1
fi


%build
# Remove '-gnu' from target triplet
%global _gnu %{nil}

# The build system tried to compile with %{_target_platform}-TOOL
CC=gcc

OPT_FLAGS="%{optflags}"
OPT_FLAGS="$(echo ${OPT_FLAGS} | sed -r 's/-m[0-9]+//g')"
%global optflags "${OPT_FLAGS}"
%configure                       \
  --with-bugurl='https://build.opensuse.org/project/show?project=GNOME%3AAyatana' \
  --enable-languages=c,c++       \
  --enable-lto                   \
  --enable-shared                \
  --enable-threads=posix         \
  --with-system-zlib             \
  --enable-__cxa_atexit          \
  --disable-libunwind-exceptions \
  --enable-gnu-unique-object     \
  --enable-linker-build-id       \
  --disable-libgcj               \
  --with-ppl                     \
  --with-cloog                   \
  --with-tune=generic            \
  --build=%{_target_platform}    \
  --target=%{_target_platform}   \
  --host=%{_target_platform}     \
  --disable-multilib
# GCC's multilib functionality will compile both 32 bit and 64 bit libraries on
# x86_64. We disable that and use RPM's multilib functionality. gcc46.x86_64
# and gcc46.i686 can be installed in parallel.
#
# This means that the '-m32' option will not work to compile 32 bit executables
# from 64 bit systems. Instead, just use gcc46.i686 to compile.

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Remove info pages and manual pages. They are mostly identical to the GCC 4.7.0
# ones and not many users are going to try to find them in the non-standard
# prefix.
rm -rv $RPM_BUILD_ROOT%{_infodir}/
rm -rv $RPM_BUILD_ROOT%{_mandir}/

# Remove other files not usually included by distros
rm -rv $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{version}/include-fixed/
rm -rf $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{version}/install-tools/
rm -rv $RPM_BUILD_ROOT%{_libexecdir}/gcc/%{_target_platform}/%{version}/install-tools/

%find_lang gcc
%find_lang cpplib
%find_lang libstdc++

cat gcc.lang cpplib.lang libstdc++.lang > gettext.lang


%files -f gettext.lang
%doc ChangeLog NEWS
%dir %{_prefix}/
%dir %{_bindir}/
%{_bindir}/c++
%{_bindir}/cpp
%{_bindir}/g++
%{_bindir}/gcc
%{_bindir}/gcov
%{_bindir}/%{_target_platform}-c++
%{_bindir}/%{_target_platform}-g++
%{_bindir}/%{_target_platform}-gcc
%{_bindir}/%{_target_platform}-gcc-%{version}
%dir %{_libdir}/
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%{_libdir}/gcc/%{_target_platform}/%{version}/*.o
%{_libdir}/libgcc_s.so.1
%{_libdir}/libgomp.so.1
%{_libdir}/libgomp.so.1.0.0
%{_libdir}/libgomp.spec
%{_libdir}/libmudflap.so.0
%{_libdir}/libmudflap.so.0.0.0
%{_libdir}/libmudflapth.so.0
%{_libdir}/libmudflapth.so.0.0.0
%{_libdir}/libquadmath.so.0
%{_libdir}/libquadmath.so.0.0.0
%{_libdir}/libssp.so.0
%{_libdir}/libssp.so.0.0.0
%{_libdir}/libstdc++.so.6
%{_libdir}/libstdc++.so.6.0.16
%{_libdir}/libstdc++.so.6.0.16-gdb.py*
%dir %{_libexecdir}/
%dir %{_libexecdir}/gcc/
%dir %{_libexecdir}/gcc/%{_target_platform}/
%dir %{_libexecdir}/gcc/%{_target_platform}/%{version}/
%{_libexecdir}/gcc/%{_target_platform}/%{version}/cc1
%{_libexecdir}/gcc/%{_target_platform}/%{version}/cc1plus
%{_libexecdir}/gcc/%{_target_platform}/%{version}/collect2
%{_libexecdir}/gcc/%{_target_platform}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{_target_platform}/%{version}/lto1
%{_libexecdir}/gcc/%{_target_platform}/%{version}/liblto_plugin.so.0
%{_libexecdir}/gcc/%{_target_platform}/%{version}/liblto_plugin.so.0.0.0
%dir %{_datadir}/
%dir %{_datadir}/gcc-%{version}/
%dir %{_datadir}/gcc-%{version}/python/
%dir %{_datadir}/gcc-%{version}/python/libstdcxx/
%dir %{_datadir}/gcc-%{version}/python/libstdcxx/v6/
%{_datadir}/gcc-%{version}/python/libstdcxx/__init__.py*
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/__init__.py*
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/printers.py*


%files devel
%doc ChangeLog NEWS
%dir %{_prefix}/
%dir %{_includedir}/
%dir %{_includedir}/c++/
%{_includedir}/c++/4.6.3/
%dir %{_libdir}/
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/plugin/
%{_libdir}/gcc/%{_target_platform}/%{version}/include/
%{_libdir}/gcc/%{_target_platform}/%{version}/plugin/include/
%{_libdir}/libgcc_s.so
%{_libdir}/libgomp.so
%{_libdir}/libmudflap.so
%{_libdir}/libmudflapth.so
%{_libdir}/libquadmath.so
%{_libdir}/libssp.so
%{_libdir}/libstdc++.so
%dir %{_libexecdir}/
%dir %{_libexecdir}/gcc/
%dir %{_libexecdir}/gcc/%{_target_platform}/
%dir %{_libexecdir}/gcc/%{_target_platform}/%{version}/
%{_libexecdir}/gcc/%{_target_platform}/%{version}/liblto_plugin.so


%files static
%doc ChangeLog NEWS
%dir %{_libdir}/
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%{_libdir}/gcc/%{_target_platform}/%{version}/*.a
%{_libdir}/libgomp.a
%{_libdir}/libiberty.a
%{_libdir}/libmudflap.a
%{_libdir}/libmudflapth.a
%{_libdir}/libquadmath.a
%{_libdir}/libssp.a
%{_libdir}/libssp_nonshared.a
%{_libdir}/libstdc++.a
%{_libdir}/libsupc++.a


%changelog
* Mon Jul 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.6.3-1
- Initial release
- Version 4.6.3
