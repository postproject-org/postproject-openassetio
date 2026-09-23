# PostProject OpenAssetIO integration validation

This focused integration asks one question: can a discoverable OpenAssetIO Manager turn
a PostProject representation reference into a `LocatableContent` URI without
leaking database or FFI details? It implements only read resolution; the
maintained Manager lives in `postproject-openassetio-manager`.
