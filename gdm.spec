# otherwise rpmlint sees %%gconf-tree.xml as unexpanded
%define	_build_pkgcheck_set %{nil}

%define major		1
%define	gmajor		1.0
%define libname		%mklibname gdmgreeter %{major}
%define libsimple	%mklibname gdmsimplegreeter %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname gdmgreeter-gir %{gmajor}

Summary: The GNOME Display Manager
Name: gdm
Version: 3.2.1.1
Release: 1
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.gnome.org/projects/gdm/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gdm/%{name}-%{version}.tar.xz

# (cg) Managing patches via git
# git format-patch --start-number 100 3.1.2..mga-3.1.2-cherry-picks
# git format-patch --start-number 200 mga-3.1.2-cherry-picks..mga-3.1.2-plymouth
Patch0200:	0200-Save-root-window-to-pixmap-at-_XROOTPMAP_ID.patch
Patch0201:	0201-Enable-smooth-transition-between-plymouth-and-X.patch
Patch0202:	0202-Fedora-force-active-vt-patch-separated-from-plymouth.patch
Patch0203:	0203-Mageia-force-active-vt-patch-fix.patch
# git format-patch --start-number 300 mga-3.1.2-plymouth..mga-3.1.2-patches
Patch0300:	0300-Novell-Make-keyboard-selector-not-neglect-to-apply-t.patch
Patch0301:	0301-Novell-Look-at-the-current-runlevel-before-managing-.patch
Patch0302:	0302-Mageia-Fix-gdm-pam.d-file-for-gnome-keyring-integrat.patch

# (tmb) fix gdm to execute .xsetup scripts, otherwise LiveCDs are broken
Patch400:	gdm-3.2.1.1-init-execute-xsetup-scripts.patch

BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	audit-devel
BuildRequires:	gettext-devel
BuildRequires:	libwrap-devel
BuildRequires:	pam-devel
BuildRequires: 	pkgconfig(accountsservice)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xrandr)

Requires: cdialog
Requires(post): dconf
# for XFdrake on failsafe fallback:
Requires: drakx-kbd-mouse-x11
Requires: gnome-session-bin
Requires: gnome-settings-daemon
Requires: metacity
Requires: pam
Requires: polkit-gnome
Requires(pre,postun): rpm-helper
Requires: sessreg
Requires: usermode
Requires: xinitrc
Requires: zenity
Suggests: gnome-power-manager

Provides: dm
%rename gdm-Xnest
%rename user-switch-applet
Obsoletes: gdm-themes
Conflicts: gdm-220

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%package -n %{libname}
Summary:	Library for the %name greeter
Group:		System/Libraries
Obsoletes:	%{_lib}gdmreeter1 < 3.2.1-3

%description -n %{libname}
This package contains the shared library gdmgreeter for %{name}.

%package -n %{libsimple}
Summary:	Library for the %name simple greeter
Group:		System/Libraries

%description -n %{libsimple}
This package contains the shared library gdmsimplegreeter for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libsimple} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
cp data/Init.in data/Default.in
%apply_patches

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x \
	--disable-static \
	--enable-console-helper  \
	--with-sysconfsubdir=X11/gdm \
	--with-dmconfdir=%{_sysconfdir}/X11/dm \
	--with-console-kit=yes 

%make LIBS='-lgmodule-2.0 -ldbus-glib-1'

%install
%makeinstall_std PAM_PREFIX=%{_sysconfdir}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# don't provide PreSession/PostSession, pam handle this
rm -f %{buildroot}%{_sysconfdir}/X11/PreSession/Default
rm -f %{buildroot}%{_sysconfdir}/X11/PostSession/Default

mkdir -p %{buildroot}%{_datadir}/hosts
mkdir -p %{buildroot}%{_var}/log/gdm %{buildroot}%{_sysconfdir}/X11/dm/Sessions
mkdir -p %{buildroot}%{_var}/lib/gdm/.gconf.defaults

# (cg) For ghost ownership
touch %{buildroot}%{_sysconfdir}/dconf/db/%{name}

#remove unpackaged files
rm -rf %{buildroot}%{_sysconfdir}/X11/gdm/PostLogin/Default.sample \
	%{buildroot}%{_datadir}/xsessions/gnome.desktop

%find_lang %{name} --with-gnome --all-name

%pre
%_pre_useradd gdm %{_var}/lib/gdm /bin/false
%_pre_groupadd xgrp gdm

%post
if [ -f /%{_sysconfdir}/X11/xdm/Xsession -a ! -x /%{_sysconfdir}/X11/xdm/Xsession ]; then
	chmod +x /%{_sysconfdir}/X11/xdm/Xsession
fi
if [ -x /usr/sbin/chksession ]; then /usr/sbin/chksession -g || true; fi
%{_sbindir}/gdm-safe-restart >/dev/null 2>&1 || :

%postun
%{make_session}
%_postun_userdel gdm
%_postun_groupdel xgrp gdm

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/dbus-1/system.d/gdm.conf
%dir %{_sysconfdir}/X11/gdm
%ghost %{_sysconfdir}/dconf/db/%{name}
%dir %{_sysconfdir}/dconf/db/gdm.d
%dir %{_sysconfdir}/dconf/db/gdm.d/locks
%{_sysconfdir}/dconf/db/gdm.d/00-upstream-settings
%{_sysconfdir}/dconf/db/gdm.d/locks/00-upstream-settings-locks
%{_sysconfdir}/dconf/profile/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm
%config(noreplace) %{_sysconfdir}/pam.d/gdm-autologin
%config(noreplace) %{_sysconfdir}/pam.d/gdm-fingerprint
%config(noreplace) %{_sysconfdir}/pam.d/gdm-password
%config(noreplace) %{_sysconfdir}/pam.d/gdm-smartcard
%config(noreplace) %{_sysconfdir}/pam.d/gdm-welcome
%config(noreplace) %{_sysconfdir}/X11/gdm/custom.conf
%config(noreplace) %{_sysconfdir}/X11/gdm/Xsession
%dir %{_sysconfdir}/X11/dm
%dir %{_sysconfdir}/X11/dm/Sessions
%config(noreplace) %{_sysconfdir}/X11/gdm/PreSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostSession
%config(noreplace) %{_sysconfdir}/X11/gdm/PostLogin
%config(noreplace) %{_sysconfdir}/X11/gdm/Init
%{_sysconfdir}/gconf/schemas/gdm-simple-greeter.schemas
%{_bindir}/gdm-screenshot
%{_bindir}/gdmflexiserver
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_libexecdir}/gdm-crash-logger
%{_libexecdir}/gdm-factory-slave
%{_libexecdir}/gdm-host-chooser
%{_libexecdir}/gdm-product-slave
%{_libexecdir}/gdm-session-worker
%{_libexecdir}/gdm-simple-chooser
%{_libexecdir}/gdm-simple-greeter
%{_libexecdir}/gdm-simple-slave
%{_libexecdir}/gdm-smartcard-worker
%{_libexecdir}/gdm-xdmcp-chooser-slave
%{_libexecdir}/gdm/simple-greeter/extensions/libfingerprint.so
%{_libexecdir}/gdm/simple-greeter/extensions/libpassword.so
%{_libexecdir}/gdm/simple-greeter/extensions/libsmartcard.so
%{_datadir}/gdm
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/gnome-session/sessions/gdm-fallback.session
%{_datadir}/gnome-session/sessions/gdm-shell.session
%{_datadir}/pixmaps/*
%dir %{_datadir}/hosts
%dir %{_localstatedir}/spool/gdm
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.mandatory
%attr(1640, gdm, gdm) %{_localstatedir}/lib/gdm/.gconf.mandatory/*.xml
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.defaults
%attr(1640, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.gconf.path
%attr(1755, gdm, gdm) %dir %{_localstatedir}/run/gdm/greeter
%attr(1777, root, gdm) %dir %{_localstatedir}/run/gdm
%attr(1755, root, gdm) %dir %{_localstatedir}/cache/gdm

%dir %{_var}/log/gdm
%{_datadir}/icons/hicolor/*/apps/gdm*
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/
%attr(1750, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.local/share/applications

%files -n %{libname}
%{_libdir}/libgdmgreeter.so.%{major}*

%files -n %{libsimple}
%{_libdir}/libgdmsimplegreeter.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GdmGreeter-%{gmajor}.typelib

%files -n %{develname}
%{_includedir}/gdm/simple-greeter
%{_includedir}/gdm/greeter/gdm-greeter-client.h
%{_includedir}/gdm/greeter/gdm-greeter-sessions.h
%{_libdir}/libgdmsimplegreeter.so
%{_libdir}/libgdmgreeter.so
%{_libdir}/pkgconfig/gdmsimplegreeter.pc
%{_libdir}/pkgconfig/gdmgreeter.pc
%{_datadir}/gir-1.0/GdmGreeter-%{gmajor}.gir

