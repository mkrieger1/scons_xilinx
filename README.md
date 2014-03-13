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

Copy the entire `site_tools/xilinx` tree to a location you like.

SCons will find it in one of the following locations by default:

- `./site_scons` (relative to your `SConstruct`/`SConscript`)
- `$HOME/.scons/site_scons`
- `/usr/share/scons/site_scons`

If you choose a different location, you can point SCons to it using the
`--site-dir` command line option or by passing it as the `toolpath`
argument to the `Environment` constructor (read more
[here](http://www.scons.org/doc/production/HTML/scons-user.html#idm28309816)).

The file copying is handled for you if you call:

    scons install [--user|--prefix=<location>]

If the `--prefix` option is given, it specifies the directory into which
the `site_tools/xilinx` tree will be copied. If it is not given and the
`--user` flag is set,`$HOME/.scons/site_scons` will be used,
`/usr/share/scons/site_scons` otherwise.

  [SCons]: http://www.scons.org/
  [Builders]: http://www.scons.org/doc/production/HTML/scons-user.html#chap-builders-writing
  [example project]: example/SConstruct

