"""Smallest useful read-only PostProject OpenAssetIO Manager."""

from openassetio import constants
from openassetio.access import EntityTraitsAccess, PolicyAccess, ResolveAccess
from openassetio.errors import BatchElementError
from openassetio.managerApi import ManagerInterface
from openassetio.trait import TraitsData
from openassetio_mediacreation.traits.content import LocatableContentTrait_v1
from openassetio_mediacreation.traits.managementPolicy import ManagedTrait
from postproject import Production, RepresentationId

PREFIX = "https://postproject.org/ref/v1/"
Location = LocatableContentTrait_v1


class Interface(ManagerInterface):
    """Resolve one representation trait through PostProject's public API."""

    def __init__(self):
        super().__init__()
        self.production = None
        self.representations = {}

    def identifier(self):
        return "org.postproject.manager-spike"

    def displayName(self):
        return "PostProject Manager spike"

    def info(self):
        return {constants.kInfoKey_EntityReferencesMatchPrefix: PREFIX}

    def settings(self, hostSession):
        return {"production_path": "", "library_path": ""}

    def initialize(self, settings, hostSession):
        self.production = Production.open(
            settings["production_path"],
            library_path=settings.get("library_path") or None,
        )
        self.representations = {
            str(representation.id): representation
            for asset in self.production.assets
            for representation in self.production.representations[asset.id]
        }

    def hasCapability(self, capability):
        return capability in (
            ManagerInterface.Capability.kEntityReferenceIdentification,
            ManagerInterface.Capability.kManagementPolicyQueries,
            ManagerInterface.Capability.kResolution,
            ManagerInterface.Capability.kEntityTraitIntrospection,
        )

    def managementPolicy(self, traitSets, policyAccess, context, hostSession):
        results = []
        for requested in traitSets:
            data = TraitsData()
            if policyAccess == PolicyAccess.kRead:
                ManagedTrait.imbueTo(data)
                if Location.kId in requested:
                    data.addTrait(Location.kId)
            results.append(data)
        return results

    def isEntityReferenceString(self, value, hostSession):
        return value.startswith(PREFIX)

    def entityTraits(
        self,
        entityReferences,
        entityTraitsAccess,
        context,
        hostSession,
        successCallback,
        errorCallback,
    ):
        for index, reference in enumerate(entityReferences):
            if entityTraitsAccess == EntityTraitsAccess.kRead:
                successCallback(index, {Location.kId})
            else:
                errorCallback(
                    index,
                    BatchElementError(
                        BatchElementError.ErrorCode.kEntityAccessError,
                        "the spike is read-only",
                    ),
                )

    def resolve(
        self,
        entityReferences,
        traitSet,
        resolveAccess,
        context,
        hostSession,
        successCallback,
        errorCallback,
    ):
        for index, reference in enumerate(entityReferences):
            try:
                if resolveAccess != ResolveAccess.kRead:
                    raise ValueError("the spike is read-only")
                binding = self.production.host_bindings.parse(reference.toString())
                if binding.production_id != self.production.id:
                    raise ValueError("reference belongs to another production")
                if not isinstance(binding.object, RepresentationId):
                    raise ValueError("reference is not a representation")
                representation = self.representations[str(binding.object)]
                resolution = next(
                    item
                    for item in self.production.resolve(representation.asset_id)
                    if item.representation_id == representation.id
                )
                candidates = resolution.resources[0].candidates
                if len(candidates) != 1:
                    raise ValueError("representation is not uniquely resolvable")
                data = TraitsData()
                if Location.kId in traitSet:
                    Location(data).setLocation(candidates[0].uri)
                successCallback(index, data)
            except (KeyError, StopIteration, ValueError) as error:
                errorCallback(
                    index,
                    BatchElementError(
                        BatchElementError.ErrorCode.kEntityResolutionError,
                        str(error),
                    ),
                )
