# PostProject OpenAssetIO integration validation

This focused integration asks one question: can a discoverable OpenAssetIO Manager turn
a PostProject representation reference into a `LocatableContent` URI without
leaking database or FFI details? It implements only read resolution; the
maintained Manager lives in `postproject-openassetio-manager`.

Host bindings carry `RepresentationRef(id)` while
IDs remain ordinary UUIDs. Test with a matching SDK wheel and native library.

This checkout requires the PostProject 0.9 development wheel and matching
native library. Manager initialization scans assets through an explicitly
owned read session with bounded pages.
