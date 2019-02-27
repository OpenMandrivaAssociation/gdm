%define _disable_ld_no_undefined 1

%define major		1
%define	gmajor		1.0
%define libname		%mklibname gdm %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname gdm-gir %{gmajor}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	The GNOME Display Manager
Name:		gdm
Version:	3.30.3
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/gdm/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
# (cg) Managing patches via git
# git format-patch --start-number 100 3.1.2..mga-3.1.2-cherry-picks

Patch0303:	0303-Read-.xsetup-scripts.patch

# It is possible that we will have to import several patches from Fedora and Mageia. Just test it after build and see if needed. (pengin)

Provides:	dm

Requires(pre):		rpm-helper
Requires(postun):	rpm-helper
Requires(post):		dconf
Requires:	pam
Requires:	sessreg
Requires:	usermode
Requires:	cdialog
Requires:	zenity
Requires:	gnome-session-bin
Requires:	gnome-settings-daemon
Suggests:	gnome-power-manager
Requires:	xinitrc >= 2.4.14
Requires:	dbus-x11
Requires:	polkit-gnome
Requires:	accountsservice
Requires:	gnome-shell
#Droped in upstream, use adwaita
#Requires:	gnome-icon-theme-symbolic
Requires:	adwaita-icon-theme
Requires:	x11-server-xwayland
Requires:	xhost
Provides:	gdm-Xnest
Obsoletes:	gdm-Xnest

Obsoletes:	gdm-themes
Conflicts:	gdm-220
BuildRequires: 	pkgconfig(accountsservice) >= 0.6.12
BuildRequires:	pkgconfig(check) >= 0.9.4
BuildRequires:	pkgconfig(dbus-glib-1) >= 0.74
BuildRequires:	pkgconfig(fontconfig) >= 2.5.0
BuildRequires:	pkgconfig(gio-2.0) >= 2.29.3
BuildRequires:	pkgconfig(gobject-2.0) >= 2.29.3
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.91.1
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.4
BuildRequires:	pkgconfig(libxklavier) >= 4.0
BuildRequires:	pkgconfig(nss) >= 3.11.1
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(ply-boot-client)
BuildRequires:	pkgconfig(upower-glib) >= 0.9.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(libkeyutils)
BuildRequires:	dconf
BuildRequires:	pam-devel
BuildRequires:	libwrap-devel
BuildRequires:	audit-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	gettext-devel
BuildRequires:	yelp-tools
BuildRequires:	itstool
BuildRequires:	gnome-common
BuildRequires:	rpm-helper
BuildRequires:	pkgconfig(xorg-server)
Obsoletes:	gdm-user-switch-applet < 3.0.0

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%pre
%_pre_useradd gdm %{_var}/lib/gdm /bin/false
%_pre_groupadd xgrp gdm

%post

# (cg) Setup dconf settings for gdm
# http://git.gnome.org/browse/gdm/commit/?id=eebeb62e2daccc932f3033fbd857b619ba9936d0
dconf update

if [ -x /usr/sbin/chksession ]; then /usr/sbin/chksession -g || true; fi

%update_scrollkeeper
%{_sbindir}/gdm-safe-restart >/dev/null 2>&1 || :

%postun
%_postun_userdel gdm
%_postun_groupdel xgrp gdm

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README.md
%_sysconfdir/dbus-1/system.d/gdm.conf
%{_bindir}/gdm-screenshot
%{_bindir}/gdmflexiserver
%{_sbindir}/gdm
%dir %{_sysconfdir}/X11/gdm
%{_sysconfdir}/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/pam.d/gdm-fingerprint
%config(noreplace) %{_sysconfdir}/pam.d/gdm-password
%config(noreplace) %{_sysconfdir}/pam.d/gdm-pin
%config(noreplace) %{_sysconfdir}/pam.d/gdm-smartcard
%config(noreplace) %{_sysconfdir}/pam.d/gdm-launch-environment
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%{_libdir}/security/pam_gdm.so

%{_libexecdir}/gdm-host-chooser
%{_libexecdir}/gdm-session-worker
%{_libexecdir}/gdm-simple-chooser
%{_libexecdir}/gdm-disable-wayland
%{_libexecdir}/gdm-wayland-session
%{_libexecdir}/gdm-x-session
/rules.d/61-gdm.rules
%{_datadir}/pixmaps/*
%{_datadir}/gdm
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/gnome-session/sessions/gnome-login.session
%dir %{_datadir}/hosts
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
#attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/applications
%attr(1755, gdm, gdm) %dir %{_localstatedir}/run/gdm/greeter
%attr(1777, root, gdm) %dir %{_localstatedir}/run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm
%attr(700,gdm,gdm) %dir %{_localstatedir}/lib/gdm/.local
%attr(700,gdm,gdm) %dir %{_localstatedir}/lib/gdm/.local/share
%attr(700,gdm,gdm) %dir %{_localstatedir}/lib/gdm/.local/share/applications
%{_datadir}/dconf/profile/gdm
%dir %{_var}/log/gdm
%{_datadir}/icons/hicolor/*/apps/gdm*
# (cg) Note: Ship this, but lets not enable it or do anything fancy
# until we fully redo any prefdm stuff and have units for all DMs
# we support.
%{_unitdir}/gdm.service

%exclude /usr/lib*/debug/usr/lib*/security/pam_gdm.so-3.30.1-1.x86_64.debug
%exclude /usr/lib*/debug/usr/libexec/gdm-disable-wayland-3.30.1-1.x86_64.debug

#--------------------------------------------------------------------
%package -n %{libname}
Summary:	Library for the %name greeter
Group:		System/Libraries
Obsoletes:	%{_lib}gdmreeter1 < 3.2.1-3

%description -n %{libname}
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%files -n %{libname}
%{_libdir}/libgdm.so.%{major}*

#--------------------------------------------------------------------

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/Gdm-%{gmajor}.typelib

#--------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files -n %{develname}
%{_includedir}/gdm
%{_libdir}/libgdm.so
%{_libdir}/pkgconfig/gdm.pc
%{_libdir}/pkgconfig/gdm-pam-extensions.pc
%{_datadir}/gir-1.0/Gdm-%{gmajor}.gir

#--------------------------------------------------------------------

%prep
%autosetup -p1
cp data/Init.in data/Default.in

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure \
	--with-sysconfsubdir=X11/gdm \
	--with-dmconfdir=%{_sysconfdir}/X11/dm \
	--disable-static \
	--with-console-kit=no \
	--with-systemd \
	--with-plymouth \
	--without-xdmcp

%make_build

%install
%make_install PAM_PREFIX=%{_sysconfdir}

# don't provide PreSession/PostSession, pam handle this
rm -f %{buildroot}%{_sysconfdir}/X11/PreSession/Default
rm -f %{buildroot}%{_sysconfdir}/X11/PostSession/Default

mkdir -p %{buildroot}%{_datadir}/hosts

%find_lang %{name} --with-gnome --all-name

mkdir -p %{buildroot}%{_var}/log/gdm %{buildroot}%{_sysconfdir}/X11/dm/Sessions

#remove unpackaged files
rm -rf %{buildroot}%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
  %{buildroot}%{_datadir}/xsessions/gnome.desktop

find %{buildroot} -name '*.la' -delete

# (cg) The existing gdm file is what we really want for gdm-password
rm -f %{buildroot}%{_sysconfdir}/pam.d/gdm-password
ln -s gdm %{buildroot}%{_sysconfdir}/pam.d/gdm-password

pushd %{buildroot}%{_sysconfdir}
ln -s X11/gdm
popd

# (ovitters) gdm-session starts gdm-x-session which can start /etc/X11/gdm/Xsession
#            ensure it is a symlink to the xinitrc Xsession
ln -s ../Xsession %{buildroot}%{_sysconfdir}/X11/gdm/Xsession

# (tmb) must exist for gdm to start xorg when WaylandEnable=false
mkdir -p %{buildroot}%{_localstatedir}/lib/gdm/.local/share/xorg

echo "auth       optional pam_group.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm
echo "auth       optional pam_group.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm-autologin
echo "session    required    pam_systemd.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm
echo "session    required    pam_systemd.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm-autologin
