# Findings

- PostProject's HTTPS host-object reference is accepted directly as an
  OpenAssetIO entity reference; no second identifier format is needed.
- Opening the production once during Manager initialization keeps native
  handles out of individual resolution calls.
- OpenAssetIO batch callbacks are the boundary where PostProject ambiguity and
  missing entities must become per-element errors.
- A usable Manager must advertise policy and trait-introspection capabilities
  even when the experiment only resolves one trait.
- A production Manager needs trait introspection, policy queries, root mapping,
  sequence traits, and entity-existence support beyond this validation.
