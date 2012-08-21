# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This package will not contain subpackages (except for devel and static). It
# makes the spec file far too complicated for no good reason. (The official
# Fedora GCC spec file is 2641 lines without changelog!)

# This is only a temporary package until nux and Unity are fixed, so it should
# be easy to install and remove.

Name:		gcc46
Version:	4.6.3
Release:	3%{?dist}
Summary:	GNU Compiler Collection (version 4.6.3)

%if %{defined suse_version}
Group:		Development/Languages/C and C++
%else
Group:		Development/Languages
%endif
# License found from f16 spec file
%if %{defined suse_version}
License:	GPL-3.0+ and GPL-3.0-with-GCC-exception and GPL-2.0-with-GCC-exception
%else
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
%endif
URL:		http://gcc.gnu.org
#Source0:	ftp://ftp.gnu.org/gnu/gcc/gcc-4.6.3/gcc-4.6.3.tar.bz2
# Just use the parts we need (saves download time)
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-4.6.3/gcc-core-4.6.3.tar.bz2
Source1:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-4.6.3/gcc-g++-4.6.3.tar.bz2
Source98:	filter_provides_opensuse.sh
Source99:	filter_requires_opensuse.sh

# Do not provide any libraries. It'll cause a huge mess when the package is put
# in a repository.
%if %{defined fedora}
%filter_provides_in .*\.so\..*$
#filter_requires_in .*\.so\..*$
%filter_from_requires /\.so/d
%filter_setup
%endif

%if %{defined suse_version}
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE98}
%define __find_requires %{SOURCE99}
%endif

BuildRequires:	binutils

%if %{defined suse_version}
BuildRequires:	fdupes
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
%if %{defined suse_version}
Group:		Development/Libraries/C and C++
%else
Group:		Development/Libraries
%endif

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files needed to create C and C++ programs.


%package static
Summary:	Static libraries from the GNU Compiler Collection version 4.6
%if %{defined suse_version}
Group:		Development/Libraries/C and C++
%else
Group:		Development/Libraries
%endif

Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains the static libraries needed to compile C and C++ programs
statically.


%prep
# Make filter scripts executable for openSUSE (needed when building on OBS)
%if %{defined suse_version}
chmod +x %{SOURCE98}
chmod +x %{SOURCE99}
%endif

%setup -q -c
%setup -q -D -T -a 1

pushd gcc-4.6.3
# Do not run fixincludes (from AUR package gcc46)
sed -i 's@\./fixinc\.sh@-c true@' gcc/Makefile.in

echo '4.6.3' > gcc/BASE-VER
echo 'GNOME:Ayatana %{version}-%{release}' > gcc/DEV-PHASE
popd

# OBS fails with: Couldn't exec ...: Permission denied for the filtering
# scripts, so allow them to be executed.
chmod +x '%{SOURCE98}' '%{SOURCE99}'


%build
# Remove '-gnu' from target triplet
%global _gnu %{nil}

mkdir build
cd build

%global _configure ../gcc-%{version}/configure

# From Fedora spec
OPT_FLAGS="%{optflags}"
OPT_FLAGS="$(echo ${OPT_FLAGS} | sed -r \
  -e 's/-m[0-9]+//g' \
%ifarch %{ix86}
  -e 's/-march=i.86//g' \
%endif
  -e 's/(-Wp,)?-D_FORTIFY_SOURCE=[12]//g' \
  -e 's/-pipe//g' \
)"
%global optflags "${OPT_FLAGS}"

%configure					\
  --with-bugurl='https://build.opensuse.org/project/show?project=GNOME%3AAyatana' \
  --enable-languages=c,c++			\
  --enable-checking=release			\
  --enable-lto					\
  --enable-plugin				\
  --enable-gold					\
  --with-plugin-ld=ld.gold			\
  --enable-ld=default				\
  --enable-shared				\
  --enable-threads=posix			\
  --with-system-zlib				\
  --enable-__cxa_atexit				\
  --enable-clocale=gnu				\
  --disable-libunwind-exceptions		\
  --enable-gnu-unique-object			\
  --enable-linker-build-id			\
  --enable-version-specific-runtime-libs	\
  --with-ppl					\
  --with-cloog					\
  --with-tune=generic				\
  --build=%{_target_platform}			\
  --target=%{_target_platform}			\
  --host=%{_target_platform}			\
  --program-suffix=-4.6				\
  --disable-libstdcxx-pch			\
  --disable-multilib
# GCC's multilib functionality will be disabled. This is a temporary package for
# compiling nux and Unity, both of which do not require 32 bit support on 64 bit
# machines.

make %{?_smp_mflags}


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libiberty
rm $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Put libgcc_s.so* in correct directory on x86_64 (or gcc will fail with:
#   /usr/bin/ld: cannot find -lgcc_s
#   collect2: ld returned 1 exist status
%ifarch x86_64
mv $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{_lib}/libgcc_s.so* \
   $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{version}/
rmdir $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{_lib}/
%endif

# Remove 'install-tools' directories, which usually isn't packaged
# On 32 bit openSUSE, both libdir and libexecdir are /usr/lib
rm -rv \
%if "%{_libexecdir}" == "%{_libdir}"
  $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{version}/install-tools/ \
%else
  $RPM_BUILD_ROOT%{_libdir}/gcc/%{_target_platform}/%{version}/install-tools/ \
  $RPM_BUILD_ROOT%{_libexecdir}/gcc/%{_target_platform}/%{version}/install-tools
%endif

# Remove info pages, manual pages, and locales. They are mostly identical to the
# GCC 4.7.0 ones and this GCC package isn't meant for users anyway :D
rm -rv $RPM_BUILD_ROOT%{_infodir}/
rm -rv $RPM_BUILD_ROOT%{_mandir}/
rm -rv $RPM_BUILD_ROOT%{_datadir}/locale/

# symlink duplicate files in openSUSE
%if %{defined suse_version}
%fdupes -s $RPM_BUILD_ROOT
%endif


%files
%if %{defined suse_version}
%defattr(-,root,root)
%endif
%doc gcc-%{version}/ChangeLog gcc-%{version}/NEWS
%{_bindir}/c++-4.6
%{_bindir}/cpp-4.6
%{_bindir}/g++-4.6
%{_bindir}/gcc-4.6
%{_bindir}/gcov-4.6
%{_bindir}/%{_target_platform}-c++-4.6
%{_bindir}/%{_target_platform}-g++-4.6
%{_bindir}/%{_target_platform}-gcc-4.6
%{_bindir}/%{_target_platform}-gcc-%{version}
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%{_libdir}/gcc/%{_target_platform}/%{version}/*.o
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc_s.so.1
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.so.1
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.so.1.0.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.spec
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflap.so.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflap.so.0.0.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflapth.so.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflapth.so.0.0.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libquadmath.so.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libquadmath.so.0.0.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libssp.so.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libssp.so.0.0.0
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.so.6
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.so.6.0.16
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.so.6.0.16-gdb.py*
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
%dir %{_datadir}/gcc-%{version}/
%dir %{_datadir}/gcc-%{version}/python/
%dir %{_datadir}/gcc-%{version}/python/libstdcxx/
%dir %{_datadir}/gcc-%{version}/python/libstdcxx/v6/
%{_datadir}/gcc-%{version}/python/libstdcxx/__init__.py*
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/__init__.py*
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/printers.py*


%files devel
%if %{defined suse_version}
%defattr(-,root,root)
%endif
%doc gcc-%{version}/ChangeLog gcc-%{version}/NEWS
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/plugin/
%{_libdir}/gcc/%{_target_platform}/%{version}/include/
%{_libdir}/gcc/%{_target_platform}/%{version}/include-fixed/
%{_libdir}/gcc/%{_target_platform}/%{version}/plugin/include/
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc_s.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflap.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflapth.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libquadmath.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libssp.so
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.so
%dir %{_libexecdir}/gcc/
%dir %{_libexecdir}/gcc/%{_target_platform}/
%dir %{_libexecdir}/gcc/%{_target_platform}/%{version}/
%{_libexecdir}/gcc/%{_target_platform}/%{version}/liblto_plugin.so


%files static
%if %{defined suse_version}
%defattr(-,root,root)
%endif
%doc gcc-%{version}/ChangeLog gcc-%{version}/NEWS
%dir %{_libdir}/gcc/
%dir %{_libdir}/gcc/%{_target_platform}/
%dir %{_libdir}/gcc/%{_target_platform}/%{version}/
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcov.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflap.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libmudflapth.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libquadmath.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libssp.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libssp_nonshared.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libsupc++.a


%changelog
* Mon Aug 20 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.6.3-3
- Now builds in openSUSE

* Tue Jul 10 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.6.3-2
- Install in /usr prefix

* Mon Jul 09 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 4.6.3-1
- Initial release
- Version 4.6.3
