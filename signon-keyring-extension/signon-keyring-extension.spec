# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

# This package (also) has three names
# - signon-keyring-extension (Ubuntu's packaging)
# - keyring (Tarball name)
# - online-accounts-keyring-extension (Website)

# We'll use the same name as Ubuntu (signon-keyring-extension)

Name:		signon-keyring-extension
Version:	0.4daily12.12.06
Release:	1%{?dist}
Summary:	GNOME Keyring Extension for signond

Group:		User Interface/Desktops
License:	LGPLv2
URL:		https://launchpad.net/online-accounts-keyring-extension
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/signon-keyring-extension_%{version}.orig.tar.gz

BuildRequires:	pkgconfig

BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(signond)

%description
This package contains an extension for signond, which allows it to use the
GNOME Keyring.


%prep
%setup -q


%build
%_qt4_qmake \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  QMAKE_CXXFLAGS="%{optflags}"

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_bindir}/keyring-test


%files
%doc COPYING
%dir %{_libdir}/signon/
%dir %{_libdir}/signon/extensions/
%{_libdir}/signon/extensions/libkeyring.so


%changelog
* Mon Jan 27 2013 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4daily12.12.06-1
- Version 0.4daily12.12.06

* Tue Sep 04 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4-1
- Initial release
- Version 0.4
