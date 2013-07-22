# An RPM spec file install a Glasgow Haskell Compiler version able to bootstrap
# GHC 7.6.x
#
# We want the latest ghc, 7.6.3, but it's binary release is not compatible with
# glibc on CentOS 5.
#
# We need to build it from source, but you need GHC to build GHC. :/
#
# The latest binary GHC release I could find that worked on CentOS 5 is 6.12.3.
#
# You cannot build ghc-7.6.3 with anything less then ghc-7.* (whose binary
# dists do not work on CentOS 5)
#
# So we need to build ghc-7.0.2 from source with ghc-6.12.3 binaries to allow
# us build our final target of ghc-7.6.3

# To Build:
# sudo yum -y install rpmdevtools gmp-devel && rpmdev-setuptree
# sudo yum -y install gmp-devel glibc-devel ncurses-devel  gmp-devel automake libtool gcc44 make  perl python libffi-devel ghc-bootstrap-compiler6
# wget http://www.haskell.org/ghc/dist/7.0.2/ghc-7.0.2-src.tar.bz2 -O ~/rpmbuild/SOURCES/ghc-7.0.2-src.tar.bz2
# wget https://raw.github.com/nmilford/rpm-ghc-bootsrap-compiler7/master/ghc-bootsrap-compiler7.spec -O ~/rpmbuild/SPECS/ghc-bootsrap-compiler7.spec
# rpmbuild -bb ~/rpmbuild/SPECS/ghc-bootsrap-compiler7.spec

%define ghc_bootstrap_ver 6.12.3
%define ghc_bootstrap_pkg ghc-bootstrap-compiler6

Name:           ghc-bootstrap-compiler7
Version:        7.0.2
Release:        1
Summary:        Glasgow Haskell Compiler version able to bootstrap GHC 7.0.x
Group:          Development/Languages
License:        The Glasgow Haskell Compiler License
URL:            http://www.haskell.org/ghc/
Source0:        http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{ghc_bootstrap_pkg}
BuildRequires:  gmp-devel
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  gmp-devel
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc44
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  python
BuildRequires:  libffi-devel

%description
GHC is a state-of-the-art, open source, compiler and interactive environment
for the functional language Haskell.

This package will install %{version}, which is packaged for the bootstrapping
of newer GHC versions.

%prep
%setup -q -n ghc-%{version}

%build
./configure --with-ghc=/usr/bin/ghc-%{ghc_bootstrap_ver} --with-gcc=/usr/bin/gcc44 --docdir=%{buildroot}/usr/share/doc/ghc-%{version}/

make 

%install
install -d -m 755 %{buildroot}/usr/

%makeinstall
rm -f %{buildroot}/usr/bin/ghc
rm -f %{buildroot}/usr/bin/ghc-pkg
rm -f %{buildroot}/usr/bin/ghci
rm -rf %{buildroot}/usr/share/man/*
mv %{buildroot}/usr/bin/haddock{,-%{version}}
mv %{buildroot}/usr/bin/hp2ps{,-%{version}}
mv %{buildroot}/usr/bin/hpc{,-%{version}}
mv %{buildroot}/usr/bin/hsc2hs{,-%{version}}
mv %{buildroot}/usr/bin/runghc{,-%{version}}
rm -rf %{buildroot}/usr/bin/runhaskell{,-%{version}}

install -d -m 755 %{buildroot}/usr/share/doc/ghc-%{version}
install    -m 644 %{_builddir}/ghc-%{version}/README  %{buildroot}/usr/share/doc/ghc-%{version}
install    -m 644 %{_builddir}/ghc-%{version}/LICENSE %{buildroot}/usr/share/doc/ghc-%{version}

for file in ghc-%{version} ghci-%{version} ghc-pkg-%{version} haddock-ghc-%{version} hp2ps-%{version} hsc2hs-%{version} runghc-%{version}; do
  sed -i -e  's|%{buildroot}||g' %{buildroot}%{_bindir}/$file
done

cd %{buildroot}/%{_libdir}/ghc-%{version}/package.conf.d/
for pkg in *; do
  sed -i -e  's|%{buildroot}||g' $pkg
done
cd -

%post
%{_bindir}/ghc-pkg-%{version} recache

%files
%defattr(-,root,root)
%{_libdir}/ghc-%{version}
%{_bindir}/*
/usr/share/*

%changelog
* Mon Jul 08 2013 Nathan Milford <nathan@milford.io> 7.0.2-1
- Initial spec.
- This is specifically meant to build newer versions of GHC.
