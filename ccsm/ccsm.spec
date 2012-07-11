# Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to>

%define _ubuntu_rel 0ubuntu3

Name:		ccsm
Version:	0.9.5.92
Release:	1.%{_ubuntu_rel}%{?dist}
Summary:	Compiz configuration manager

Group:		User Interface/Desktops
License:	GPLv2
URL:		https://launchpad.net/compizconfig-settings-manager
Source0:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-settings-manager_%{version}.orig.tar.gz

Source99:	https://launchpad.net/ubuntu/+archive/primary/+files/compizconfig-settings-manager_%{version}-%{_ubuntu_rel}.diff.gz

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	glib2-devel
BuildRequires:	libcompizconfig-devel
BuildRequires:	libxml2
BuildRequires:	libXtst-devel
BuildRequires:	python-compizconfig

Requires:	hicolor-icon-theme
Requires:	pygtk2
Requires:	python-compizconfig

# Satisfy OBS conflict on gtk3 (installed by build dependencies)
BuildRequires:  gtk3
BuildRequires:  gtk3-devel

# Satisfy OBS conflict on xorg-x11-proto-devel
BuildRequires:	xorg-x11-proto-devel

BuildArch:	noarch

%description
This package contains the Compiz configuration manager for modify Compiz and
its plugins' settings.


%prep
%setup -q

# Apply Ubuntu's patches
zcat '%{SOURCE99}' | patch -Np1
for i in $(grep -v '#' debian/patches/series); do
  patch -Np1 -i "debian/patches/${i}"
done


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --prefix %{_prefix} --root $RPM_BUILD_ROOT

# Fix desktop file
sed -i \
  -e '/^Encoding=/d' \
  -e '/^Categories=/ s/Compiz;//' \
  $RPM_BUILD_ROOT%{_datadir}/applications/ccsm.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/ccsm.desktop

%find_lang ccsm


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ ${1} -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :


%files -f ccsm.lang
%doc AUTHORS ChangeLog
%{_bindir}/ccsm
%dir %{python_sitelib}/ccm/
%{python_sitelib}/ccm/Conflicts.py*
%{python_sitelib}/ccm/Constants.py*
%{python_sitelib}/ccm/Pages.py*
%{python_sitelib}/ccm/Settings.py*
%{python_sitelib}/ccm/Utils.py*
%{python_sitelib}/ccm/Widgets.py*
%{python_sitelib}/ccm/Window.py*
%{python_sitelib}/ccm/__init__.py*
%{python_sitelib}/ccsm-0.9.5.92-py2.7.egg-info
%{_datadir}/applications/ccsm.desktop
%dir %{_datadir}/ccsm/
%{_datadir}/ccsm/icons/hicolor/*/categories/*.png
%{_datadir}/ccsm/icons/hicolor/*/devices/*.png
%{_datadir}/ccsm/icons/hicolor/*/mimetypes/*.png
%{_datadir}/ccsm/icons/hicolor/scalable/apps/*.svg
%{_datadir}/ccsm/icons/hicolor/scalable/categories/*.svg
%{_datadir}/ccsm/images/*.png
%{_datadir}/icons/hicolor/*/apps/ccsm.png
%{_datadir}/icons/hicolor/*/apps/ccsm.svg


%changelog
* Sun Jul 08 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 0.9.5.92-1.0ubuntu3
- Initial release
- Version 0.9.5.92
- Ubuntu release 0ubuntu3
