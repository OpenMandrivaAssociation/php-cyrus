%define realname cyrus
%define modname cyrus
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A16_%{modname}.ini

Summary:	An extension which eases the manipulation of Cyrus IMAP servers for PHP
Name:		php-%{modname}
Version:	1.0
Release:	%mkrel 27
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/cyrus
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
Patch0:		cyrus-1.0-lib64.diff
Requires:	php-cli >= 3:5.2.0
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	cyrus-imapd-devel
BuildRequires:	libsasl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An extension which eases the manipulation of Cyrus IMAP servers.

%prep

%setup -q -n %{modname}-%{version}
%patch0 -p0

cp %{SOURCE1} %{inifile}

%build
%serverbuild

#%{_usrsrc}/php4-devel/buildext %{modname} cyrus.c "-lsasl2 -lcyrus -lcyrus_min" \
#    "-DCOMPILE_DL_CYRUS -DHAVE_CYRUS -I%{_includedir}/sasl"

phpize
export CYRUS_SHARED_LIBADD="-L%{_libdir} -lsasl2 -lcyrus -lcyrus_min"
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc CREDITS README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
