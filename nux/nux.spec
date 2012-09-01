# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _major_ver 3

Name:		nux
Version:	3.4.0
Release:	1%{?dist}
# Summary from Ubuntu
Summary:	Visual rendering toolkit for real-time applications

Group:		System Environment/Libraries
License:	GPLv3 and LGPLv3
URL:		https://launchpad.net/nux
Source0:	https://launchpad.net/nux/%{_major_ver}.0/3.4/+download/nux-%{version}.tar.gz
Source1:	50_check_unity_support

BuildRequires:	xorg-x11-xinit

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	graphviz

BuildRequires:	boost-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(compositeproto) 
BuildRequires:	pkgconfig(damageproto)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(ibus-1.0)
BuildRequires:	pkgconfig(libgeis)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xxf86vm)

Requires:	%{name}-common = %{version}-%{release}
Requires:	xorg-x11-xinit

# Description from Ubuntu
%description
Nux is a graphical user interface toolkit for applications that mixes OpenGL
hardware acceleration with high quality visual rendering.

%package devel
Summary:	Development files for the Nux library
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	boost-devel
Requires:	pkgconfig(cairo)
Requires:	pkgconfig(gdk-pixbuf-2.0)
Requires:	pkgconfig(glew)
Requires:	pkgconfig(glib-2.0)
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(sigc++-2.0)
Requires:	pkgconfig(xxf86vm)
Requires:	pkgconfig(gl)
Requires:	pkgconfig(pango)
Requires:	pkgconfig(libpcre)

%description devel
This package contains the development files for the Nux library.

%package common
Summary:	Common files for the Nux library
Group:		System Environment/Libraries

BuildArch:	noarch

Requires:	%{name} = %{version}-%{release}

%description common
This package contains the architecture-independent files for the Nux library.

%package tools
Summary:	Visual rendering toolkit for real-time applications - Tools
Group:		Development/Tools

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains various tools for the Nux library.

%prep
%setup -q

# Avoid rpmlint spurious-executable-perm error in debuginfo package
find -type f \( -name '*.h' -o -name '*.cpp' \) -exec chmod 644 {} \;


%build
%configure

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# Ubuntu doesn't package the gputests
rm -rv $RPM_BUILD_ROOT%{_datadir}/nux/gputests/

# Avoid rpmlint zero-length error. Remove empty files.
find $RPM_BUILD_ROOT -type f -empty -delete

# Install X startup session file
install -dm755 $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%{_libdir}/libnux-%{_major_ver}.0.so.0
%{_libdir}/libnux-%{_major_ver}.0.so.0.400.0
%{_libdir}/libnux-core-%{_major_ver}.0.so.0
%{_libdir}/libnux-core-%{_major_ver}.0.so.0.400.0
%{_libdir}/libnux-graphics-%{_major_ver}.0.so.0
%{_libdir}/libnux-graphics-%{_major_ver}.0.so.0.400.0


%files devel
%doc AUTHORS
%dir %{_includedir}/Nux-%{_major_ver}.0/
%dir %{_includedir}/Nux-%{_major_ver}.0/Nux
%dir %{_includedir}/Nux-%{_major_ver}.0/Nux/ProgramFramework/
%dir %{_includedir}/Nux-%{_major_ver}.0/NuxCore/
%dir %{_includedir}/Nux-%{_major_ver}.0/NuxCore/Character/
%dir %{_includedir}/Nux-%{_major_ver}.0/NuxCore/FileManager/
%dir %{_includedir}/Nux-%{_major_ver}.0/NuxCore/Math/
%dir %{_includedir}/Nux-%{_major_ver}.0/NuxGraphics/
%{_includedir}/Nux-%{_major_ver}.0/Nux/Readme.txt
%{_includedir}/Nux-%{_major_ver}.0/Nux/*.h
%{_includedir}/Nux-%{_major_ver}.0/Nux/ProgramFramework/*.h
%{_includedir}/Nux-%{_major_ver}.0/NuxCore/*.h
%{_includedir}/Nux-%{_major_ver}.0/NuxCore/Character/*.h
%{_includedir}/Nux-%{_major_ver}.0/NuxCore/FileManager/*.h
%{_includedir}/Nux-%{_major_ver}.0/NuxCore/Math/*.h
%{_includedir}/Nux-%{_major_ver}.0/NuxGraphics/*.h
%{_libdir}/libnux-%{_major_ver}.0.so
%{_libdir}/libnux-core-%{_major_ver}.0.so
%{_libdir}/libnux-graphics-%{_major_ver}.0.so
%{_libdir}/pkgconfig/nux-%{_major_ver}.0.pc
%{_libdir}/pkgconfig/nux-core-%{_major_ver}.0.pc
%{_libdir}/pkgconfig/nux-graphics-%{_major_ver}.0.pc


%files common
%doc AUTHORS
%dir %{_datadir}/nux/
%dir %{_datadir}/nux/%{_major_ver}.0/
%dir %{_datadir}/nux/%{_major_ver}.0/Fonts/
%dir %{_datadir}/nux/%{_major_ver}.0/UITextures/
%{_datadir}/nux/%{_major_ver}.0/Fonts/*.txt
%{_datadir}/nux/%{_major_ver}.0/Fonts/*.png
%{_datadir}/nux/%{_major_ver}.0/UITextures/*.png
%{_datadir}/nux/%{_major_ver}.0/UITextures/*.tga
%{_datadir}/nux/%{_major_ver}.0/UITextures/Painter.xml
%{_datadir}/nux/%{_major_ver}.0/UITextures/UIArchive.iar


%files tools
%doc AUTHORS
%{_libexecdir}/unity_support_test
%{_sysconfdir}/X11/xinit/xinitrc.d/50_check_unity_support


%changelog
* Sat Sep 01 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.4.0-1
- Version 3.4.0

* Wed Aug 22 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.2.0-1
- Fix license

* Wed Aug 22 2012 Damian Ivanov <damianatorrpm@gmail.com> - 3.2.0-1
- Uses pkgconfig for dependencies 
- Add xorg-x11-xinit to dependencies (owns /etc/X11/xinit/xinitrc.d/ etc.)

* Mon Aug 13 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.2.0-1
- Version 3.2.0

* Fri Jul 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.0-1
- Version 3.0.0

* Tue Jul 10 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 2.12.0-1
- Initial release
- Version 2.12.0
