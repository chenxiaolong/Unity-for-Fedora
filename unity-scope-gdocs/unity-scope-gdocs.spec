# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

Name:		unity-scope-gdocs
Version:	0.4
Release:	1%{?dist}
Summary:	Google Docs scope for Unity

Group:		User Interface/Desktops
License:	GPLv3
URL:		https://launchpad.net/unity-lens-gdocs
Source0:	https://launchpad.net/unity-lens-gdocs/trunk/%{version}/+download/unity-scope-gdocs-%{version}.tar.gz

# Use /usr/libexec/ instead of /usr/lib/unity-scope-gdocs/
Patch0:		0001_Use_libexecdir.patch

BuildArch:	noarch

BuildRequires:	desktop-file-utils
BuildRequires:	python3-distutils-extra

BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(python3)

# Requires the GObject Introspection bindings for these libraries
Requires:	account-plugin-google
Requires:	dee
Requires:	libaccounts-glib
Requires:	libgdata
Requires:	libsignon-glib
Requires:	libunity

%description
This package contains a Google Docs scope for Unity which allows for searching
and browsing of Google Docs documents in the Unity dash.


%prep
%setup -q

%patch0 -p1 -b .libexecdir


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

desktop-file-validate \
  $RPM_BUILD_ROOT%{_datadir}/applications/unity-scope-gdocs.desktop


%post
touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor/ &>/dev/null || :


%files
%doc
%{_libexecdir}/unity-scope-gdocs
%{python3_sitelib}/unity_scope_gdocs-%{version}-py*.egg-info
%{_datadir}/applications/unity-scope-gdocs.desktop
%{_datadir}/dbus-1/services/unity-scope-gdocs.service
%{_datadir}/icons/hicolor/48x48/apps/unity-scope-gdocs.png
%dir %{_datadir}/unity/
%dir %{_datadir}/unity/lenses/
%dir %{_datadir}/unity/lenses/files/
%{_datadir}/unity/lenses/files/gdocs.scope


%changelog
* Thu Sep 27 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.4-1
- Initial release
- Version 0.4
