About
=====

This is a collection of [SCons][] tools for automating the Xilinx build
flow.

The package makes a set of [Builders][] available, which you can use in a
`SConstruct` or `SConscript` file:

| Builder      | Source files | Target files |
|--------------|--------------|--------------|
|`Coregen`     |`.xco`        |`.ngc`, `.v`  |
|`XstSynthesis`|`.v`, `.vhd`  |`.ngc`        |
|`NgdBuild`    |`.ngc`, `.ucf`|`.ngd`        |
|`Map`         |`.ngd`        |`_map.ncd`    |
|`PlaceRoute`  |`_map.ncd`    |`.ncd`        |
|`BitGen`      |`.ncd`        |`.bit`        |

Example usage:

```python
env = Environment(tools=['xilinx'])
env.XstSynthesis('out.ngc', ['source.v', 'module.v'])
```

To see in more detail how the tools can be used, look at the
[example project][].

Installation
============

Copy the entire `xilinx` directory into a directory
`<root>/site_scons/site_tools`, where `<root>` must be visible to SCons
when invoked.

By default, SCons accepts the following locations as `<root>`:

- the current working directory (where `SConstruct`/`SConscript` is)
- `$HOME/.scons` (installation for single user)
- `/usr/share/scons` (installation for all users)

The file copying is handled for you if you call

    scons install [--user]

where the presence of the `--user` option selects between the `$HOME/.scons`
and the `/usr/share/scons` location.

If you choose to copy the tools to a different `<root>` location, you can
point SCons to it either by passing the command line argument
`--site-dir=<root>` or by using

```python
env = Environment(tools=['xilinx'], toolpath=['<root>'])
```

in the `SConstruct`/`SConscript` file.

  [SCons]: http://www.scons.org/
  [Builders]: http://www.scons.org/doc/production/HTML/scons-user.html#chap-builders-writing
  [example project]: example/SConstruct

