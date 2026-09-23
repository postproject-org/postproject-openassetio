import os

from openassetio.access import ResolveAccess
from openassetio.hostApi import HostInterface, ManagerFactory
from openassetio.log import ConsoleLogger
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory
from openassetio_mediacreation.traits.content import LocatableContentTrait_v1
from postproject import Production

Location = LocatableContentTrait_v1


class Host(HostInterface):
    def identifier(self):
        return "org.postproject.validation-host"

    def displayName(self):
        return "PostProject validation host"


def test_resolves_postproject_representation(tmp_path):
    library = os.environ["POSTPROJECT_LIBRARY"]
    media = tmp_path / "clip.mov"
    media.write_bytes(b"media")
    production_path = tmp_path / "show.pproj"
    with Production.create(production_path, library_path=library) as production:
        with production.transaction() as transaction:
            asset_id = transaction.import_media(media, "clip")
        representation = production.representations[asset_id][0]
        reference = production.host_bindings[representation.id]

    logger = ConsoleLogger()
    factory = PythonPluginSystemManagerImplementationFactory(logger)
    manager = ManagerFactory.createManagerForInterface(
        "org.postproject.manager-validation", Host(), factory, logger
    )
    manager.initialize(
        {"production_path": str(production_path), "library_path": library}
    )
    data = manager.resolve(
        manager.createEntityReference(reference),
        {Location.kId},
        ResolveAccess.kRead,
        manager.createContext(),
    )
    assert Location(data).getLocation() == media.resolve().as_uri()
