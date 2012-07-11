# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		libgdu
Version:	3.0.2
Release:	1%{?dist}
Summary:	GNOME library for dealing with storage devices

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://git.gnome.org/cgit/gnome-disk-utility
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-disk-utility/3.0/gnome-disk-utility-3.0.2.tar.xz

Patch0:		0001_Build_library_only.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gnome-common
BuildRequires:	intltool

BuildRequires:	dbus-glib-devel
BuildRequires:	glib2-devel
BuildRequires:	libatasmart-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	udisks-devel

%description
This package contains the GNOME Disk Utility libraries from GNOME 3.0.


%package devel
Summary:	Development files for libgdu
Group:		Development/Libraries

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files for the GNOME Disk Utility library.


%prep
%setup -q -n gnome-disk-utility-%{version}

%patch0 -p1 -b .libonly

# Remove unused source code
rm -rvf \
  data/ \
  doc/ \
  help/ \
  src/format-tool/ \
  src/gdu-gtk \
  src/nautilus-extension \
  src/notification \
  src/palimpsest

autoreconf -vfi


%build
%configure --disable-scrollkeeper --disable-nautilus --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete


%post -p /usr/sbin/ldconfig

%postun -p /usr/sbin/ldconfig


%files
%doc AUTHORS NEWS README
%{_libdir}/libgdu.so.0
%{_libdir}/libgdu.so.0.0.0


%files devel
%doc AUTHORS NEWS README
%dir %{_includedir}/gnome-disk-utility/
%{_includedir}/gnome-disk-utility/gdu/gdu-adapter.h
%{_includedir}/gnome-disk-utility/gdu/gdu-callbacks.h
%{_includedir}/gnome-disk-utility/gdu/gdu-device.h
%{_includedir}/gnome-disk-utility/gdu/gdu-drive.h
%{_includedir}/gnome-disk-utility/gdu/gdu-error.h
%{_includedir}/gnome-disk-utility/gdu/gdu-expander.h
%{_includedir}/gnome-disk-utility/gdu/gdu-hub.h
%{_includedir}/gnome-disk-utility/gdu/gdu-known-filesystem.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume-group.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume-hole.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-lvm2-volume.h
%{_includedir}/gnome-disk-utility/gdu/gdu-linux-md-drive.h
%{_includedir}/gnome-disk-utility/gdu/gdu-machine.h
%{_includedir}/gnome-disk-utility/gdu/gdu-pool.h
%{_includedir}/gnome-disk-utility/gdu/gdu-port.h
%{_includedir}/gnome-disk-utility/gdu/gdu-presentable.h
%{_includedir}/gnome-disk-utility/gdu/gdu-process.h
%{_includedir}/gnome-disk-utility/gdu/gdu-types.h
%{_includedir}/gnome-disk-utility/gdu/gdu-util.h
%{_includedir}/gnome-disk-utility/gdu/gdu-volume-hole.h
%{_includedir}/gnome-disk-utility/gdu/gdu-volume.h
%{_includedir}/gnome-disk-utility/gdu/gdu.h
%{_libdir}/libgdu.so
%{_libdir}/pkgconfig/gdu.pc


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0.2-1
- Initial release
- Version 3.0.2