%define _disable_ld_no_undefined 1

%define major		1
%define	gmajor		1.0
%define libname		%mklibname gdm %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname gdm-gir %{gmajor}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	The GNOME Display Manager
Name:		gdm
Version:	48.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://www.gnome.org/projects/gdm/
Source0:      https://ftp.gnome.org/pub/GNOME/sources/gdm/%{url_ver}/%{name}-%{version}.tar.xz
Source1:      gnome-enable-root-gui.desktop
Source2:      gdm-password
Source3:      gdm.sysusers

Provides:	dm

Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): dconf
Requires: pam
Requires: sessreg
#Requires: usermode
Requires: cdialog
Requires: zenity-gtk
#Requires: gnome-session-bin
Requires: gnome-settings-daemon
Suggests: gnome-power-manager
Requires: xinitrc >= 2.4.14
Requires: dbus-x11
# While the rest of the world has moved on to dbus-broker, gdm
# still hardcodes dbus-daemon calls and can't live without it.
# Don't update this dependency unless and until gdm-x11-session.c
# and gdm-wayland-session.c stop exec-ing dbus-daemon.
# https://gitlab.gnome.org/GNOME/gdm/-/blob/main/daemon/gdm-x-session.c?ref_type=heads#L463
# https://gitlab.gnome.org/GNOME/gdm/-/blob/main/daemon/gdm-wayland-session.c?ref_type=heads#L139
Requires: dbus-daemon
Requires: polkit-gnome
Requires: accountsservice
#Requires: gnome-shell
#Droped in upstream, use adwaita
#Requires: gnome-icon-theme-symbolic
#Requires: gnome-shell
Requires: adwaita-icon-theme
Requires: x11-server-xwayland
Requires: xhost
# As of 47.0: Sad, but true: gnome filth has become so dirty that even the display
# manager requires half the broken desktop.
# The greeter launches its UI by calling
# /usr/libexec/gdm-x-session "dbus-run-session -- gnome-session --autostart /usr/share/gdm/greeter/autostart"
# Resulting in a permanent black screen if gnome-session isn't there.
# gnome-session then calls the piece of bloat that is gnome-shell.
Requires: gnome-session
Requires: gnome-shell
Provides: gdm-Xnest
Obsoletes: gdm-Xnest

Obsoletes: gdm-themes
Conflicts: gdm-220
BuildRequires: pkgconfig(accountsservice) >= 0.6.12
BuildRequires: pkgconfig(check) >= 0.9.4
BuildRequires: pkgconfig(dconf)
BuildRequires: pkgconfig(dbus-glib-1) >= 0.74
BuildRequires: pkgconfig(fontconfig) >= 2.5.0
BuildRequires: pkgconfig(gio-2.0) >= 2.29.3
BuildRequires: pkgconfig(gobject-2.0) >= 2.29.3
#gobject-introspection-1.0 provided by lib64girepository-devel
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gthread-2.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 2.91.1
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libcanberra-gtk3) >= 0.4
BuildRequires: pkgconfig(libxklavier) >= 4.0
BuildRequires: pkgconfig(nss) >= 3.11.1
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(systemd)
BuildRequires: systemd-rpm-macros
BuildRequires: pkgconfig(ply-boot-client)
BuildRequires: pkgconfig(upower-glib) >= 0.9.0
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xdmcp)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(libkeyutils)
BuildRequires: pkgconfig(udev)
BuildRequires: cmake
BuildRequires: meson
BuildRequires: dconf
BuildRequires: pam-devel
BuildRequires: libwrap-devel
BuildRequires: audit-devel
BuildRequires: intltool >= 0.40.0
BuildRequires: gettext-devel
BuildRequires: yelp-tools
BuildRequires: itstool
BuildRequires: gnome-common
BuildRequires: rpm-helper
BuildRequires: pkgconfig(xorg-server)
Obsoletes: gdm-user-switch-applet < 3.0.0

%patchlist
gdm-46.2-no-selinux-deps.patch

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%pre
%_pre_groupadd xgrp gdm

%preun
%systemd_preun gdm.service

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
%{_sysusersdir}/%{name}.conf
%{_bindir}/gdmflexiserver
%{_bindir}/gdm-config
%{_sbindir}/gdm
%{_prefix}/lib/udev/rules.d/61-gdm.rules
%dir %{_sysconfdir}/X11/gdm
%{_sysconfdir}/gdm
#config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/pam.d/gdm-fingerprint
%config(noreplace) %{_sysconfdir}/pam.d/gdm-password
%config(noreplace) %{_sysconfdir}/pam.d/gdm-smartcard
%config(noreplace) %{_sysconfdir}/pam.d/gdm-launch-environment
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%config(noreplace) %{_sysconfdir}/X11/gdm/Xsession
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%{_libdir}/security/pam_gdm.so

%{_libexecdir}/gdm-*
%{_datadir}/gdm
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/gnome-session/sessions/gnome-login.session
%{_datadir}/polkit-1/rules.d/20-gdm.rules
%dir %{_datadir}/hosts
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(700,gdm,gdm) %dir %{_localstatedir}/lib/gdm/.local
%attr(700,gdm,gdm) %dir %{_localstatedir}/lib/gdm/.local/share
%{_datadir}/dconf/profile/gdm
%dir %{_var}/log/gdm
# (cg) Note: Ship this, but lets not enable it or do anything fancy
# until we fully redo any prefdm stuff and have units for all DMs
# we support.
%{_unitdir}/gdm.service
%{_sysconfdir}/xdg/autostart/gnome-enable-root-gui.desktop
%{_prefix}/lib/systemd/user/gnome-session@gnome-login.target.d/session.conf

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
%meson -Dpam-prefix=%{_sysconfdir} \
       --sysconfdir=%{_sysconfdir}/X11 \
       -Ddbus-sys=%{_sysconfdir}/dbus-1/system.d \
       -Drun-dir=/run/gdm \
       -Dudev-dir=%{_udevrulesdir} \
       -Ddefault-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/usr/games \
       -Dprofiling=true \
       -Dplymouth=enabled \
       -Dselinux=disabled

%meson_build

%install
%meson_install

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
#ln -s gdm %{buildroot}%{_sysconfdir}/pam.d/gdm-password
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/gdm-password

# (angry p) Install sysusers needed for rpm 4.19
install -p -m644 -D %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf

pushd %{buildroot}%{_sysconfdir}
ln -s X11/gdm
popd

# (ovitters) gdm-session starts gdm-x-session which can start /etc/X11/gdm/Xsession
#            ensure it is a symlink to the xinitrc Xsession
ln -s ../Xsession %{buildroot}%{_sysconfdir}/X11/gdm/Xsession

# (tmb) must exist for gdm to start xorg when WaylandEnable=false
mkdir -p %{buildroot}%{_localstatedir}/lib/gdm/.local/share/xorg

# (martinw) enable root apps (e.g. MCC) to run in Wayland
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/gnome-enable-root-gui.desktop

#echo "auth       optional pam_group.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm
echo "auth       optional pam_group.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm-autologin
#echo "session    required    pam_systemd.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm
echo "session    required    pam_systemd.so" >> %{buildroot}%{_sysconfdir}/pam.d/gdm-autologin
